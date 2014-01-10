#!/usr/bin/env python
'''
This is the main file that the meta-server calls when you want you
run just one robot at the time
'''

import roslib; roslib.load_manifest('br_swarm_rover')
import rospy
from sensor_msgs.msg import CompressedImage
from sensor_msgs.msg import Image
from std_msgs.msg import String

import br_cam
from br_control import RovCon

#from time import sleep

# meta_server.py creates the file where ROS shall write its network
# address, then the address is passed as an argument here
# TODO: may be able to do something directly like:
# python fibo.py <arguments> (on command line)
# import sys  (inside script)
#    fib(int(sys.argv[1]))
# to enter argument instead of using argparser
import argparse
parser = argparse.ArgumentParser('br_single_control')
parser.add_argument('file', type=str, default=None,
                    help='temporary file to store server uri')
parser.add_argument('robot_address', type=str, default=None,
                    help='address of NICs connect to robots')
arg = parser.parse_args()

if __name__ == '__main__':
    try:
        #TODO: change the local host part to a normal address
        # for now the wanted address is exported manually in the
        # .bashrc file

        # initiate rover connection and video streaming
        rover = RovCon(arg.robot_address) 
        rover_video = br_cam.RovCam(rover.return_data())

        # publish robot camera data
        pub = rospy.Publisher('/output/image_raw/compressed'+ 
                arg.robot_address.split('.')[3], CompressedImage)
        rospy.init_node('robot'+arg.robot_address.split('.')[3])
#        distance = 0.5    # feet
#        speed = 1         # foot/sec
        # obtain published move command
        #TODO: also obtain speed and distance
        rospy.Subscriber("move", String, rover.set_move)

        # thread to run the subscriber
        from threading import Thread
        spin_thread = Thread(target=lambda: rospy.spin())
        spin_thread.start()

        while not rospy.is_shutdown(): 
            buf = rover_video.receive_image()
            pub.publish(buf)    # publish CompressedImage
            rospy.sleep(0.033)  # manually given image frame rate

    except rospy.ROSInterruptException:
        rover.disconnect_rover()
        rover_video.disconnect_video()
#        pass
        from sys import exit
        exit()
