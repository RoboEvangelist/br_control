#!/usr/bin/env python
import roslib; roslib.load_manifest('beginner_tutorials')
import rospy
from std_msgs.msg import String

import cv2

import socket
import array
import time

class RovCam(): 
    def __init__(self, data):
        self.host = '192.168.1.100'
        self.port = 80
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.max_tcp_cmd_buffer = 2048
        self.max_image_buffer = 231072
        self.init_connection(data)     #image id is taken from data 

    def init_connection(self, data):
	# Create new socket for video
        self.connect_video()
	
        print "data in video socket: " + data

        m_c = array.array('c')
        m_c.extend(['M', 'O', '_', 'V'])
        m_c.extend('\0')
        i = 0
        while i < 10:
            m_c.extend('\0')
            i = i + 1
        m_c.extend('\x04')
        i = 0
        while i < 3:
            m_c.extend('\0')
            i = i + 1
        m_c.extend('\x04')
        i = 0
        while i < 3:
            m_c.extend('\0')
            i = i + 1
        ldata = list(data)
        id_cp = ldata[25:29]
        m_c.extend(id_cp)
        msg = m_c.tostring()
        self.video_socket.send(msg)

    def connect_video(self):	
        self.video_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.video_socket.connect((self.host, self.port))
        self.video_socket.setblocking(1)

    def disconnect_video(self):
        self.video_socket.close()

    def write_cmd(self, extra_input):	
#	    Robot's Control Packets
        packet_len = 26                          # length of the video buffer
        cmd_buffer = array.array('c')
        cmd_buffer.extend(['M', 'O', '_', 'V'])
        for i in range(4, packet_len+1):	
            cmd_buffer.append('\0')
        cmd_buffer[15] = '\x04'
        cmd_buffer[19] = '\x04'
        for i in range(0, 3):
            if (len(extra_input) >= 4):
                cmd_buffer[i + 22] = extra_input[i]
            else:	
                cmd_buffer[i + 22] = '\0'     #extra_input[1]
        msg = cmd_buffer.tostring()
        self.video_socket.send(msg) 

    def display_image(self):
 	# For now just get one frame, we have to make this a loop of course
        print 'Get video frame!'
        data = ''
        ldata = []
        start = ''
        while len(data) == 0:
            data = self.video_socket.recv(self.max_tcp_cmd_buffer)
            list_data = list(data)
            m_c = array.array('c')
            m_c.extend (list_data[0:4])

            if (start == ''):
                start = 'first'
            else:
                start = m_c.tostring()
            if (start == 'MO_V'):
                break
            else:
                ldata.extend(list_data)

            data = ''

        # Write image to "test.jpg"
        img = ldata[36:]
        img = ''.join(img)
        jpgfile = open('test.jpg', 'wb')
        for i in img:
            jpgfile.write(i)
        jpgfile.close()

#        image = cv2.imread('test.jpg', 1)
 #       cv2.imshow('hola', image)
        time.sleep(1) 
  #      cv2.destroyWindow('test.jpg')
