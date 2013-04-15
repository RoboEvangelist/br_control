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
	def __init__(self):
		self.host = '192.168.1.100'
		self.port = 80
		self.maxTCPBuffer = 2048
		self.initConnection()

	def initConnection(self):
		# set up rover for communication
		msg = 'GET /check_user.cgi?user=AC13&pwd=AC13 HTTP/1.1\r\nHost: 192.168.1.100:80\r\nUser-Agent: WifiCar/1.0 \
		CFNetwork/485.12.7 Darwin/10.4.0\r\nAccept: */*\r\nAccept-Language: en-us\r\nAccept-Encoding: gzip, deflate\r\n \
		Connection: keep-alive\r\n\r\n'

		# Create new socket for video
		self.videoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.videoSocket.connect((self.host,self.port))
		self.videoSocket.setblocking(1)

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





