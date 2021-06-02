from mido import MidiFile
import serial
from os import path


def play_song(file):
	f = open("komunikaceFile.txt", "w")
	ser = serial.Serial('/dev/ttyUSB0',9600)
	print(ser.name, ser.baudrate)
	file_path = '{}{}'.format('./songs/', file)
	if file[-3:] != 'mid' or not path.exists(file_path):
		return False
	for msg in MidiFile(file_path).play():
		val = msg.dict()
		output = ser.write((tuple(val.items())[3][1]))
		#output_str = f'{output}'
		output_chr = chr(output)
		print(output_chr)
		f.write(output_chr)
	ser.close()
	f.close()
	return True
