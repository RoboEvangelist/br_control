#!/usr/bin/env python
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import subprocess


START_ROS_ROVER = []    # stores roscor and rover program


def getServerAddress():
    # commands to start roscore and the rovers ROS program
    roscore_cmd = ['roscore']
    br_cmd = ['rosrun', 'br_control.py']
    START_ROS_ROVER.append(subprocess.Popen(roscore_cmd))



if __name__ == '__main__':
    getServerAddress() 
