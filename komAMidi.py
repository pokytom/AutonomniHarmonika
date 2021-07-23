from mido import MidiFile
import serial
import pigpio
from os import path

WIND_POWER = 0

PLAYING_SONG = False

def set_bit(value, bit):
    return value | (1<<bit+1)

def clear_bit(value, bit):
    return value & ~(1<<bit+1)

def check_bit_possitive(value, bit):
    return value & (1 << bit+1)

def find_byte(note):
    return note // 7

def find_bit_position(note):
    return note % 7

def play_song(file):
	# metoda pro prehrani pisne
	global PLAYING_SONG
	PLAYING_SONG = True
	#pi = pigpio.pi()
	#pi.set_PWM_dutycycle(13,WIND_POWER)
	f = open("komunikaceFile.txt", "w")
	#ser = serial.Serial('/dev/ttyUSB0',9600)
#	print(ser.name, ser.baudrate)
	file_path = '{}{}'.format('./songs/', file)
	if file[-3:] != 'mid' or not path.exists(file_path):
		f.close()
#		ser.close
#		pi.set_PWM_dutycycle(13, 0)
		return False
	notes = [1, 0, 0, 0, 0]

	for msg in MidiFile(file_path).play():
		if PLAYING_SONG:
			val = msg.dict()
			if tuple(val.items())[0][1] != 'program_change' and tuple(val.items())[0][1] != 'control_change':
				note = tuple(val.items())[3][1]-53

				byte = find_byte(note)
				bit_possition = find_bit_position(note)
				if check_bit_possitive(notes[byte], bit_possition):
					notes[byte] = clear_bit(notes[byte], bit_possition)
				else:
					notes[byte] = set_bit(notes[byte], bit_possition)
				output_ser = b''
				print(lookup(note+53))
				for i in range(5):
					output_ser += lookup(notes[i])

#				ser.write(output_ser)
				listTestByteAsHex = [int(hex(x).split('x')[-1]) for x in output_ser]
				print(listTestByteAsHex)
				print(output_ser)
		else:
			break
#	ser.close()
	f.close()
#	pi.set_PWM_dutycycle(13, 0)
	PLAYING_SONG = False

	return True

def play_note(note_number):
	# metoda pro zapnuti/vypnuti noty
	ser = serial.Serial('/dev/ttyUSB0', 9600)
	print(ser.name, ser.baudrate)

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
	WIND_POWER = power
	return

def get_wind_power():
	global WIND_POWER
	return WIND_POWER

def check_song_exist(name):
	if not path.exists('{}{}'.format('./songs/', name)):
		return False
	return True



