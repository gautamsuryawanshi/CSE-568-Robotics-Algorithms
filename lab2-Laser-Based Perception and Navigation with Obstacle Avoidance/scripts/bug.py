#! /usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
import random
import math
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
from visualization_msgs.msg import Marker
import numpy as np


x = 0.0
y = 0.0 
theta = 0.0

wallFollow = False


def callback(msg):
   

    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y


    ox = msg.pose.pose.orientation.x
    oy = msg.pose.pose.orientation.y
    oz = msg.pose.pose.orientation.z
    ow = msg.pose.pose.orientation.w

    (roll, pitch, theta) = euler_from_quaternion([ox, oy, oz, ow])


def takeLeft():
    vel_msg = Twist()
    vel_msg.linear.x = 0.0
    vel_msg.angular.z = 0.5
    pub.publish(vel_msg) 

def takeRight():
    vel_msg = Twist()
    vel_msg.angular.z = -1
    pub.publish(vel_msg) 

def moveStraight():
    vel_msg = Twist()
    vel_msg.linear.x =  1
    pub.publish(vel_msg) 


def checkPositionOnLine():
    check = (11*x) - (12.5*y) + 63
    print("Position on Line",check)
    if( (check < 2) and (check > -2)):
        return True
    else:
        return False

def checkOrientedTowardsGoal():
    goal = Point()
    goal.x = 4.5
    goal.y = 9.0

    inc_x = goal.x - x
    inc_y = goal.y - y

    angle_to_goal = atan2(inc_y, inc_x)
    ang_diff = angle_to_goal - theta

    if(abs(ang_diff) > 0.1):
        return False
    else:
        return True


def orientTowardsGoal():
    goal = Point()
    
    goal.x = 4.5
    goal.y = 9.0

    inc_x = goal.x - x
    inc_y = goal.y - y

    angle_to_goal = atan2(inc_y, inc_x)
    ang_diff = angle_to_goal - theta


    if( abs(ang_diff) > 0.1 ):
        speed = Twist()
        speed.linear.x = 0.0
        speed.angular.z = ang_diff
        pub.publish(speed)




def laser_callback(msg):
   
    ranges = msg.ranges
    r1 = np.average(ranges[:90])
    r2 = np.average(ranges[90:180])
    r3 = np.average(ranges[180:270])
    r4 = np.average(ranges[270:])

    h1 = np.average(ranges[:180])
    h2 = np.average(ranges[180:])
    h3 = np.average(ranges[90:180])

    a = np.average(ranges[:])

    print("r1 :" + str(r1) +" r2 :" + str(r2) + " r3 :" + str(r3) + " r4 :" + str(r4) +  " h1 :" + str(h1) + " h2 :" + str(h2) + " a :" + str(a) )

    distance =  ( np.sqrt( np.square(x-4.5) + np.square(y-9) ))

    print("Distance :",distance)
    
    if(distance > 1):
        
        if((a<2.2) or (r3 < 1) or (r4 < 1)):
            global wallFollow
            #print("Wall Follow set to true")
            wallFollow = True
        else:
            #print("***")
            if(checkPositionOnLine()):
                #print("Wall Follow set to False")
                wallFollow = False
        
        
        if(not wallFollow):
            print("In Goal Follow")
            if(checkOrientedTowardsGoal()):
                moveStraight()
            else:
                orientTowardsGoal()
        




        if(wallFollow):
            print("In Wall Follow ")
            if(((h1<2) and (h2<2)) or (r3<1.5) ):
                takeRight()
            elif((h1 > 1) and (h2 > 2)):
                takeLeft()
            else:
                moveStraight()
    else:
        if(distance < 0.5):
            print("Goal Reached")
        else:
            if(checkOrientedTowardsGoal()):
                moveStraight()
            else:
                orientTowardsGoal()



     
        



rospy.init_node("speed_controller")
sub = rospy.Subscriber('/odom',Odometry,callback)
sub1 = rospy.Subscriber('/base_scan', LaserScan, laser_callback)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 10)
pub1 = rospy.Publisher('/perception', Marker ,queue_size=10)
rospy.spin()




        

