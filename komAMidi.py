from mido import MidiFile
import serial
import pigpio
from os import path


def play_song(file):
	pi = pigpio.pi()
	pi.set_PWM_dutycycle(13,6)
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
		print(output_ser)
	ser.close()
	f.close()
	pi.set_PWM_dutycycle(13, 0)
	return True

def lookup(i):
	return i.to_bytes(1, 'big')#switcher.get(i,0)