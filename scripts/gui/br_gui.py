#!/usr/bin/env python
'''
Client specifically for controller several rovers
'''

import kivy
kivy.require('1.7.1')

import roslib; roslib.load_manifest('br_swarm_rover')
import rospy 
from std_msgs.msg import String

#from os.path import join, dirname
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.image import ImageData
from kivy.graphics.texture import Texture
from kivy.logger import Logger

# FIXME this shouldn't be necessary
from kivy.base import EventLoop
EventLoop.ensure_window()
#from kivy.core.window import Window

# maybe not necessary
from pygame.image import tostring

class KeyboardInterface():
    def __init__(self, server_uri, update_image):

        self.__has_control = True

    def hasControl(self):
        '''Return True if user wants to send control commands with
        keyboard.
        Tab key and shift-tab toggle this.
        '''
        # Check if control flag should be toggled.
        import pygame
        if pygame.key.get_pressed()[pygame.K_TAB]:
            self.__has_control = not (pygame.key.get_mods() & pygame.KMOD_LSHIFT)

            if self.__has_control:
                print('Take control')
            else:
                print('Release control')

        return self.__has_control

class ControlClass(FloatLayout):
    def __init__(self, **kwargs):
        '''
        We use __init__ mainly because _args cannot be initialized
        to an ObjectProperty for some reason, so we gotta initialize
        it this way
        '''
        super(ControlClass, self).__init__(**kwargs)
#        self._args = self.parser_arguments()
        self._started = False     # true if client connected
        self._client = None       # server client object

        # original image size (from server)
        self._ori_im_width = 1280.0
        self._ori_im_height = 720.0

        # variables for publishing movement
        self._rospy = rospy
        self._pub = self._rospy.Publisher('move', String)
        self._rospy.init_node('client')
#        from threading import Thread
#        roscore_thread = \
#            Thread(target=lambda: self._rospy.init_node('client'))
#        roscore_thread.start()

    def call_stop_track(self, *args):
        '''
        calls tllhe move forward service to move robot forward
        '''
        try:
            self._pub.publish(String('stop'))
            Logger.info('stop')
        except rospy.ServiceException, e:
            print "Stop Tracks Service call failed: %s"%e

    def schedule_stop_track(self, *args):
        '''
        calls the move forward on a loop
        '''
        trigger = Clock.create_trigger(self.call_stop_track)
        # later
        trigger()

    def call_move_forward(self, *args):
        '''
        calls the move forward service to move robot forward
        '''
        try:
            self._pub.publish(String('forward'))
            Logger.info('forward')
        except rospy.ServiceException, e:
            print "Move forward Service call failed: %s"%e

    def schedule_move_forward(self, *args):
        '''
        calls the move forward on a loop
        '''
        # this function only when button is pressed
        trigger = Clock.create_trigger(self.call_move_forward)
        # later
        trigger()

    def schedule_client(self, *args):
        '''
        starts the thead to to run the server simulation
        '''
#        Clock.schedule_interval(self.start_server, 1.0 / 25.0)
        trigger = Clock.create_trigger(self.start_server)
        # later
        trigger()


    def start_server(self, dt):
        '''
        initializes the client connection, and gets image data
        '''
        hostname = "0.0.0.0"
        # Keep trying in case server is not up yet
        if not self._started:
            count = 0
            while True:
                import socket
                try:
                    from xmlrpclib import ServerProxy
                    # connect to meta server first
                    prox = \
                        ServerProxy("http://" + hostname + ":12345")
                    # get servers address from the meta server
                    ros_uri = prox.startProcess()
                    Logger.info('Server Address\n <%s>', ros_uri)
#                    self._client = \
#                    KeyboardInterface(ros_uri,
#                    self._args.image_updates)
                    self._started = True
                    Logger.info('Client Connected...')
                    break
                except socket.error:
                    count += 1
                    import time
                    time.sleep(.1)

                if count > 100:
                    waiting = 'Waiting for meta server at %s'
                    uri="http://" + hostname + ":12345"
                    Logger.info(waiting, uri)
        try:
            print('testing')
#            self._client.processClients() # get all pygame events
            # TODO: get image string data from br_cam.py
            # size of all incoming images
#            im_size = self._client.getImageSize()
#            retrieve = self._client.retrieveImage()
#            # convert pygame surface to Kivy data
#            buf = tostring(retrieve, 'RGB', True)
#            imdata = ImageData(im_size[0], im_size[1],
#                               'rgb', buf)
#            tex = Texture.create_from_data(imdata)
#
#            # calculate new image size
#            aspect_ratio = self._ori_im_height / self._ori_im_width
#            w = 3.0*self.width/4.0      # desired width
#            h = aspect_ratio * w        # desired height
#
#            # image's origin starts from buttom left
#            (pos_x, pos_y) = (self.center_x/4, self.center_y/4)
#
#            # transform image's bottom origin to the top left
#            # which agrees with the mouse's origin
#            x_0 = pos_x
#            y_0 = self.height - (h + pos_y)
#            im_translation = []
#            im_translation.append(x_0)
#            im_translation.append(y_0)
#
#            # size difference ratio between GUI window and picture
#            im_translation.append(self.width/w)    # x ratio
#            im_translation.append(self.height/h)   # y ratio
#            self._client.setMouseRatio(im_translation)
#            self.canvas.clear()   # clear to upate canvas
#            with self.canvas:     #display image
#                Rectangle(texture=tex,
#                      pos= (pos_x, pos_y),
#                      size=(w, h))
        except BaseException:
            Logger.warning('closing simulation connection')
            self.stop_connection()

    def stop_connection(self):
#        self._client.quit()
        from sys import exit
        exit()

class KivyGui(App):
    def build(self):
        return ControlClass()

if __name__ == '__main__':
    KivyGui().run()
