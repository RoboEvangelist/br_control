#!/usr/bin/env python
'''
Client specifically for controlling several rovers
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

class KeyboardInterface():
    def __init__(self, server_uri, update_image):

        self.__has_control = True

    def hasControl(self):
        '''
        Return True if user wants to send control commands with
        keyboard.
        Tab key and shift-tab toggle this.
        '''
        # Check if control flag should be toggled.
        import pygame
        if pygame.key.get_pressed()[pygame.K_TAB]:
            self.__has_control = not (pygame.key.get_mods() &
                                    pygame.KMOD_LSHIFT)

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
        self._started = False     # true if client connected
        self._client = None       # server client object

        # original image size (from server)
        self._im_width = 320.0
        self._im_height = 240.0

        # variables for publishing movement
        self._pub = rospy.Publisher('move', String)
        rospy.init_node('br_gui')
        self._im_string = ''      # image string

    def get_image_data(self, image_string):
        '''
        obtains the published image data
        '''
        self._im_string = image_string

    def call_stop_track(self, *args):
        '''
        publishes the stop command to stop a robot robot
        '''
        try:
            self._pub.publish(String('stop'))
            Logger.info('stop')
        except rospy.ServiceException, e:
            print "Stop Tracks Service call failed: %s"%e

    def call_move_forward(self, *args):
        '''
        calls the move forward service to move robot forward
        '''
        try:
            self._pub.publish(String('forward'))
            Logger.info('forward')
        except rospy.ServiceException, e:
            print "Move forward Service call failed: %s"%e

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
                    # use double quote for subscriber name
                    rospy.Subscriber("image", String,
                                        self.get_image_data)
                    from threading import Thread
                    spin_thread = Thread(target=lambda: rospy.spin())
                    spin_thread.start()
#                    rospy.spin()
                    break
                except socket.error:
                    count += 1
                    import time
                    time.sleep(.1)

                if count > 100:
                    waiting = 'Waiting for meta server at %s'
                    uri="http://" + hostname + ":12345"
                    Logger.info(waiting, uri)

    def display_raw_image(self, dt):
        '''
        Display the normal image coming straight from the rover
        '''
        try:
            print('testing')
            print(self._im_string)
            
#            self._client.processClients() # get all pygame events
            # assum size of all incoming images is 320x240
#            im_size = self._client.getImageSize()
#            retrieve = self._client.retrieveImage()
#            # convert pygame surface to Kivy data
#            buf = tostring(retrieve, 'RGB', True)
            imdata = ImageData(self._im_width, self._im_height,
                               'rgb', self._im_string)
            tex = Texture.create_from_data(imdata)

            # calculate new image size
            aspect_ratio = self._ori_im_height / self._ori_im_width
            w = 3.0*self.width/4.0      # desired width
            h = aspect_ratio * w        # desired height
#
            # image's origin starts from buttom left
            (pos_x, pos_y) = (self.center_x/4, self.center_y/4)

            # transform image's bottom origin to the top left
            # which agrees with the mouse's origin
            x_0 = pos_x
            y_0 = self.height - (h + pos_y)
            im_translation = []
            im_translation.append(x_0)
            im_translation.append(y_0)

            # size difference ratio between GUI window and picture
            im_translation.append(self.width/w)    # x ratio
            im_translation.append(self.height/h)   # y ratio
#            self._client.setMouseRatio(im_translation)
#            self.canvas.clear()   # clear to upate canvas
            with self.canvas:     #display image
                Rectangle(texture=tex,
                      pos= (pos_x, pos_y),
                      size=(w, h))
        except BaseException:
            Logger.warning('Error gettin image frame')
            pass
    #        self.stop_connection()

    def stop_connection(self):
#        self._client.quit()
        from sys import exit
        exit()

    # create threads down here

    def schedule_stop_track(self, *args):
        '''
        calls the stop track on a loop
        '''
        trigger = Clock.create_trigger(self.call_stop_track)
        # later
        trigger()

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
        trigger = Clock.create_trigger(self.start_server)
        # later
        trigger()
        # schedule image display thread
        Clock.schedule_interval(self.display_raw_image, 1.0 / 25.0)

class KivyGui(App):
    def build(self):
        return ControlClass()

if __name__ == '__main__':
    KivyGui().run()
