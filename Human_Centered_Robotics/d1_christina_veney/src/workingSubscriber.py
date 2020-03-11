#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import LaserScan
import pandas as pd

L = None
def callback(data):
    global L
    L = data

def check():
    rospy.init_node("RL_robot", anonymous=True)
    laser_sub = rospy.Subscriber('/scan', LaserScan, callback)
    
    # Wait until the first scan is available.
    while L is None and not rospy.is_shutdown():
        rospy.sleep(.1)
        
    # Rate object used to make the main loop execute at 10hz.
    rate = rospy.Rate(10) 
    
    while not rospy.is_shutdown():
        print(L.ranges[4])
        rate.sleep()
    
# This is how we usually call the main method in Python. 
if __name__ == "__main__":
    check()