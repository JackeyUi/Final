import serial
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

while 1 :
   line = s.read(22)
   print(line.decode())