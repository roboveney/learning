#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import LaserScan
import math
import pandas as pd

class Object(object):
    pass

#Global Variables
scan_data = None
bot = Object()
roaming = True # boolean on if the robot is close enough to follow a wall


def callback(data):
    global scan_data
    scan_data = data
    
def updateScan(sides):
    sides['Right'] = round(min(scan_data.ranges[45:75]),3)
    sides['RightFront'] = round(min(scan_data.ranges[15:45]),3)
    sides['Front'] = round(min((scan_data.ranges[0:15] + scan_data.ranges[345:360])),3)
    sides['Left'] = round(min(scan_data.ranges[255:285]),3)
    bot.minDis = min(sides.values())
    bot.state = [key for key in sides if sides[key] == bot.minDis]
    
def findWall(sides):
    global bot
    global roaming
    #print("The closest side is ", minSide)
    #print("Min dis: ", minDis)
    if bot.minDis >= 0.5:
        if bot.state == ['Front']:
            bot.pose.x = 0.1
            #print("moving towards Front", bot.x)
        if bot.state == ['Left']:
            bot.pose.y = 0.1
            #print("moving towards Left", bot.y)
        if bot.state == ['Right']:
            bot.pose.y = -0.1
            #print("moving towards Right", bot.y)
    else:
        bot.pose.x = 0
        bot.pose.y = 0
        a = 1
        roaming = False
        
def followWall(sides):
    turnRight(sides,10)
    turnLeft(sides,10)

def turnRight(sides, angle):
    global bot
    bot.pose.theta = 0
    bot.pose.x = 0    
    i = 0
    while i < 500:
        bot.pose.theta = angle
        bot.pose.y = 0.35
        bot.vel_pub.publish(bot.pose)
        print("Turning Right")
        i+=1
    bot.pose.theta = 0
    bot.pose.x = 0
    bot.vel_pub.publish(bot.pose)
    return 

def turnLeft(sides, angle):
    global bot
    bot.pose.theta = 0
    bot.pose.x = 0
    i = 0
    while i < 500:
        bot.pose.theta = angle
        bot.pose.x = 0.35
        bot.vel_pub.publish(bot.pose)
        print("Turning Left")
        i+=1
    bot.pose.theta = 0
    bot.pose.x = 0
    bot.vel_pub.publish(bot.pose)
    return

def Main():
    rospy.init_node("RL_robot", anonymous=True)
    bot.laser_sub = rospy.Subscriber('/scan', LaserScan, callback)
    bot.vel_pub = rospy.Publisher("/triton_lidar/vel_cmd", Pose2D, queue_size=2)
    
    bot.pose = Pose2D()  # pos x corresponds to front of robot and pos y is left
    sides = {'Right':0, 'RightFront':0, 'Front':0, 'Left':0}
    
    # Wait until the first scan is available.
    while scan_data is None and not rospy.is_shutdown():
        rospy.sleep(.1)

    #execute at 10hz.
    rate = rospy.Rate(10) 
    
    while not rospy.is_shutdown():
        
        while roaming == True:
            updateScan(sides)
            findWall(sides)
            bot.vel_pub.publish(bot.pose)
        
        while roaming == False:
            followWall(sides)
            print("sleep start")
            rospy.sleep(5)
            print("sleep finish")
        
        rate.sleep()
        
        
        
    
# This is how we usually call the main method in Python. 
if __name__ == "__main__":
    Main()