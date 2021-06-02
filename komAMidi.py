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
		output = tuple(val.items())[3][1]
		#output_str = f'{output}'
		output_chr = chr(output)
		output_ser = ser.write(.format(output_chr))
		print(output_ser)
		#f.write(output_ser)
	ser.close()
	f.close()
	return True
