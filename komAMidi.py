from mido import MidiFile
import serial
from os import path


def play_song(file):
	#ser = serial.Serial('/dev/ttyUSB0',9600)
	#print(ser.name, ser.baudrate)
	file_path = '{}{}'.format('./songs/', file)
	if file[-3:] != 'mid' or not path.exists(file_path):
		return False
	for msg in MidiFile(file_path).play():
		val = msg.dict()
		#output = ser.write((tuple(val.items())[3][1]))
		print(tuple(val.items())[3][1])
		#f.write(output)
	#ser.close()
	return True
