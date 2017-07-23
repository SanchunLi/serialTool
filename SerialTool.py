import sys
import time
import math
import string
import serial
import threading
from PyQt4 import QtCore, QtGui, uic


qtCreatorFile = "mainwindow.ui"   # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

ev1 = threading.Event()
ev2 = threading.Event()
ev3 = threading.Event()
ev4 = threading.Event()
ev5 = threading.Event()
ev6 = threading.Event()

# send the command to change the machine's work-mode
class Send(threading.Thread):
	def __init__(self, signal, port, data1,data2,data3, interval, sendLabel1,sendLabel2,sendLabel3):
	    threading.Thread.__init__(self)  # You must call
	    self.signal = signal
	    self.port = port
	    self.data1 = data1
	    self.data2 = data2
	    self.data3 = data3
	    self.interval = interval
	    self.sendLabel1 = sendLabel1
	    self.sendLabel2 = sendLabel2
	    self.sendLabel3 = sendLabel3
	    self.sendCnt1 = 0
	    self.sendCnt2 = 0
	    self.sendCnt3 = 0

	    self.daemon = True # When the main thread exits the sub-thread to quit
	    self.start()       # start the thread

	def run(self):
		# print(self.port)

		data1 = str(self.data1) # Qstring is changed to Python string object
		''' str(QtCore.QString('def'))   to    'def' '''

		data2 = str(self.data2)
		data3 = str(self.data3)
		interval = self.interval

		while 1:
			# print('send thread: ' + str(self.signal.isSet()))

			if self.signal.isSet():
				break

			# print("send ...")

			while 1:
				ev4.set()

				ev1.set()
				if (data1 != ''):
					# print((round(float(interval1))))

					self.port.write(data1.encode(encoding = "utf-8"))
					self.port.write(b'\x0D\x0A')
					self.sendCnt1 += 1
					self.sendLabel1.setText(str(self.sendCnt1))
				time.sleep(int(interval))
				ev1.clear()

				ev5.set()

				ev2.set()
				if (data2 != ''):
					self.port.write(data2.encode(encoding = "utf-8"))
					self.port.write(b'\x0D\x0A')
					self.sendCnt2 += 1
					self.sendLabel2.setText(str(self.sendCnt2))
				time.sleep(int(interval))
				ev2.clear()

				ev6.set()

				ev3.set()
				if (data3 != ''):
					self.port.write(data3.encode(encoding = "utf-8"))
					self.port.write(b'\x0D\x0A')
					self.sendCnt3 += 1
					self.sendLabel3.setText(str(self.sendCnt3))
				time.sleep(int(interval))
				ev3.clear()


				if self.signal.isSet():
					break

		# print("send thread exit.")
		# self.exiting = True
		# self.wait()

# receive the feedback to checkout if the work-mode has been changed correctly
class Recv(threading.Thread):
	def __init__(self,signal, port, recv1Label, recv2Label, recv3Label):
	    threading.Thread.__init__(self) # You must call
	    self.signal = signal
	    self.port = port
	    self.recv1Label = recv1Label
	    self.recv1Cnt = 0
	    self.recv2Label = recv2Label
	    self.recv2Cnt = 0
	    self.recv3Label = recv3Label
	    self.recv3Cnt = 0

	    self.laststate = 0x00   # record the last work-mode (u8Mode),,,,,

	    self.daemon = True  # When the main thread exits the sub-thread to quit
	    self.start()        # start the thread

	def run(self):
		print(self.port)
		while 1:
			# print('recv thread: ' + str(self.signal.isSet()))

			# print("listen ...")

			if self.signal.isSet():
				break

			datatemp = self.port.readline()
			if "YaoCe" in datatemp:
				data = datatemp.strip().split(',')
				u8Modetemp = data[len(data) - 3]
				u8Mode = int(u8Modetemp,16)

			# data = self.port.read(1)
			# if data == b'\x05':
				# data = self.port.read(1)
				# if data == b'\x0A':
				# 	u8Type = self.port.read(1)
				# 	u8Len = self.port.read(1)
				# 	u8Mode = self.port.read(1)
				# 	u8ExpTime1 = self.port.read(1)
				# 	u8ExpTime2 = self.port.read(1)
				# 	u8ExpTime3 = self.port.read(1)
				# 	u8checkSum = ord(self.port.read(1))
				# 	# check
				# 	realSumtmp = ord(u8Type) + ord(u8Len) + ord(u8Mode) +ord(u8ExpTime1) + ord(u8ExpTime2) + ord(u8ExpTime3)

				# 	realSum = realSumtmp % 256
				# 	print 'Sum: ' + str(realSum)
				# 	print 'Check: ' + str(u8checkSum)
				# 	if realSum == u8checkSum:

				# 		# print( 'check succeed: ' + str(u8Mode))

				if (u8Mode & 0x30) == 0x10:
					if ev4.isSet():
						self.laststate = 0x00
						ev4.clear()
					# print 'pre:'+str(self.laststate)

					if (self.laststate != 0x10) and (self.laststate != 0x20) and (self.laststate != 0x30) and (ev1.isSet()):
						self.recv1Cnt += 1
						self.recv1Label.setText(str(self.recv1Cnt))

				if (u8Mode & 0x30) == 0x20:
					if ev5.isSet():
						self.laststate = 0x00
						ev5.clear()

					if (self.laststate != 0x20) and (self.laststate != 0x10) and (self.laststate != 0x30)  and (ev2.isSet()):
						self.recv2Cnt += 1
						self.recv2Label.setText(str(self.recv2Cnt))

				if (u8Mode & 0x30) == 0x30:
					if ev6.isSet():
						self.laststate = 0x00
						ev6.clear()

					if (self.laststate != 0x30) and (self.laststate != 0x10) and (self.laststate != 0x20)  and (ev3.isSet()):
						self.recv3Cnt += 1
						self.recv3Label.setText(str(self.recv3Cnt))

				self.laststate = u8Mode    # important!!!

		# print("recv thread exit.")
		self.exiting = True


# main interface
class MyApp(QtGui.QMainWindow, Ui_MainWindow):

	signal = threading.Event()

	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.cmd1bt.clicked.connect(self.cmd1bt_func)

	def cmd1bt_func(self):

		if self.cmd1bt.isChecked():
			# print("cmd1 pressed")
			self.cmd1bt.setText('stop')

			self.sendCnt1.setText('0')
			self.sendCnt2.setText('0')
			self.sendCnt3.setText('0')
			self.recvCnt1.setText('0')
			self.recvCnt2.setText('0')
			self.recvCnt3.setText('0')

			portID = self.comPortID.currentText()
			baudrate = self.baudrateLabel.currentText()

			bytesize = serial.EIGHTBITS
			parity = serial.PARITY_NONE
			stopbits= serial.STOPBITS_TWO

			# also selected according demand
			bytesizetmp= self.bytesizeLabel.currentText()
			# print('gui: ' + bytesizetmp)
			if bytesizetmp == '8':
				bytesize = serial.EIGHTBITS
			elif bytesizetmp == '7':
				bytesize = serial.SEVENBITS
			elif bytesizetmp == '6':
				bytesize = serial.SIXBITS
			elif bytesizetmp == '5':
				bytesize = serial.FIVEBITS

			paritytmp = self.parity.currentText()
			if paritytmp == 'NONE':
				parity = serial.PARITY_NONE
			elif paritytmp == 'EVEN':
				parity = serial.PARITY_EVEN
			elif paritytmp == 'ODD':
				parity = serial.PARITY_ODD
			elif paritytmp == 'MARK':
				parity = serial.PARITY_MARK
			elif paritytmp == 'SPACE':
				parity = serial.PARITY_SPACE
			# print(parity)

			stopbitstmp = self.stopbitssize.currentText()
			if stopbitstmp == '1':
				stopbits= serial.STOPBITS_ONE
			elif stopbitstmp == '1.5':
				stopbits = serial.STOPBITS_ONE_POINT_FIVE
			elif stopbitstmp == '2':
				stopbits = serial.STOPBITS_TWO
			# print(stopbits)

			#self.comPort = serial.Serial(portID,baudrate = baudrate1,bytesize = bytesize1,parity = parity1,stopbits = stopbits1,timeout = 0.1,xonxoff) # open
			self.comPort = serial.Serial(str(portID),baudrate,bytesize,parity,stopbits,timeout = 0.1)   # open

			data1 = self.cmd1label.toPlainText()
			data2 = self.cmd2label.toPlainText()
			data3 = self.cmd3label.toPlainText()
			interval = self.interval.toPlainText()

			# print('data2:' + str(data2))

			self.signal.clear()

			Send(self.signal, self.comPort, data1, data2, data3, interval,self.sendCnt1, self.sendCnt2, self.sendCnt3)

			Recv(self.signal, self.comPort, self.recvCnt1, self.recvCnt2, self.recvCnt3)

		else:
			print("cmd1 released")

			self.signal.set()
			# print('main: ' + str(self.signal.isSet()))
			self.cmd1bt.setText('send')

			# Send.join()  # wait thread exit
			# Recv.join()

			self.comPort.close() # close

	def cmd2bt_func(self):
		print("cmd2 pushed")
	def cmd3bt_func(self):
		print("cmd3 pushed")


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = MyApp()
window.show()
sys.exit(app.exec_())
