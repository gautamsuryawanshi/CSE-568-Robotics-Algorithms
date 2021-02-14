#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import random
import math
from sensor_msgs.msg import PointCloud2 as pc2
from laser_geometry import LaserProjection
import numpy as np
import random


def ransac_func(points):
    iteration_count = 30
    threshold = 0.4
    pointCheck = []
    finalpoint = [0,0,0,0,0,[]]

    for i in range(iteration_count):
        if(len(points) < 1):
            break
        
        p1 = points[random.randrange(0,len(points))]
        p2 = points[random.randrange(0,len(points))]

        x1 = p1[0]
        y1 = p1[1]

        x2 = p2[0]
        y2 = p2[1]

        
        inlier_count = 0

        inlier_points = []

        for p in points:
            cx = p[0]
            cy = p[1]
            
            d1 = abs(((y2-y1)*cx) - ((x2-x1)*cy) + ((x2*y1) - (y2*x1)))
            d2 = math.sqrt(((y2-y1)**2) + ((x2-x1)**2))

            if(d2 != 0):
                distance =  d1/d2 
                
                if(distance < threshold):
                    inlier_points.append([cx,cy])
                    inlier_count += 1

        pointCheck.append([x1,y1,x2,y2,inlier_count,inlier_points]) 
        
        
        for pc in pointCheck:
            if(finalpoint[4] < pc[4]):
                finalpoint = pc
                
            

    point1 = Point(finalpoint[0],finalpoint[1],0)
    point2 = Point(finalpoint[2],finalpoint[3],0)

    return point1,point2,finalpoint[5]





def cartesian_coords_func(data):
    angle = data.angle_min
    ang_inc =  data.angle_increment
    
    pointss = []


    for r in data.ranges:
        if(r < 2.5):
            x = r*math.cos(angle)
            y = r*math.sin(angle)
            pointss.append([x,y])
        angle +=ang_inc

    totalPoints = []
    for i in range(3):
        a,b,c = ransac_func(pointss)
        for r1 in c:
            if(r1 in pointss):
                pointss.remove(r1)
    
        totalPoints.append(a)
        totalPoints.append(b)

    markLine(totalPoints)
    
    '''
    <node pkg="lab2" type="evader.py" name="scan_values1" output="screen" />
    
    '''

    
   

   


def markLine(allPoints):
    marker = Marker()
    marker.header.frame_id = '/base_link'
    marker.header.stamp = rospy.Time.now()
    #marker.pose.orientation.w = 1.0
    marker.type = marker.LINE_LIST
    marker.action = marker.ADD
    marker.lifetime = rospy.Duration(1)

    marker.scale.x = 0.1
    marker.scale.y = 0.1
    #marker.scale.z = 0

    marker.color.a = 1.0
    marker.color.b = 1.0
    
    for p in allPoints:
        if(p.x != 0 and p.y != 0):
            marker.points.append(p)


    pub.publish(marker)

    
    

def laser_callback(data):
    cartesian_coords_func(data)
    

	


if __name__ =='__main__':
    rospy.init_node('new')
    sub = rospy.Subscriber('/base_scan' , LaserScan , laser_callback)
    pub = rospy.Publisher('/perception', Marker ,queue_size=1)
    rospy.spin()


    
    

