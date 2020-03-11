#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import LaserScan
import pandas as pd

def Locate(msg):
    R = min(msg.ranges[-90:-30])
    RF = min(msg.ranges[-60:-30])
    F = min(msg.ranges[-30:30])
    L = min(msg.ranges[30:90])
    return R, RF, F, L 

def rangeing(dis):
    if dis < 0.6:
        prox = 0 #close
        return prox
    elif 0.6 <= dis < 0.9:
        prox = 1 #medium
        return prox
    elif dis >= 0.9:
        prox = 2 #far
        return prox
    
def main(R,RF,F,L):    
    #establish ros node and publisher to velocity
    rospy.init_node("fwd", anonymous=True)
    sub = rospy.Subscriber('/scan', LaserScan, Locate)
    pub = rospy.Publisher("/triton_lidar/vel_cmd", Pose2D, queue_size=2)
    rate = rospy.Rate(2) # 10hz
    vel_msg = Pose2D()
    vel_msg.y = 0
    print(L)
    
#    Fprox = rangeing(F)
#    print(Fprox)
#    while Fprox == 2:
#        vel_msg.y = 0.1
#        pub.publish(vel_msg)
#        rangeing(F)
#        
#    
#    vel_msg.y = 0
#    vel_msg.x = 0.1    
#    rate.sleep()
    
    
#if __name__ == '__main__':
#    R = 0
#    RF = 0
#    F = 0
#    L = 0
#    main(R,RF,F,L)

    #update ros topics on main thread
    rospy.spin()
