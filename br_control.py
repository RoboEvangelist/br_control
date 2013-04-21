#!/usr/bin/env python
import roslib; roslib.load_manifest('beginner_tutorials')
import rospy
from std_msgs.msg import String

import br_cam

import socket
import time
import datetime
import array
import struct

class RovCon(): 
    def __init__(self):
        self.host = '192.168.1.100'
        self.port = 80
        self.max_tcp_buffer = 2048
        self.init_connection()
        self.data = ''

    def init_connection(self):
        self.connect_rover()

	# set up rover for communication
        msg = 'GET /check_user.cgi?user=AC13&pwd=AC13 HTTP/1.1\r\nHost: \
        192.168.1.100:80\r\nUser-Agent: WifiCar/1.0 CFNetwork/485.12.7 \
        Darwin/10.4.0\r\nAccept: */*\r\nAccept-Language: \
        en-us\r\nAccept-Encoding: gzip, deflate\r\n \
        Connection: keep-alive\r\n\r\n'
        self.move_socket.send(msg)

		# Get the return message
        print 'Wait for HTML return msg'
        data = ''
        while len(data) == 0:
            data = self.move_socket.recv(self.max_tcp_buffer)
        print data

		# We have to close the socket and open it again
        self.disconnect_rover()
        self.connect_rover()

		# The first MO_O command
        m_c = array.array('c')
        m_c.extend(['M', 'O', '_', 'O'])
        i = 0
        m_c.extend('\x00')
        while i < 18:
            m_c.extend('\0')
            i = i + 1
        msg = m_c.tostring()
        self.move_socket.send(msg)

        print 'Wait for result on 1st MO command'
        data = ''
        while len(data) == 0:
            data = self.move_socket.recv(self.max_tcp_buffer)
        #ldata = list(data)
        # msg_i = ldata[4]

		# The second MO_O command
		#49=4+1+10+1+7+4+9+4+9
        m_c = array.array('c')
        m_c.extend(['M', 'O', '_', 'O'])
        m_c.extend('\x02')
        i = 0
        while i < 10:
            m_c.extend('\0')
            i = i + 1
        m_c.extend('\x1a')
        i = 0
        while i < 7:
            m_c.extend('\0')
            i = i + 1
        m_c.extend(['A', 'C', '1', '3'])
        i = 0
        while i < 9:
            m_c.extend('\0')
            i = i + 1
        m_c.extend(['A', 'C', '1', '3'])
        i = 0
        while i < 9:
            m_c.extend('\0')
            i = i + 1
        msg = m_c.tostring()
        self.move_socket.send(msg)

        print 'Wait for next MO msg'
        data = ''
        while len(data) == 0:
            data = self.move_socket.recv(self.max_tcp_buffer)
		#print list(data)

        m_c = array.array('c')
        m_c.extend(['M', 'O', '_', 'O'])
        m_c.extend('\x04')
        i = 0
        while i < 10:
            m_c.extend('\0')
            i = i + 1
        m_c.extend('\x01')
        i = 0
        while i < 3:
            m_c.extend('\0')
            i = i + 1
            m_c.extend('\x01')
        i = 0
        while i < 3:
            m_c.extend('\0')
            i = i + 1
        m_c.extend('\x02')
        msg = m_c.tostring()
        self.move_socket.send(msg)

        print 'Wait for next MO msg'
        data = ''
        while len(data) == 0:
            data = self.move_socket.recv(self.max_tcp_buffer)
		#print list(data)
        self.data = data

    def connect_rover(self):	
        self.move_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.move_socket.connect((self.host, self.port))
        self.move_socket.setblocking(1)

    def disconnect_rover(self):
        self.move_socket.close()

    def return_data(self):
        return self.data

    def write_cmd(self, index, extra_input):	
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
		#extra_input is a javaArray of Bytes
		
        len = 0
        if index == 1:
            len = 22
        elif index == 2:
            len = 48
        elif index == 3:
            len = 23
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
        buffer.extend(['M', 'O', '_', 'O'])
        for i in range(4, len+1):	
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
        self.move_socket.send(msg)

    # robot's speed is ~2 feet/second

    def move_forward(self, distance, speed):
        speed = 2
        move_time = distance/speed
        init_time = time.time()
        delta_time = 0
        while delta_time <= move_time:
            self.write_cmd(7, 0)
            self.write_cmd(5, 0)
            delta_time = time.time() - init_time
		# stop tracks
        self.write_cmd(12, 0)
        self.write_cmd(13, 0)

    def move_left_forward(self, distance, speed):
        speed = 1
        move_time = distance/speed
        init_time = time.time()
        delta_time = 0
    #	while delta_time <= move_time:       
        self.write_cmd(7, 0)
    #		delta_time = datetime.datetime.now() - delta_time  
		# stop tracks
        self.write_cmd(13, 0)

if __name__ == '__main__':
    try:
        pub = rospy.Publisher('chatter', String)
        rospy.init_node('AC13_robot')
        rover = RovCon() 
        video = RovCam(rover.return_data())
        counter = 0
        distance = 0.5    # feet
        speed = 1         # foot/sec
        while not rospy.is_shutdown(): 
            str = "robot moves %s" % rospy.get_time()
            rospy.loginfo(str)
            pub.publish(String(str))
#           rover.moveForward(distance,speed)
            rover.display_image()
            rospy.sleep(0.1)
#           counter = counter + 1

        rover.disconnect_rover()
    except rospy.ROSInterruptException:
        pass
