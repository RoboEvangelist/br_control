#!/usr/bin/env python
import roslib; roslib.load_manifest('beginner_tutorials')
import rospy
from std_msgs.msg import String

import br_cam

import socket
import time
import array

class RovCon(): 
    def __init__(self):
        self.host = '192.168.1.100'
        self.port = 80
        self.max_tcp_cmd_buffer = 2048
        self.init_connection()
        self.final_data = ''

    def init_connection(self):
        self.connect_rover()

	# set up rover for communication
        msg = ['GET /check_user.cgi?user=AC13&pwd=AC13 HTTP/1.1\r\nHost: '] 
        msg.append('192.168.1.100:80\r\n')
        msg.append('User-Agent: WifiCar/1.0 CFNetwork/485.12.7 ')
        msg.append('Darwin/10.4.0\r\nAccept: */*\r\nAccept-Language: ')
        msg.append('en-us\r\nAccept-Encoding: gzip, deflate\r\n')
        msg.append('Connection: keep-alive\r\n\r\n')
        msg = ''.join(msg)

        self.move_socket.send(msg)

	# Get the return message
        print 'Wait for HTML return msg'
        data = ''
        while len(data) == 0:
            data = self.move_socket.recv(self.max_tcp_cmd_buffer)
        print data

	# We have to close the socket and open it again
        self.disconnect_rover()
        self.connect_rover()

        # send MO_O commands
        for i in range(1,4)
            self.writ_cmd(i,0)
            data = ''
            while len(data) == 0:
                data = self.move_socket.recv(self.max_tcp_cmd_buffer)
            print data            

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
            data = self.move_socket.recv(self.max_tcp_cmd_buffer)
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
            data = self.move_socket.recv(self.max_tcp_cmd_buffer)
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
            data = self.move_socket.recv(self.max_tcp_cmd_buffer)
		#print list(data)
        self.final_data = data

    def connect_rover(self):	
        self.move_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.move_socket.connect((self.host, self.port))
        self.move_socket.setblocking(1)

    def disconnect_rover(self):
        self.move_socket.close()

    def return_data(self):
        return self.final_data

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
		
        packet_len = 0
        if index == 1:
            packet_len = 22
        elif index == 2:
            packet_len = 48
        elif index == 3:
            packet_len = 23
        elif index == 5:
            packet_len = 24
        elif index == 6:
            packet_len = 24
        elif index == 7:
            packet_len = 24
        elif index == 8:
            packet_len = 24
        elif index == 9:
            packet_len = 22
        elif index == 10:
            packet_len = 23
        elif index == 11:
            packet_len = 23
        elif index == 12:
            packet_len = 24
        elif index == 13:
            packet_len = 24

        cmd_buffer = array.array('c')
        cmd_buffer.extend(['M', 'O', '_', 'O'])
        for i in range(4, packet_len+1):	
            cmd_buffer.append('\0')

        if index == 1:
            cmd_buffer[4] = '\x02'
        elif index == 2:
            cmd_buffer[4] = '\x02'
            cmd_buffer[15] = '\x1a'
            cmd_buffer[23] = 'A'
            cmd_buffer[24] = 'C'
            cmd_buffer[25] = '1'
            cmd_buffer[26] = '3'
            cmd_buffer[36] = 'A'
            cmd_buffer[37] = 'C'
            cmd_buffer[38] = '1'
            cmd_buffer[39] = '3'
        elif index == 3:
            cmd_buffer[4] = '\x04'
            cmd_buffer[15] = '\x01'
            cmd_buffer[19] = '\x01'
            cmd_buffer[23] = '\x02'
        elif index == 5:     # left wheel Forward
            cmd_buffer[4] = '\xfa'
            cmd_buffer[15] = '\x02'
            cmd_buffer[19] = '\x01'
            cmd_buffer[23] = '\x04'
            cmd_buffer[24] = '\x0a'
        elif index == 6:    # left wheel Backward
            cmd_buffer[4] = '\xfa'
            cmd_buffer[15] = '\x02'
            cmd_buffer[19] = '\x01'
            cmd_buffer[23] = '\x05'
            cmd_buffer[24] = '\x0a'
        elif index == 7:    # right wheel Forward
            cmd_buffer[4] = '\xfa'
            cmd_buffer[15] = '\x02'
            cmd_buffer[19] = '\x01'
            cmd_buffer[23] = '\x01'
            cmd_buffer[24] = '\x0a'
        elif index == 8:    # right whell backward
            cmd_buffer[4] = '\xfa'
            cmd_buffer[15] = '\x02'
            cmd_buffer[19] = '\x01'
            cmd_buffer[23] = '\x02'
            cmd_buffer[24] = '\x0a'
        elif index == 9:    # IR off(?)
            cmd_buffer[4] = '\xff'
        elif index == 10:   # switches infrared LED on
            cmd_buffer[4] = '\x0e'
            cmd_buffer[15] = '\x01'
            cmd_buffer[19] = '\x01'
            cmd_buffer[23] = '\x5e'
        elif index == 11:   # switches infrared LED off
            cmd_buffer[4] = '\x0e'
            cmd_buffer[15] = '\x01'
            cmd_buffer[19] = '\x01'
            cmd_buffer[23] = '\x5f'
        elif index == 12:   # stop left track
            cmd_buffer[4] = '\xfa'
            cmd_buffer[15] = '\x02'
            cmd_buffer[19] = '\x01'
            cmd_buffer[23] = '\x02'
            cmd_buffer[24] = '\x00'
        elif index == 13:  # stop right track
            cmd_buffer[4] = '\xfa'
            cmd_buffer[15] = '\x02'
            cmd_buffer[19] = '\x01'
            cmd_buffer[23] = '\x04'
            cmd_buffer[24] = '\x00'
        msg = cmd_buffer.tostring()
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
        rover_video = br_cam.RovCam(rover.return_data())
        distance = 0.5    # feet
        speed = 1         # foot/sec
        while not rospy.is_shutdown(): 
            str = "robot moves %s" % rospy.get_time()
            rospy.loginfo(str)
            pub.publish(String(str))
            rover.move_forward(distance, speed)
            #rover_video.display_image()
            rospy.sleep(0.1)
#           counter = counter + 1

        rover.disconnect_rover()
    except rospy.ROSInterruptException:
        pass
