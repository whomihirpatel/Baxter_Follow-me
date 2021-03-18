#!/usr/bin/env python3

import rospy
from collections import deque
from imutils.video import VideoStream
import pyrealsense2 as rs
import numpy as np
import cv2
import argparse
import time
import imutils
from geometry_msgs.msg import Point
import time



def listener():
    global x_wpoint, y_wpoint, z_wpoint, msg_Point

    x_waypoints = []
    y_waypoints = []
    z_waypoints = []

    rospy.init_node('cv_to_waypoint', anonymous=True)
    sub = rospy.Subscriber('world_coord', Point, go_pointCallback)

    i = 0
    while True:
        x_waypoints.append(x_wpoint)
        y_waypoints.append(y_wpoint)
        z_waypoints.append(z_wpoint)

        time.sleep(0.5) #delay callback by 0.5s so we don't collect all waypoints being published from CV node

        if (len(x_waypoints) > 1):
            delta = x_waypoints[i] - x_waypoints[i-1]
        if (delta <= 0.001):
            print("target object is stationary\r\n")
            print("store waypoint into ros params\r\n")

            rospy.set_param('x_waypoints', x_waypoints)
            rospy.set_param('y_waypoints', y_waypoints)
            rospy.set_param('z_waypoints', z_waypoints)
            
            break
        

def go_pointCallback(msg_Point):
    global x_wpoint, y_wpoint, z_wpoint, msg_Point
    x_wpoint = msg_Point.x
    y_wpoint = msg_Point.y
    z_wpoint = msg_Point.z
   

if __name__ == '__main__':
    listener()
    