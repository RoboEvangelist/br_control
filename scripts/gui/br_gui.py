#!/usr/bin/env python
'''
Client specifically for controlling several rovers and gather data
from the rovers
'''

import kivy
kivy.require('1.7.1')

import roslib; roslib.load_manifest('br_swarm_rover')
import rospy 
from std_msgs.msg import String

import StringIO

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.core.image.img_pygame import ImageLoaderPygame

# FIXME this shouldn't be necessary
from kivy.base import EventLoop
EventLoop.ensure_window()

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

    def call_move_backward(self, *args):
        '''
        calls the move backward service to move
        '''
        try:
            self._pub.publish(String('backward'))
            Logger.info('backward')
        except rospy.ServiceException, e:
            print "Move backward Service call failed: %s"%e

    def call_turn_left(self, *args):
        '''
        calls the turn left service to move robot
        '''
        try:
            self._pub.publish(String('turn left'))
            Logger.info('turn left')
        except rospy.ServiceException, e:
            print "Move turn left Service call failed: %s"%e

    def call_turn_right(self, *args):
        '''
        calls the turn right service to move
        '''
        try:
            self._pub.publish(String('turn right'))
            Logger.info('turn right')
        except rospy.ServiceException, e:
            print "Move turn right Service call failed: %s"%e

    def call_left_forward(self, *args):
        '''
        calls the turn left forward service to move
        '''
        try:
            self._pub.publish(String('left forward'))
            Logger.info('left forward')
        except rospy.ServiceException, e:
            print "Move left forward Service call failed: %s"%e

    def call_right_forward(self, *args):
        '''
        calls the turn right forward service to move
        '''
        try:
            self._pub.publish(String('right forward'))
            Logger.info('right forward')
        except rospy.ServiceException, e:
            print "Move right forward Service call failed: %s"%e

    def call_left_backward(self, *args):
        '''
        calls the turn left backward service to move
        '''
        try:
            self._pub.publish(String('left backward'))
            Logger.info('left backward')
        except rospy.ServiceException, e:
            print "Move left backward Service call failed: %s"%e

    def call_right_backward(self, *args):
        '''
        calls the turn right backward service to move
        '''
        try:
            self._pub.publish(String('right backward'))
            Logger.info('right backward')
        except rospy.ServiceException, e:
            print "Move right backward Service call failed: %s"%e

    def start_server(self, dt):
        '''
        initializes the client connection, and gets image data
        '''
        hostname = "0.0.0.0"
        if not self._started:
            count = 0
            while True:  # Keep trying in case server is not up yet
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
            # assum size of all incoming images is 320x240
#            import pdb; pdb.set_trace()
            # get published image str and store it in a buffer
            buff = StringIO.StringIO()
            buff.write(self._im_string.data)
            buff.seek(0)
            # open buffer file and extract image texture
            imdata = ImageLoaderPygame(buff).texture
            size = (320, 240)
#            # calculate new image size
            aspect_ratio = size[0] / size[1]
            w = self.width/3.0      # desired width
            h = aspect_ratio * w        # desired height

#            # image's origin starts from buttom left
            (pos_x, pos_y) = (self.center_x/4, self.center_y/4)
            
            # use this part to implement mouse clicking
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
##            self._client.setMouseRatio(im_translation)
            # TODO: create a canvas just for the image and 
            # clear only that canvas
#            self.canvas.clear() 
            with self.canvas:     #display image
                Rectangle(texture = imdata, pos= (pos_x, pos_y),
                                      size=(w, h))
        except BaseException:
            Logger.warning('Error getting image frame')
            pass
    #        self.stop_connection()

    def stop_connection(self):
#        self._client.quit()
        from sys import exit
        exit()

    # create threads down here

    def schedule_client(self, *args):
        '''
        starts the thead to to run the server simulation
        '''
        # called only when button is pressed
        trigger = Clock.create_trigger(self.start_server)
        # later
        trigger()
        # schedule image display thread
        Clock.schedule_interval(self.display_raw_image, 1.0 / 30.0)

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
        # this function is called only when button is pressed
        trigger = Clock.create_trigger(self.call_move_forward)
        # later
        trigger()

    def schedule_move_backward(self, *args):
        '''
        calls the move backward on a loop
        '''
        # this function only when button is pressed
        trigger = Clock.create_trigger(self.call_move_backward)
        # later
        trigger()

    def schedule_turn_left(self, *args):
        '''
        calls the turn left on a loop
        '''
        # this function is called only when button is pressed
        trigger = Clock.create_trigger(self.call_turn_left)
        # later
        trigger()

    def schedule_turn_right(self, *args):
        '''
        calls the turn left on a loop
        '''
        # this function is called only when button is pressed
        trigger = Clock.create_trigger(self.call_turn_right)
        # later
        trigger()

    def schedule_left_forward(self, *args):
        '''
        calls the left forward on a loop
        '''
        # this function is called only when button is pressed
        trigger = Clock.create_trigger(self.call_left_forward)
        # later
        trigger()

    def schedule_right_forward(self, *args):
        '''
        calls the right forward on a loop
        '''
        # this function is called only when button is pressed
        trigger = Clock.create_trigger(self.call_right_forward)
        # later
        trigger()

    def schedule_left_backward(self, *args):
        '''
        calls the left backward on a loop
        '''
        # this function is called only when button is pressed
        trigger = Clock.create_trigger(self.call_left_backward)
        # later
        trigger()

    def schedule_right_backward(self, *args):
        '''
        calls the right backward on a loop
        '''
        # this function is called only when button is pressed
        trigger = Clock.create_trigger(self.call_right_backward)
        # later
        trigger()

class KivyGui(App):
    try:
        def build(self):
            return ControlClass()
    except BaseException:
        from sys import exit
        exit()

if __name__ == '__main__':
    KivyGui().run()
