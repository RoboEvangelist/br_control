#!/usr/bin/env python
import roslib; roslib.load_manifest('beginner_tutorials')
import rospy
from std_msgs.msg import String

import cv2

import socket
import time
import array

class RovCam(): 
    def __init__(self, data):
        self.host = '192.168.1.100'
        self.port = 80
        self.max_tcp_buffer = 2048
        self.init_connection(data)     #image id is taken from data 

    def init_connectionion(self, data):
	# set up rover for communication
        msg = 'GET /check_user.cgi?user=AC13&pwd=AC13 HTTP/1.1\r\nHost: \
        192.168.1.100:80\r\nUser-Agent: WifiCar/1.0 CFNetwork/485.12.7 \
        Darwin/10.4.0\r\nAccept: */*\r\nAccept-Language: \
        en-us\r\nAccept-Encoding: gzip, deflate\r\n \
        Connection: keep-alive\r\n\r\n'


	# Create new socket for video
        self.connect_rover()

        mc = array.array('c')
        mc.extend(['M', 'O', '_', 'V'])
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
        self.video_socket.send(msg)

    def connect_rover(self):	
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.video_socket.connect((self.host, self.port))
        self.video_socket.setblocking(1)

    def disconnect_video(self):
        self.video_socket.close()

    def writeCmd(self, index, extra_input):	
#	    Robot's Control Packets
        len = 26                          # actuall length of the video buffer
        buffer = array.array('c')
        buffer.extend(['M', 'O', '_', 'V'])
        for i in range(4, len+1):	
            buffer.append('\0')
        buffer[15] = '\x04'
        buffer[19] = '\x04'
        for i in range(0,3):
            if (len(extra_input) >= 4):
                buffer[i + 22] = extra_input[i]
            else:	
                buffer[i + 22] = '\0'     #extra_input[1]
		
        msg = buffer.tostring()
        self.video_socket.send(msg) 

    def displayImage(self):
 	# For now just get one frame, we have to make this a loop of course
        print 'Get video frame!'
        data = ''
        ldata = []
        start = ''
        while len(data) == 0:
            data = self.video_socket.recv(self.max_tcp_buffer)
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
        jpgfile = open('test.jpg', 'wb')
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

