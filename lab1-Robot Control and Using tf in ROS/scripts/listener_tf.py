#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
from geometry_msgs.msg import Twist

if __name__ == '__main__':
    rospy.init_node('listener')

    listener = tf.TransformListener()

    robot_vel = rospy.Publisher('robot_1/cmd_vel', Twist,queue_size=1)

    rate = rospy.Rate(10.0)
    listener.waitForTransform("/robot_1", "/robot_0", rospy.Time(), rospy.Duration(4.0))
    rospy.sleep(rospy.Duration(1.0))
    while not rospy.is_shutdown():
        try:
            now = rospy.Time.now() 
	        past = now - rospy.Duration(1.0)
	        listener.waitForTransformFull('/robot_1', now, '/robot_0', past, "/world", rospy.Duration(1.0))
            (trans,rot) = listener.lookupTransformFull('/robot_1', now, '/robot_0', past, "/world")

        except (tf.LookupException, tf.ConnectivityException, tf.Exception):
            continue

        angular = 4 * math.atan2(trans[1], trans[0])
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        cmd = Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        robot_vel.publish(cmd)

        rate.sleep()

