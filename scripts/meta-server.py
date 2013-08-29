#!/usr/bin/env python
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import subprocess
from threading import Thread


START_ROS_ROVER = []    # stores roscor and rover program


class myThread (Thread):
    def __init__(self, cmd):
        Thread.__init__(self)
        self.cmd = cmd
        self.cmd_process = []
    def run(self):
        self.cmd_process.append(subprocess.Popen(self.cmd))

def getServerAddress():
    # commands to start roscore and the rovers ROS program
    roscore_cmd = ['roscore']
    br_cmd = ['rosrun', 'br_swarm_rover', 'br_control.py']
    roscore_thread = myThread(roscore_cmd)
    roscore_thread.start()
    rover_started = True    # true if rover program started
    while rover_started:
        try:
            print('before trying rover')
            rover_thread = myThread(br_cmd)
            rover_thread.start()
            rover_started = False
            print('after trying Rover program')
        except BaseException:
            print('trying to connect to rover(s)')
            pass

if __name__ == '__main__':
    try:
        getServerAddress() 
    except BaseException:
        print('exiting ROS program')
        from sys import exit
        exit()
