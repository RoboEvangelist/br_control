#!/usr/bin/env python
'''
This is the main file that the meta-server calls when you want you
run just one robot at the time
'''

import sys
sys.path.append('../')  # path to br_cam, etc.


import roslib; roslib.load_manifest('br_swarm_rover')
import rospy

import br_cam
from br_control import RovCon
from time import sleep

def input_speed(new_speed):
    while True:
        new_speed = raw_input('speed: ')
        new_speed = float(new_speed)
    

if __name__ == '__main__':
    try:
        # open file to save ROS server address
        # initiate rover connection and video streaming
        rover = RovCon() 
#        rover_video = br_cam.RovCam(rover.return_data())

        rospy.init_node('br_single_control')
#        distance = 0.5    # feet

        speed = 0.015
        i = 0
        while not rospy.is_shutdown(): 
            while i < 1/speed:
                rover.move_forward()
                rover.stop_tracks()
                sleep(speed) # manually given image frame rate
                i = i + 1
            i = 0
            speed = raw_input('speed: ')
            speed = float(speed)

    except rospy.ROSInterruptException:
        rover.disconnect_rover()
#        rover_video.disconnect_video()
#        pass
        from sys import exit
        exit()
