import serial

ser = serial.Serial('/dev/ttyUSB0',9600)
print(ser.name, ser.baudrate)
ser.write(b'E')
ser.close()
