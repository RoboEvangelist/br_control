#!/usr/bin/env python
import roslib; roslib.load_manifest('beginner_tutorials')
import rospy
from std_msgs.msg import String

import socket
import time
import datetime
import array
import struct

class RovCon(): 
	def __init__(self):
		self.host = '192.168.1.100'
		self.port = 80
		self.maxTCPBuffer = 2048
		self.initConnection()

	def initConnection(self):
		self.moveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.moveSocket.connect((self.host,self.port))
		self.moveSocket.setblocking(1)
		
		# set up rover for communication
		msg = 'GET /check_user.cgi?user=AC13&pwd=AC13 HTTP/1.1\r\nHost: \
		192.168.1.100:80\r\nUser-Agent: WifiCar/1.0 CFNetwork/485.12.7 \
		Darwin/10.4.0\r\nAccept: */*\r\nAccept-Language: \
		en-us\r\nAccept-Encoding: gzip, deflate\r\n Connection: keep-alive\r\n\r\n'
		self.moveSocket.send(msg)

		# Get the return message
		print 'Wait for HTML return msg'
		data = ''
		while len(data) == 0:
			data = self.moveSocket.recv(self.maxTCPBuffer)
		print data

		self.moveSocket.close()

		# We have to close the socket and open it again
		self.moveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.moveSocket.connect((self.host,self.port))
		self.moveSocket.setblocking(1)

		# The first MO_O command
		mc = array.array('c')
		mc.extend(['M','O','_','O']);
		i = 0
		mc.extend('\x00')
		while i < 18:
			mc.extend('\0')
			i = i + 1
		msg = mc.tostring()
		self.moveSocket.send(msg)

		print 'Wait for result on 1st MO command'
		data = ''
		while len(data) == 0:
			data = self.moveSocket.recv(self.maxTCPBuffer)
		ldata = list(data)
		msg_i = ldata[4]

		# The second MO_O command
		#49=4+1+10+1+7+4+9+4+9
		mc = array.array('c')
		mc.extend(['M','O','_','O']);
		mc.extend('\x02')
		i = 0
		while i < 10:
			mc.extend('\0')
			i = i + 1
		mc.extend('\x1a')
		i = 0
		while i < 7:
			mc.extend('\0')
			i = i + 1
		mc.extend(['A','C','1','3']);
		i = 0
		while i < 9:
			mc.extend('\0')
			i = i + 1
		mc.extend(['A','C','1','3']);
		i = 0
		while i < 9:
			mc.extend('\0')
			i = i + 1
		msg = mc.tostring()
		self.moveSocket.send(msg)

		print 'Wait for next MO msg'
		data = ''
		while len(data) == 0:
			data = self.moveSocket.recv(self.maxTCPBuffer)
		#print list(data)

		mc = array.array('c')
		mc.extend(['M','O','_','O']);
		mc.extend('\x04')
		i = 0
		while i < 10:
			mc.extend('\0')
			i = i + 1
		mc.extend('\x01')
		i = 0
		while i < 3:
			mc.extend('\0')
			i = i + 1
		mc.extend('\x01')
		i = 0
		while i < 3:
			mc.extend('\0')
			i = i + 1
		mc.extend('\x02')
		msg = mc.tostring()
		self.moveSocket.send(msg)

		print 'Wait for next MO msg'
		data = ''
		while len(data) == 0:
			data = self.moveSocket.recv(self.maxTCPBuffer)
		#print list(data)

	def disconnectRover(self):
		self.moveSocket.close()

	def writeCmd(self, index, extraInput):	
#	     Robot's Control Packets

# 		     The left brake command is 
# 		      1 4d 4f 5f 4f fa 00 00 00 00 00 00 00 00 00 00 02
# 		      0010 00 00 00 01 00 00 00 02 00
# 		 02 was the byte that puts the left break
# 
# 		     and the right brake command is
# 		      0000 4d 4f 5f 4f fa 00 00 00 00 00 00 00 00 00 00 02
# 		      0010 00 00 00 01 00 00 00 04 00
# 		  04 was the byte that puts the left break
# 
# 		     Left Wheel forward
# 		      0000 4d 4f 5f 4f fa 00 00 00 00 00 00 00 00 00 00 02
# 		      0010 00 00 00 01 00 00 00 04 0a
# 		 
# 		     Right Wheel Forward
# 		      0000 4d 4f 5f 4f fa 00 00 00 00 00 00 00 00 00 00 02
# 		      0010 00 00 00 01 00 00 00 01 0a
# 		 
# 		     Left Wheel Backward
# 		      0000 4d 4f 5f 4f fa 00 00 00 00 00 00 00 00 00 00 02
# 		      0010 00 00 00 01 00 00 00 05 0a
# 		 
# 		     Right Wheel Backward
# 		      0000 4d 4f 5f 4f fa 00 00 00 00 00 00 00 00 00 00 02
# 		      0010 00 00 00 01 00 00 00 02 0a
 
		# index is integer which specifies which command to send
		#extraInput is a javaArray of Bytes
		
		len = 0
		if index == 1:
			len = 22
		elif index == 2:
			len = 48
		elif index == 3:
			len = 23
		elif index == 4: 
			len = 26 
		elif index == 5:
			len = 24
		elif index == 6:
			len = 24
		elif index == 7:
			len = 24
		elif index == 8:
			len = 24
		elif index == 9:
			len = 22
		elif index == 10:
			len = 23
		elif index == 11:
			len = 23
		elif index == 12:
			len = 24
		elif index == 13:
			len = 24

		buffer = array.array('c')
		buffer.extend(['M','O','_','O']);
		if index == 4:
			buffer[3] = 'V'
		for i in range(4,len+1):	
			buffer.append('\0')

		if index == 1:
			buffer[4] = '\x02'
		elif index == 2:
			buffer[4] = '\x02'
			buffer[15] = '\x1a'
			buffer[23] = 'A'
			buffer[24] = 'C'
			buffer[25] = '1'
			buffer[26] = '3'
			buffer[36] = 'A'
			buffer[37] = 'C'
			buffer[38] = '1'
			buffer[39] = '3'
		elif index == 3:
			buffer[4] = '\x04'
			buffer[15] = '\x01'
			buffer[19] = '\x01'
			buffer[23] = '\x02'
		elif index == 4: 
			buffer[15] = '\x04'
			buffer[19] = '\x04'
			for i in range(0,3):
				if (len(extraInput) >= 4):
					buffer[i + 22] = extraInput[i]
				else:	
					buffer[i + 22] = '\0'     #extraInput[1]
		elif index == 5:     # left wheel Forward
			buffer[4] = '\xfa'
			buffer[15] = '\x02'
			buffer[19] = '\x01'
			buffer[23] = '\x04'
			buffer[24] = '\x0a'
		elif index == 6:    # left wheel Backward
			buffer[4] = '\xfa'
			buffer[15] = '\x02'
			buffer[19] = '\x01'
			buffer[23] = '\x05'
			buffer[24] = '\x0a'
		elif index == 7:    # right wheel Forward
			buffer[4] = '\xfa'
			buffer[15] = '\x02'
			buffer[19] = '\x01'
			buffer[23] = '\x01'
			buffer[24] = '\x0a'
		elif index == 8:    # right whell backward
			buffer[4] = '\xfa'
			buffer[15] = '\x02'
			buffer[19] = '\x01'
			buffer[23] = '\x02'
			buffer[24] = '\x0a'
		elif index == 9:    # IR off(?)
			buffer[4] = '\xff'
		elif index == 10:   # switches infrared LED on
			buffer[4] = '\x0e'
			buffer[15] = '\x01'
			buffer[19] = '\x01'
			buffer[23] = '\x5e'
		elif index == 11:   # switches infrared LED off
			buffer[4] = '\x0e'
			buffer[15] = '\x01'
			buffer[19] = '\x01'
			buffer[23] = '\x5f'
		elif index == 12:   # stop left track
			buffer[4] = '\xfa'
			buffer[15] = '\x02'
			buffer[19] = '\x01'
			buffer[23] = '\x02'
			buffer[24] = '\x00'
		elif index == 13:  # stop right track
			buffer[4] = '\xfa'
			buffer[15] = '\x02'
			buffer[19] = '\x01'
			buffer[23] = '\x04'
			buffer[24] = '\x00'
		msg = buffer.tostring()
		if index == 4:
			self.videoSocket.send(msg)   				
		else:
			self.moveSocket.send(msg)

# robot's speed is ~2 feet/second

	def moveForward(self, distance, speed):
		speed = 2
		moveTime = distance/speed
		iniTime = time.time()
		deltaTime = 0
		while deltaTime <= moveTime:
			self.writeCmd(7,0)
			self.writeCmd(5,0)
			deltaTime = time.time() - iniTime
		# stop tracks
		self.writeCmd(12,0)
		self.writeCmd(13,0)

	def moveLeftForward(self, distance, speed):
		speed = 1
		moveTime = distance/speed
		iniTime = time.time()
		deltaTime = 0
	#	while deltaTime <= moveTime:       
		self.writeCmd(7,0)
	#		deltaTime = datetime.datetime.now() - deltaTime  
		# stop tracks
		self.writeCmd(13,0)

	def displayImage(self):
 		# For now just get one frame, we have to make this a loop of course
		print 'Get video frame!'
		data = ''
		ldata = []
		start = ''
		while len(data) == 0:
			data = self.videoSocket.recv(self.maxTCPBuffer)
			ld = list(data)
			mc = array.array('c')
			mc.extend (ld[0:4])

			if (start == ''):
				start = 'first'
			else:
				start = mc.tostring()
			if (start == 'MO_V'):
				break
			else:
				ldata.extend(ld)

			data = ''

		# Write image to "test.jpg"
		img = ldata[36:]
		jpgfile = open('test.jpg','wb')
		for i in img:
			jpgfile.write(i)
		# Close file handlers
		jpgfile.close()

		image = cv2.imread('test.jpg')
		#cv2.NamedWindow('hola', WINDOW_AUTOSIZE)
		#cv2.ShowImage('robot window', image)
		cv2.imshow('hola', image)
		cv2.waitKey(100)
		cv2.destroyWindow('test.jpg')

if __name__ == '__main__':
    try:
	pub = rospy.Publisher('chatter', String)
	rospy.init_node('AC13_robot')
	rover = RovCon() 
	counter = 0
	distance = 0.5    # feet
	speed = 1         # foot/sec
	while not rospy.is_shutdown(): 
		str = "robot moves %s" % rospy.get_time()
		rospy.loginfo(str)
		pub.publish(String(str))
#		rover.moveForward(distance,speed)
		rover.displayImage()
		rospy.sleep(0.1)
#		counter = counter + 1

	rover.disconnectRover()
    except rospy.ROSInterruptException:
        pass
