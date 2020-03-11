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
bot.roaming = True # boolean on if the robot is close enough to follow a wall


def callback(data):
    global scan_data
    scan_data = data
    
def updateScan(sides):
    sides['Right'] = round(min(scan_data.ranges[45:75]),3)
    sides['RightFront'] = round(min(scan_data.ranges[15:45]),3)
    sides['Front'] = round(min((scan_data.ranges[0:15] + scan_data.ranges[345:360])),3)
    sides['Left'] = round(min(scan_data.ranges[255:285]),3)
    overallMin = scan_data.range_min
    if overallMin <= 0.15:
        print("collision has occured")
    bot.minDis = min(sides.values())
    bot.state = [key for key in sides if sides[key] == bot.minDis]
    
def stateDis():
    if bot.state == ['Right'] or ['Front']:
        if bot.minDis < 0.5:
            bot.state.prox = 'Too Close'
        elif 0.5 <= bot.minDis < 0.8:
            bot.state.prox = 'Close'
        elif 0.8 <= bot.minDis < 1.2:
            bot.state.prox = 'Far'
        elif bot.minDis >= 1.2:
            bot.state.prox = 'Too Far'
    elif bot.state == ['RightFront']:
        if bot.minDis <= 1.2:
            bot.state.prox = 'Close'
        else:
            bot.state.prox = 'Far'
    print("The current state is ", bot.state, "and the prox is ", bot.state.prox)
    
def Qtable():
    data = {'Fwd':[0,0,10,0,0,0,0,-10,-1,0,0,0,0,-10,10,0,0],'Left':[10,1,0,-1,-10,-1,0,0,0,0,0,0,0,0,-1,0,0],\
            'Right':[-10,-1,0,1,10,0,0,10,1,0,0,0,1,1,-1,1,0], \
            'States':['R.TooClose','R.Close','R.Med', 'R.Far','R.TooFar','L.Close','L.Far','F.TooClose','F.Close', \
                      'F.Med', 'F.Far','RF.Close','RF.Far','O.AppWall','O.Parallel','O.AwayWall','O.Undef']}
            
    qTable = pd.DataFrame(data)

    
def findWall(sides):
    #print("The closest side is ", minSide)
    #print("Min dis: ", minDis)
    if bot.minDis >= 0.25:
        if bot.state == ['Front']:
            bot.pose.x = 0.1
            #print("moving towards Front", bot.minDis)
        if bot.state == ['Left']:
            bot.pose.y = 0.1
            #print("moving towards Left", bot.MinDis)
        if bot.state == ['Right']:
            bot.pose.y = -0.1
            #print("moving towards Right", bot.MinDis)
    else:
        stopMotion()
        bot.roaming = False
        
def followWall(sides):
    while bot.state != ['Right']:
        turn(sides, 5, 'R')
        updateScan(sides)
    print("wall is now on right")
    
    

def turn(sides, angle, direction):
    if direction == 'r' or 'R':
        angle = -angle
    stopMotion()
    i = 0
    while i < 500:
        bot.pose.theta = angle
        bot.pose.x = 0.35
        bot.vel_pub.publish(bot.pose)
        updateScan(sides)
        #print("Turning Right")
        i+=1
    stopMotion()
    bot.vel_pub.publish(bot.pose)
    return 

def stopMotion():
    bot.pose.theta = 0
    bot.pose.x = 0
    bot.pose.y = 0

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
        
        while bot.roaming == True:
            updateScan(sides)
            findWall(sides)
            bot.vel_pub.publish(bot.pose)
        
        while bot.roaming == False:
            followWall(sides)
            print("sleep start")
            rospy.sleep(5)
            print("sleep finish")     
        rate.sleep()
        
        
        
    
# This is how we usually call the main method in Python. 
if __name__ == "__main__":
    Main()