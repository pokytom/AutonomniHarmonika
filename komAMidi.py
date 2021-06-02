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
		note = tuple(val.items())[3][1]
		output_ser = lookup(note)
		ser.write(output_ser)
		#print(output) #int 69
		#output_str = f'{output}'
		#print(output_str) #string 69 - please enode to bytes
		#output_chr = chr(output)
		#print(output_chr) #string E
		#output_ser = ser.write(output.encode('UTF-8'))
		print(output_ser)
		#f.write(bin(output_ser))
	ser.close()
	f.close()
	return True

def lookup(i):
	switcher={
		65: b'A',
		66: b'B',
		67: b'C',
		68: b'D',
		69: b'E',
		70: b'F',
		71: b'G',
		72: b'H'
	}
	return switcher.get(i,"Chybna nota")
