#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import LaserScan
import pandas as pd
import numpy as np

class Object(object):
    pass

#Global Variables
scan_data = None
bot = Object()
bot.roaming = True # if the robot is looking for a wall
bot.speed = 3 #factor to increase the speed by

data = {'States':['R.TooClose','R.Close','R.Med', 'R.Far','R.TooFar','L.Close','L.Far','F.TooClose','F.Close', \
        'F.Med', 'F.Far','RF.Close','RF.Far','O.AppWall','O.Parallel','O.AwayWall','O.Undef'],\
        'Fwd':[1,10,20,10,0,0,0,-10,-1,0,0,0,0,-10,10,0,0],'Left':[1,1,0,-1,-10,-1,0,0,0,0,0,0,0,0,-1,0,0],\
        'Right':[-10,-1,0,1,10,0,0,10,1,0,0,0,1,1,-1,1,0]}

#After running long enough for convergence
datav2 = {'States':['R.TooClose','R.Close','R.Med', 'R.Far','R.TooFar','L.Close','L.Far','F.TooClose','F.Close', \
        'F.Med', 'F.Far','RF.Close','RF.Far','O.AppWall','O.Parallel','O.AwayWall','O.Undef'],\
        'Fwd':[1,43,76,50,0,44,40,-10,-1,60,0,43,0,-10,10,0,0],'Left':[1,1,0,-1,-10,-1,0,0,0,0,0,0,0,0,-1,0,0],\
        'Right':[-10,-1,0,1,49,0,0,10,46,0,0,0,1,1,-1,1,0]}
            
qTable = pd.DataFrame(datav2)
del qTable['States']
Qarray = qTable.to_numpy()
Rarray = Qarray.copy()
bot.Qlast = 0
bot.count = 0
bot.ref = 0


def callback(data):
    global scan_data
    scan_data = data
    
def updateScan(sides):
    sides['Right'] = round(min(scan_data.ranges[45:75]),3)
    sides['RightFront'] = round(min(scan_data.ranges[15:45]),3)
    sides['Front'] = round(min((scan_data.ranges[0:15] + scan_data.ranges[345:360])),3)
    sides['Left'] = round(min(scan_data.ranges[255:285]),3)
    overallMin = scan_data.range_min
    if overallMin <= 0.1:
        bot.collision = True
        print("collision has occured")
    bot.minDis = min(sides.values())
    bot.state = ([key for key in sides if sides[key] == bot.minDis])
    
def stateDis():
    if bot.state == ['Right']:
        if bot.minDis < 0.1:
            bot.ref = 0 #TooClose
        elif 0.1 <= bot.minDis < 0.25:
            bot.ref = 1 #Close
        elif 0.25 <= bot.minDis < 0.35:
            bot.ref = 2 #Med
        elif 0.35 <= bot.minDis < 0.5:
            bot.ref = 3 #Far
        elif bot.minDis >= 0.5:
            bot.ref = 4 #TooFar
    elif bot.state == ['Left']:
        if bot.minDis < 0.5:
            bot.ref = 5 #Close
        elif 0.5 <= bot.minDis:
            bot.ref = 6 #Far
    elif bot.state == ['Front']:
        if bot.minDis < 0.1:
            bot.ref = 7 #TooClose
        elif 0.1 <= bot.minDis < 0.25:
            bot.ref = 8 #Close
        elif 0.25 <= bot.minDis < 0.35:
            bot.ref = 9 #far
        elif 0.35 <= bot.minDis < 0.5:
            bot.ref = 10 #TooFar
    elif bot.state == ['RightFront']:
        if bot.minDis <= 1.2:
            bot.ref = 11 #Close
        else:
            bot.ref = 12 #Far
    elif bot.minDis >= 2:
        bot.roaming = True
    return bot.ref
    #print("The current state is ", bot.state)
    
def Qtable(sides):
    global Qarray
    global Rarray
    alpha = 0.2
    gamma = 0.8
    
    updateScan(sides)
    stateDis()
    s = bot.ref
    Qrow = Qarray[s,:]
    maxQ = max(Qrow)
    maxIdx = np.argmax(Qrow)
    reward = Rarray[s,maxIdx]
    stopMotion()
    
    f = bot.Qlast + alpha*(reward + gamma * maxQ - bot.Qlast)
    newQ = round(int(f),2)
    #print("new Q ", newQ, "Reward ", reward)
    if maxIdx == 0:
        bot.pose.x = 0.1*bot.speed
    elif maxIdx ==1:
        turn(sides,10, 'L')
    elif maxIdx ==2:
        turn(sides,10,'R')
    
    Qarray[s,maxIdx] = newQ
    bot.vel_pub.publish(bot.pose)
    
    bot.Qlast = newQ
    if (bot.count % 1000 == 0):
        print(Qarray, bot.count)

    
def findWall(sides):
    #print("The closest side is ", bot.state)
    #print("Min dis: ", bot.minDis)
    if bot.minDis >= 0.4:
        if bot.state == ['Front']:
            bot.pose.x = 0.1*bot.speed
            bot.pose.y = 0.01*bot.speed
            #print("moving towards Front", bot.minDis)
        if bot.state == ['Left']:
            bot.pose.x = 0.01*bot.speed
            bot.pose.y = 0.1*bot.speed
            #print("moving towards Left", bot.minDis)
        if bot.state == ['Right']:
            bot.pose.x = -0.01*bot.speed
            bot.pose.y = -0.1*bot.speed
            #print("moving towards Right", bot.minDis)
        bot.vel_pub.publish(bot.pose)
    else:
        stopMotion()
        bot.roaming = False
        Qtable(sides)
        
def followWall(sides):
    while bot.state != ['Right']:
        turn(sides, 5, 'R')
        updateScan(sides)
    Qtable(sides)
    
    

def turn(sides, angle, direction):
    if direction == 'r' or 'R':
        angle = -angle
    stopMotion()
    i = 0
    while i < 2:
        bot.pose.theta = angle
        bot.pose.x = 0.02*bot.speed 
        bot.pose.y = 0.02*bot.speed 
        bot.vel_pub.publish(bot.pose)
        updateScan(sides)
        #print("Turning ", direction)
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
        
        qTable = pd.DataFrame(datav2)
        print("Starting Q Matrix which will also be the static rewards matrix used.")
        print(qTable)
        rospy.sleep(3)
        #execute at 10hz.
        rate = rospy.Rate(10) 
    
    while not rospy.is_shutdown():
        turn(sides,50,'r') #avoid hitting weird corner at start
        stopMotion() #ensure robot is stopped from last run
        rospy.sleep(1)
        
        while bot.roaming == True:
            updateScan(sides)
            findWall(sides)
            bot.vel_pub.publish(bot.pose)
            stopMotion()
        while bot.roaming == False:
            followWall(sides)
            bot.count +=1
            stopMotion()
        rate.sleep()
                
            
if __name__ == "__main__":
    Main()