#!/usr/bin/env python
import roslib; roslib.load_manifest('beginner_tutorials')
import rospy
from std_msgs.msg import String

import cv2

import socket
import time
import datetime
import array
import struct

class RovCam(): 
	def __init__(self, data):
		self.host = '192.168.1.100'
		self.port = 80
		self.maxTCPBuffer = 2048
		self.initConnection(data)     #image id is taken from data 

	def initConnection(self, data):
		# set up rover for communication
		msg = 'GET /check_user.cgi?user=AC13&pwd=AC13 HTTP/1.1\r\nHost: 192.168.1.100:80\r\nUser-Agent: WifiCar/1.0 \
		CFNetwork/485.12.7 Darwin/10.4.0\r\nAccept: */*\r\nAccept-Language: en-us\r\nAccept-Encoding: gzip, deflate\r\n \
		Connection: keep-alive\r\n\r\n'

		# Create new socket for video
		self.connectRover()

		mc = array.array('c')
		mc.extend(['M','O','_','V']);
		mc.extend('\0')
		i = 0
		while i < 10:
			mc.extend('\0')
			i = i + 1
		mc.extend('\x04')
		i = 0
		while i < 3:
			mc.extend('\0')
			i = i + 1
		mc.extend('\x04')
		i = 0
		while i < 3:
			mc.extend('\0')
			i = i + 1
		ldata = list(data)
		id_cp = ldata[25:29]
		mc.extend(id_cp)
		#print mc, identifier of the image(?)
		msg = mc.tostring()
		self.videoSocket.send(msg)

	def connectRover(self):	
		self.videoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.videoSocket.connect((self.host,self.port))
		self.videoSocket.setblocking(1)

	def disconnectVideo(self):
		self.videoSocket.close()

	def writeCmd(self, index, extraInput):	
#	    Robot's Control Packets
		len = 26                          # actuall length of the video buffer
		buffer = array.array('c')
		buffer.extend(['M','O','_','V']);
		for i in range(4,len+1):	
			buffer.append('\0')
		buffer[15] = '\x04'
		buffer[19] = '\x04'
		for i in range(0,3):
			if (len(extraInput) >= 4):
				buffer[i + 22] = extraInput[i]
			else:	
				buffer[i + 22] = '\0'     #extraInput[1]
		
		msg = buffer.tostring()
		self.videoSocket.send(msg) 

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

