#!/usr/bin/env python
'''
This files runs indefinitelly  in a computer and waits for a client
to request connection to a/the robot(s)
'''

from SimpleXMLRPCServer import SimpleXMLRPCServer
import subprocess
from time import sleep


START_ROS_ROVER = []    # stores roscor and rover program

def startProcess():
    '''
    This function starts roscore and the rovers software.
    The function is called when a client connects to the meta-server
    '''
    # commands to start roscore and the rovers ROS program
#    roscore_cmd = ['roscore']
    from tempfile import NamedTemporaryFile
    address_file = NamedTemporaryFile(delete=False)
    # pass temp file name as argument to br_swarm_rover
    uri_file = address_file.name
    # TODO: run this in a loop start a node per robot available
    # Another argument of br_cmd shall be the NIC network name
    br_cmd = ['rosrun', 'br_swarm_rover', 'br_single_control.py',
                uri_file]
    from threading import Thread
#    roscore_thread = Thread(target=lambda: START_ROS_ROVER.append(
#        subprocess.Popen(roscore_cmd)))
#    roscore_thread.start()
    rover_started = False    # true if rover program started
    sleep(3)
    while not rover_started:
        try:
            rover_thread = \
                Thread(target=lambda: START_ROS_ROVER.append(
                    subprocess.Popen(br_cmd)))
            rover_thread.start()
            rover_started = True
        except BaseException:
            print('trying to connect to rover(s)')
            pass
#    address_file = open(uri_file, 'r+b')
    line = None
    while not line:
        address_file.seek(0)
        line =  address_file.readline()
    return line       #threads

def getServerAddress(file_name):
    '''
    Meta-server calls this function when when requesting
    ROS server's address
    '''
    import tempfile
    tempfile.name

if __name__ == '__main__':
    threads = START_ROS_ROVER
    thread_started = False
    server = SimpleXMLRPCServer(("0.0.0.0", 12345))
    server.register_function(startProcess, "startProcess")
    while True:
        try:
            if not thread_started:
                print('\nwaiting for a client to connect...\n\n')
                server.handle_request() 
                thread_started = True
        except BaseException:
            print('exiting ROS program')
            for thread in threads:
                thread.kill()
            from sys import exit
            exit()
