from mido import MidiFile
import serial
import pigpio
from os import path

PLAYING_SONG = False

def play_song(file):
	# metoda pro prehrani pisne
	global PLAYING_SONG
	PLAYING_SONG = True
	#pi = pigpio.pi()
	#pi.set_PWM_dutycycle(13,6)
	f = open("komunikaceFile.txt", "w")
	#ser = serial.Serial('/dev/ttyUSB0',9600)
	#print(ser.name, ser.baudrate)
	file_path = '{}{}'.format('./songs/', file)
	if file[-3:] != 'mid' or not path.exists(file_path):
		f.close()
		#ser.close
		#pi.set_PWM_dutycycle(13, 0)
		return False
	for msg in MidiFile(file_path).play():
		if PLAYING_SONG:
			val = msg.dict()
			if tuple(val.items())[0][1] != 'program_change' and tuple(val.items())[0][1] != 'control_change':
				note = tuple(val.items())[3][1]
				output_ser = lookup(note)
				#ser.write(output_ser)
				print(output_ser)
		else:
			break
	#ser.close()
	f.close()
	#pi.set_PWM_dutycycle(13, 0)
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
	pi.set_PWM_dutycycle(13, 6)
	print("vzduch zapnut")

	return True

def lookup(i):
	return i.to_bytes(1, 'big')#switcher.get(i,0)