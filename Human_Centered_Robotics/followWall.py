#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import LaserScan
import numpy as np
import math
import time
from random import randint, random
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
import moreFunctions as F

class Object(object):
    pass

#Global Variables
scan_data = None
bot = Object()
bot.collision = False
bot.speed = 1.5
bot.count = 0
bot.lastS = 0
bot.lastA = 0
bot.min = 10
bot.ref = [2,'R.Med']
bot.epsdn = 0
bot.badState = 0
bot.AcuReward = 0

states = Object()
states.Right = [2, 'R.Med']
states.Front = [9, 'F.Med']
states.rightFront = [12, 'RF.Med']
states.Left = [5, 'L.Med']

def callback(data):
    global scan_data
    scan_data = data

def repositionBot():
    c = random()/2 + 0.25
    x = randint(-3,3) + c
    y = randint(-3,3) + c
    state_msg = ModelState()
    state_msg.model_name = 'triton_lidar'
    state_msg.pose.position.x = x
    state_msg.pose.position.y = y
    rospy.wait_for_service('/gazebo/set_model_state')
    set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
    set_state(state_msg)

def updateScan():
    bot.Left = round(min(scan_data.ranges[60:160]),3)
    bot.rightFront = round(min(scan_data.ranges[290:340]),3)
    bot.Front = round(min((scan_data.ranges[0:30] + scan_data.ranges[340:360])),3)
    bot.Right = round(min(scan_data.ranges[240:290]),3)
    bot.min = round(min(scan_data.ranges[0:360]),3)
    if bot.min < 0.12:
        bot.collision = True
        print("collision has occured")
    else:
        bot.collision = False

    stopMotion()
    F.stateDis(bot,states)
    #print("R:", bot.Right,"RF:", bot.rightFront, "F:",bot.Front,"L:",bot.Left)

def calcReward(aIdx):
    updateScan()
    
    fwdR = abs(round(scan_data.ranges[230],3))
    bckR = abs(round(scan_data.ranges[310],3))
    slope = round(fwdR-bckR,5) 
    
    #guassian for slope max of about 2
    xS = np.linspace(-0.35, 0.35, 100)
    yS = np.array([xS,F.gaussian(xS,0,0.175)])
    idxS = F.find_nearest(yS[0],slope)
    
    #guassian for distance max of about 18
    xD = np.linspace(0.2, 0.5, 100)
    yD = np.array([xD,F.gaussian(xD,0.35,0.03)])
    idxD = F.find_nearest(yD[0],bot.Right)
    
    #max reward around 40 if at best slope and distance    
    r = math.floor((yS[1][idxS]) * (yD[1][idxD])) 
    
    r2 = 0
    if states.Front[0] >=9 and bot.lastS <=3: #encourage wall following
        if 0 < states.Right[0] <= 2:
            r2 = 60 + 20*int(states.Right[0])
            bot.AcuReward += 10            
            bot.badState = 0
        elif states.Right[0] > 2 and aIdx ==2: #encourage proper u turns
            bot.AcuReward += 10
            bot.badState = 0
            r2 = 75
        else:
            r2 -= 25
    elif states.Front[0] <= 9: #encourage left turn when approaching walls
        if aIdx == 1 and bot.lastS in [0,7,8,9,12]:
            r2 += 50
        else:
            r2 -= 50
    elif bot.collision == True or bot.ref[0] in [0,7]: #discourage hitting wall
        r2 -= 50
    elif bot.lastS in [5,6] and bot.ref[0] in [7,8,9,12]:
        r2 += 5
    elif bot.ref[0] == 5 and bot.lastS==5: #discourage following on left side
        r2 -= 1
    elif bot.min > 0.5 and bot.ref[0] ==13:
        r2 += 1
    
    if r2 < 0:  #track if robot is stuck in a behavior
        bot.badState +=1 
    elif r2 > 0:
        bot.badState -=1
                
    R = int(r) + r2
    #print("rewards:",int(r), r2)
    return R

def Qlearn():
    if bot.learnMode == True:
        eps = 1 - (0.9 * bot.epsdn) #ensures randomness decreases w/ each episode
        alpha = 0.2
        gamma = 0.8
    else:
        eps = 1
        alpha = 0
        gamma = 0.8
    
    r = random()

    updateScan()
    s = bot.ref[0]
    Qrow = bot.Qarray[s,:]
    
    Qlast =  bot.Qarray[bot.lastS, bot.lastA]
    maxQ = max(Qrow)
    if r < eps:
        curQ = maxQ
        aIdx = np.argmax(Qrow)
    else:
        aIdx = randint(0,2)
        curQ = bot.Qarray[s,aIdx]
        
    reward = calcReward(aIdx)
    
    if bot.policy == True: #using SARSA
        f = Qlast + alpha * (reward + gamma * curQ - Qlast)
    elif bot.policy == False: #using Qlearning
        f = Qlast + alpha * (reward + gamma * maxQ - Qlast)
                
    newQ = round(int(f),2)
    #print("newQ:",newQ)
    
    if newQ == 0:
        bot.badState +=1
    elif newQ != 0:
        bot.badState -=1
    
    if aIdx == 0:
        drive()
    elif aIdx ==1:
        turn('l')
    elif aIdx ==2:
        turn('r')
    
    bot.Qarray[bot.lastS,bot.lastA] = newQ
    bot.lastS = s
    bot.lastA = aIdx
    
    if (bot.count % 500 == 0):
        print(bot.Qarray, bot.count)
    
def drive():
    bot.pose.theta = 0
    bot.pose.x = 0.3
    bot.pose.y = 0
    bot.vel_pub.publish(bot.pose)  
    
def turn(direction):
    if direction in ['r','R']:
        ang = -1.25
    else:
        ang = 1.25
    bot.pose.theta = ang
    bot.pose.x = 0.1
    bot.pose.y = 0
    bot.vel_pub.publish(bot.pose)
            
def stopMotion():
    bot.pose.theta = 0
    bot.pose.x = 0
    bot.pose.y = 0
    bot.vel_pub.publish(bot.pose)

def Main():
    rospy.init_node("RL_robot", anonymous=True)
    bot.laser_sub = rospy.Subscriber('/scan', LaserScan, callback)
    bot.vel_pub = rospy.Publisher("/triton_lidar/vel_cmd", Pose2D, queue_size=2)
    bot.pose = Pose2D()
    rate = rospy.Rate(10) #execute at 10hz.
    start = time.time()
    
    if bot.count == 0:
        print("waiting for scan_data")
        bot.learnMode = F.learningMode()
        bot.policy = F.policyMode()
        stopMotion()
        print("Starting Qtable is the following:")
        if bot.learnMode == True:
            total_episodes = 500
            max_steps = 500
            bot.Qarray = F.dispQtable('start',False)
            print(F.dispQtable('start',True))
        else:
            total_episodes = 5
            max_steps = 5000
            if bot.policy == True:
                bot.Qarray = F.dispQtable('learnedSARSA',False)
                print(F.dispQtable('learnedSARSA',True))
            else:
                bot.Qarray = F.dispQtable('learnedQL',False)
                print(F.dispQtable('learnedQL',True))
        rospy.sleep(3)
        
        Eval = np.zeros(total_episodes)
            
            
    # Wait until the first scan is available.
    while scan_data is None and not rospy.is_shutdown():
        stopMotion()
        
        
    for episode in range(total_episodes):
        bot.count = 0 
        bot.epsdn = pow(0.985,episode+1) #start out a little less random and ensure near 1 eps before stop
        #print("current eps:", 1-(0.9*bot.epsdn))
        stopMotion()
        repositionBot()
        rospy.sleep(1)
        updateScan()
        while bot.count < max_steps:
            if bot.learnMode == False:
                bot.badState = 0
            if bot.collision == True or abs(bot.badState) > 100:
                #print("break cond met:", bot.collision, bot.badState)
                bot.collision = False
                bot.badState = 0
#                Eval[episode] = bot.AcuReward
#                print("total reward", bot.AcuReward)
#                bot.AcuReward = 0
                break
            Qlearn() 
            bot.count += 1
            rate.sleep()
        Eval[episode] = bot.AcuReward
        print("total reward", bot.AcuReward)
        bot.AcuReward = 0
        print(episode, " episodes complete")
        t = time.time()
        print("time(s): ", (t-start))
    if bot.policy == True:    
        np.savetxt('/home/cveney/catkin_ws/src/d2_christina_veney/QresultSARSA.csv', bot.Qarray, delimiter=',')  
    else:
        np.savetxt('/home/cveney/catkin_ws/src/d2_christina_veney/QresultQL.csv', bot.Qarray, delimiter=',')  
    
    np.savetxt('/home/cveney/catkin_ws/src/d2_christina_veney/AcumulatedReward.csv', Eval, delimiter=',')
     
if __name__ == "__main__":

    Main()

