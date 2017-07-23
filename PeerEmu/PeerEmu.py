import serial
import string
import time

sp = serial.Serial('COM2')  # you can use your COMx to replace it
# print('listen ...')

# data = 'aa'
# data = input("Please enter the command")

while 1:
	data = sp.read(2)
	# print(data)

	# Send feedback cycle
	cnt = 1
	while cnt <= 10:
		if data == b'aa':
			print("recv cmd1 ok")
			# sp.write(b'\x05\x0A\x00\x00\x20\x00\x00\x00\x20')
			sp.write(b'>dykb 3')
			sp.write(b'\x0D\x0A')
			sp.write(b'dykb send 8 bytes.')
			sp.write(b'\x0D\x0A')
			sp.write(b'  (05 0A 24 03)')
			sp.write(b'\x0D\x0A')
			sp.write(b'  (14 03 03 41)')
			sp.write(b'\x0D\x0A')
			sp.write(b'>1126 YaoCe B: 0x50,0x0A,0xAA,0x04,0x20,6380,0xD2')
			sp.write(b'\x0D\x0A')
			sp.write(b'>1127 YaoCe B: 0x50,0x0A,0xAA,0x04,0x10,5931,0x00')
			sp.write(b'\x0D\x0A')

		elif data == b'bb':
			print("recv cmd2 ok")
			# sp.write(b'\x05\x0A\xAA\x04\x20\x00\x00\x00\x00')
			sp.write(b'>dykb 3')
			sp.write(b'\x0D\x0A')
			sp.write(b'dykb send 8 bytes.')
			sp.write(b'\x0D\x0A')
			sp.write(b'  (05 0A 24 03)')
			sp.write(b'\x0D\x0A')
			sp.write(b'  (14 03 03 41)')
			sp.write(b'\x0D\x0A')
			sp.write(b'>1126 YaoCe B: 0x50,0x0A,0xAA,0x04,0x10,6337,0x97')
			sp.write(b'\x0D\x0A')
			sp.write(b'>1127 YaoCe B: 0x50,0x0A,0xAA,0x04,0x20,5973,0x3A')
			sp.write(b'\x0D\x0A')

		elif data == b'cc':

			print("recv cmd3 ok")
			# sp.write(b'\x05\x0A\xAA\x04\x30\x00\x00\x00\x00')
			sp.write(b'>dykb 3')
			sp.write(b'\x0D\x0A')
			sp.write(b'dykb send 8 bytes.')
			sp.write(b'\x0D\x0A')
			sp.write(b'  (05 0A 24 03)')
			sp.write(b'\x0D\x0A')
			sp.write(b'  (14 03 03 41)')
			sp.write(b'\x0D\x0A')
			sp.write(b'>1126 YaoCe B: 0x50,0x0A,0xAA,0x04,0x20,6348,0xB2')
			sp.write(b'\x0D\x0A')
			sp.write(b'>1127 YaoCe B: 0x50,0x0A,0xAA,0x04,0x30,5943,0x2C')
			sp.write(b'\x0D\x0A')

		else:
			print('error cmd')

		time.sleep(0.01)  # Send feedback cycle
		cnt += 1

sp.close()
