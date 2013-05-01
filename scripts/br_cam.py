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
        self.image_ptr = 0;
        self.tcp_ptr = 0;
        self.image_start_position = 0
        self.image_length = 0
        self.image_buffer = array.array('c')
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
        ldata = array.array('c')
       # ldata = []
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
            print i 
        jpgfile.close()

        image = array.array('c')
        image = cv2.imread('test.jpg', 1)
        print type(image)
        image = image[:,-1::-1,:]
        image = image * 1
        cv2.imshow(u'Image', image)
        #time.sleep(1) 
        cv2.waitKey()
        #cv2.destroyWindow('test.jpg')



#     def receive_image:
#         len = 0
#         new_ptr = self.tcp_ptr;
#         imageLength = 0;
#         fnew = false;
# 
#         while (!fnew && new_ptr < self.max_image_buffer - self.max_tcp_cmd_buffer) 
#         {
#             len = self.video_socket.recv(self.max_tcp_cmd_buffer)
# 				# todo: check if this happens too often and exit
#         if (len <= 0) continue
# 
#         f4 = array.array('c')
# 				
# 				for (i = 0; i < 4; i++)
# 					f4[i] = self.image_buffer[new_ptr + i];
# 				
# 				if (ImgStart(f4) && (imageLength > 0))
# 					fnew = true;
# 				
# 				if (!fnew) # OLD IMAGE, SO WHAT THE SOCKET GOT WAS A CHUNK OF AN IMAGE
# 				{
# 					new_ptr += len;
# 					image_length = new_ptr - image_ptr;
# 				} 
# 				else #NEW IMAGE
# 				{
# 						
# 					SetImageStartPosition(image_ptr + 36);#PORB 36 ES LA CANTIDAD MAXIMA DE BYTES DE IMAGEN QUE LEES, CADA VEZ
# 														#O TAMBN PUEDE SER QUE AL SUMARLE 36 ELIMINAS EL ENCABEZADO DE LA IMG
# 					SetImageLength(imageLength - 36);
# 				
# 					if (new_ptr > maxImageBuffer / 2) 
# 					{
# 						# copy first chunk of new arrived image to start of
# 						# array
# 						for (int i = 0; i < len; i++)
# 							imageBuffer[i] = imageBuffer[new_ptr + i];
# 						image_ptr = 0;
# 						tcpPtr = len;	
# 						
# 					} else 
# 					{
# 						image_ptr = new_ptr;
# 						tcpPtr = new_ptr + len;
# 					}
# 					
# 				}#END ELSE
# 				
# 			}#END WHILE
# 					
# 			# reset if ptr runs out of boundaries
# 			if (new_ptr >= maxImageBuffer - maxTCPBuffer) {
# 				image_ptr = 0;
# 				tcpPtr = 0;
# 			}
# 			
# 		} catch (Exception eg) {
# 		 # Log.v("Comunicator ERROR", eg.toString());
# 		}	
# 	}
