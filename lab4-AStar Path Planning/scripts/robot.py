#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2
import numpy as np

import astar as a



class Robot:
  def __init__(self,path):
    self.x = 0
    self.y = 0
    self.theta = 0
    self.path = path

    self.region1 = 0
    self.region2 = 0

    self.sub = rospy.Subscriber('/odom',Odometry,self.callback)
    self.pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 10)
    self.sub1 = rospy.Subscriber('/base_scan' , LaserScan , self.laser_callback)


  def laser_callback(self,data):
    ranges = data.ranges

    self.region1 = np.average(ranges[:180])
    self.region2 = np.average(ranges[180:])

  
  def callback(self,msg):
    self.x = msg.pose.pose.position.x
    self.y = msg.pose.pose.position.y


    ox = msg.pose.pose.orientation.x
    oy = msg.pose.pose.orientation.y
    oz = msg.pose.pose.orientation.z
    ow = msg.pose.pose.orientation.w

    (roll, pitch, self.theta) = euler_from_quaternion([ox, oy, oz, ow])



  def moveRobot(self):

    for i in self.path:
      x1 = i[0]
      y1 = i[1]

      print(x1,y1)

      if self.region2 < 1:
        y1 = y1 + y1 * 0.4
      
      if self.region1 < 0.75:
        x1 = x1 + x1 * 0.25

    

      print(x1,y1,self.region1,self.region2)

      goal = Point()
      goal.x = x1
      goal.y = y1

      speed = Twist()
      while True:
      
        inc_x = goal.x - self.x
        inc_y = goal.y - self.y

        angle_to_goal = atan2(inc_y, inc_x)
        ang_diff = angle_to_goal - self.theta
      
        distance = np.sqrt((x1-self.x)*(x1-self.x) + (y1-self.y)*(y1-self.y))

        if distance < 0.1:
          print("Reached Mini Goal",x1,y1)
          print("***********")
          break;

        if abs(ang_diff) < 0.1:
          speed.linear.x = 0.5
        else:
          speed.linear.x = 0.0
          speed.angular.z =  ang_diff
        
        self.pub.publish(speed)





if __name__ == '__main__':
  rospy.init_node("speed_controller")
  path = a.givePath()


  r =  Robot(path)
  r.moveRobot()
  
  rospy.spin()













    
































