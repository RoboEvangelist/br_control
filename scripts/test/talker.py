#!/usr/bin/env python
import roslib; roslib.load_manifest('br_swarm_rover')
import rospy
from std_msgs.msg import String


def talker():
    pub = rospy.Publisher('chatter', String)
    rospy.init_node('talker')
    while not rospy.is_shutdown():
        stri = "hello world %s" % rospy.get_time()
        rospy.loginfo(stri)
        pub.publish(String(stri))
        rospy.sleep(1.0)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
