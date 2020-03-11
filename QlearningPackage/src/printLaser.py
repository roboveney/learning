#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import LaserScan
#import pandas as pd
    

class laser:
    
    def callback(self, data):
        self.laser = data.ranges
        return
    
    def __init__(self):
        rospy.init_node("RL_robot", anonymous=True)
        self.vel_pub = rospy.Publisher("/triton_lidar/vel_cmd", Pose2D, queue_size=2)
        self.laser_sub = rospy.Subscriber('/scan', LaserScan, self.callback)
        #rospy.spin()
        rospy.Rate(2) # 10hz
        return


if __name__ == '__main__':
    x = laser()
    check = x.callback
    print(check)
    
    rospy.spin()