from mido import MidiFile
import serial
import pigpio
from os import path

WIND_POWER = 0
NOTES_ON = 0

PLAYING_SONG = False

def calc_wind_power(notes=0):
	wd_power = WIND_POWER + notes * 0.5
	if wd_power >= 15:
		return 15
	else:
		return wd_power

def play_song(file):
	# metoda pro prehrani pisne
	global PLAYING_SONG
	notes_on = 0
	PLAYING_SONG = True
	pi = pigpio.pi()
	pi.set_PWM_dutycycle(13,WIND_POWER)
	f = open("komunikaceFile.txt", "w")
	ser = serial.Serial('/dev/ttyUSB0',9600)
	print(ser.name, ser.baudrate)
	file_path = '{}{}'.format('./songs/', file)
	if file[-3:] != 'mid' or not path.exists(file_path):
		f.close()
		ser.close
		pi.set_PWM_dutycycle(13, 0)
		return False
	for msg in MidiFile(file_path).play():
		if PLAYING_SONG:
			val = msg.dict()
			if tuple(val.items())[0][1] != 'program_change' and tuple(val.items())[0][1] != 'control_change':
				note = tuple(val.items())[3][1]
				#vypnuti noty
				if ((tuple(val.items())[0][1] == 'note_off' or tuple(val.items())[4][1] == 0) and (53 <= note <=84)):
					output_ser = lookup(note-21)
					ser.write(output_ser)
					print(output_ser)
					notes_on -= 1
				#zapnuti noty
				elif(tuple(val.items())[0][1] == 'note_on' and (53 <= note <=84)):
					output_ser = lookup(note+11)
					ser.write(output_ser)
					print(output_ser)
					notes_on += 1
				else:
					print("nota mimo rozsah!")
				pi.set_PWM_dutycycle(13, calc_wind_power(notes_on))
		else:
			break
	ser.close()
	f.close()
	pi.set_PWM_dutycycle(13, 0)
	PLAYING_SONG = False

	return True

def play_note(note_number):
	global NOTES_ON
	# metoda pro zapnuti/vypnuti noty
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	print(ser.name, ser.baudrate)
	pi = pigpio.pi()
	if note_number >= 64:
		NOTES_ON += 1
	else:
		NOTES_ON -= 1
	pi.set_PWM_dutycycle(13, calc_wind_power(NOTES_ON))
	print(calc_wind_power(NOTES_ON))
	output = lookup(note_number)
	ser.write(output)
	print(output)

	ser.close()
	return True

def reset():
	global PLAYING_SONG
	PLAYING_SONG = False
	# metoda pro nulovani vystupu a vypnuti vzduchu
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	print(ser.name, ser.baudrate)

	pi = pigpio.pi()
	pi.set_PWM_dutycycle(13, 0)
	print("vzduch vypnut")

	output = b'r'
	ser.write(output)
	print(output)

	ser.close()
	return True

def air_on():
	# metoda pro zapnuti vzduchu

	pi = pigpio.pi()
	pi.set_PWM_dutycycle(13, WIND_POWER)
	print("vzduch zapnut, hlasitost:", WIND_POWER)

	return True

def lookup(i):
	return i.to_bytes(1, 'big')#switcher.get(i,0)

def set_wind_power(power):
	global WIND_POWER
	if power == 1:
		WIND_POWER = 5
	elif power == 2:
		WIND_POWER = 9
	elif power == 3:
		WIND_POWER = 15
	else:
		WIND_POWER = 0
	return

def get_wind_power():
	global WIND_POWER
	return WIND_POWER

def check_song_exist(name):
	if not path.exists('{}{}'.format('./songs/', name)):
		return False
	return True



