#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np
import random


def stop():
     vel_msg = Twist()
     vel_msg.linear.x = 0.0
     pub.publish(vel_msg)


def moveRight():
    vel_msg = Twist()
    vel_msg.angular.z = -0.7
    pub.publish(vel_msg)

def moveLeft():
    vel_msg = Twist()
    vel_msg.angular.z = 0.7
    pub.publish(vel_msg)  


def moveBackward():
    vel_msg = Twist()
    vel_msg.linear.x = -2
    pub.publish(vel_msg) 


def completeLeft():
    vel_msg = Twist()
    vel_msg.angular.z = 1
    pub.publish(vel_msg) 


def completeRight():
    vel_msg = Twist()
    vel_msg.angular.z = -1
    pub.publish(vel_msg) 




def keepMoving():
     vel_msg = Twist()
     vel_msg.linear.x = 2.0
     pub.publish(vel_msg)


    

def callback(msg):
    ranges = msg.ranges
    r1 = np.average(ranges[:90])
    r2 = np.average(ranges[90:180])
    r3 = np.average(ranges[180:270])
    r4 = np.average(ranges[270:])

    h1 = np.average(ranges[:180])
    h2 = np.average(ranges[180:])

    #print("r1 :" + str(r1) +" r2 :" + str(r2) + " r3 :" + str(r3) + " r4 :" + str(r4) +  " h1 :" + str(h1) + " h2 :" + str(h2))


    if( h1 < 2 and h2 < 2):
        stop()
        moveBackward()
    
    elif( r1 < 2 ):
        moveBackward()
        completeLeft()
    
    elif( r4 < 1.7):
        moveBackward()
        completeRight()

    elif( r2 < 2 and r3 < 2):
        r = random.random()
        print("Random : ",r)
        if( r < 0.5):
            moveBackward()
            completeLeft()
        else:
            moveBackward()
            completeRight()

    elif( h1 < 2.5 ):
        stop()
        moveBackward()
        moveLeft()
    
    elif( h2 < 2.5 ):
        stop()
        moveBackward()
        moveRight()

    else:
        keepMoving()

    



 
rospy.init_node('scan_values1')
sub = rospy.Subscriber('/base_scan', LaserScan, callback)
pub = rospy.Publisher('/cmd_vel',Twist,queue_size=1)
rospy.spin()
    