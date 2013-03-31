#!/usr/bin/env python
import roslib; roslib.load_manifest('beginner_tutorials')
import rospy
from std_msgs.msg import String

import socket
import time
import array
import struct

class RovCon(): 
	def __init__(self):
        super(Interface, self).__init__()

		self.pub = rospy.Publisher('chatter', String)
		rospy.init_node('roboTalker')
		self.host = '192.168.1.100'
		self.port = 80
		self.maxTCPBuffer = 2048
		self.initConnection()

	def initConnection(self):
		moveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		moveSocket.connect((host,port))
		moveSocket.setblocking(1)
		msg = 'GET /check_user.cgi?user=AC13&pwd=AC13 HTTP/1.1\r\nHost: 192.168.1.100:80\r\n
			User-Agent: WifiCar/1.0 CFNetwork/485.12.7 Darwin/10.4.0\r\nAccept: */*\r\n
			Accept-Language: en-us\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\n\r\n'
		moveSocket.send(msg)

		# Get the return message
		print 'Wait for HTML return msg'
		data = ''
		while len(data) == 0:
			data = moveSocket.recv(size)
		print data

		moveSocket.close()

		# We have to close the socket and open it again
		moveSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		moveSocket.connect((host,port))
		moveSocket.setblocking(1)

		# The first MO_O command
		mc = array.array('c')
		mc.extend(['M','O','_','O']);
		i = 0
		mc.extend('\x00')
		while i < 18:
			mc.extend('\0')
			i = i + 1
		msg = mc.tostring()
		moveSocket.send(msg)

		print 'Wait for result on 1st MO command'
		data = ''
		while len(data) == 0:
			data = moveSocket.recv(size)
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
		moveSocket.send(msg)

		print 'Wait for next MO msg'
		data = ''
		while len(data) == 0:
			data = moveSocket.recv(size)
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
		moveSocket.send(msg)

		print 'Wait for next MO msg'
		data = ''
		while len(data) == 0:
			data = moveSocket.recv(size)
		#print list(data)

		# Create new socket for video
		videoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		videoSocket.connect((host,port))
		videoSocket.setblocking(1)

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
		videoSocket.send(msg)


	def writeCmd(self, object, index, extraInput)	
	 # index is integer which specifies which command to send
         #j_extra_input is a javaArray of Bytes





	# For now just get one frame, we have to make this a loop of course
	print 'Get video frame!'
	data = ''
	ldata = []
	start = ''
	while len(data) == 0:
		data = videoSocket.recv(size)
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
	videoSocket.close()
	videoSocket.close()

	while not rospy.is_shutdown():
		str = "robot connected %s" % rospy.get_time()
		rospy.loginfo(str)
		pub.publish(String(str))
		rospy.sleep(1.0)


if __name__ == '__main__':
    try:
        roboTalker()
    except rospy.ROSInterruptException:
        pass
