#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 19:59:40 2020

@author: cveney
"""
import pandas as pd
import numpy as np
import math

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def gaussian(x, meu, sig):
    return 1./(sig*math.sqrt(2**math.pi))*np.exp(-0.5*np.power((x - meu)/sig, 2.))

def learningMode():
    learning = bool(input("Do you want to run in learning mode? True or False?"))
    if learning == ("True"):
        print("True")
    if learning == ("False"):
        print("False")
    return(learning)

def policyMode():
    policy = bool(input("Do you want to use SARSA or Qlearning policy? True(SARSA) or False(Q)?"))
    if policy == ("True"):
        print("using SARSA")
    if policy == ("False"):
        print("using Q learning")
    return(policy)

def dispQtable(version, disp):
    start = {'States':['R.TooClose','R.Close','R.Med', 'R.Far','R.TooFar','L.Close','L.Far','F.TooClose','F.Close', \
        'F.Med','F.Far', 'F.TooFar','RF.Close','RF.Far'],\
        'Fwd':[0,5,100,5,0,0,0,-50,-10,1,10,20,0,1],'Left':[30,20,-10,-20,-30,-50,0,30,20,-1,-1,-1,1,0],\
        'Right':[-50,-20,-10,20,30,10,10,0,0,0,0,0,0,10]}
    startPd = pd.DataFrame(start)
    t1 = startPd.drop('States',axis = 1)
    #After running QL policy
    trainedQL = {'States':['R.TooClose','R.Close','R.Med', 'R.Far','R.TooFar','L.Close','L.Far','F.TooClose','F.Close', \
            'F.Med','F.Far', 'F.TooFar','RF.Close','RF.Far'],\
            'Fwd':[24,291,491,221,-1,-85,13,-33,57,48,64,12,76,-5],'Left':[64,332,340,196,0,14,-5,101,267,252,18,0,148,-4],\
            'Right':[-55,278,336,276,0,-29,0,-17,-23,105,-1,0,93,1]}
    trainedQLPd = pd.DataFrame(trainedQL)
    t2 = trainedQLPd.drop('States',axis = 1)
    #After running SARSA policy
    trainedS = {'States':['R.TooClose','R.Close','R.Med', 'R.Far','R.TooFar','L.Close','L.Far','F.TooClose','F.Close', \
            'F.Med','F.Far', 'F.TooFar','RF.Close','RF.Far'],\
            'Fwd':[-49,334,512,187,1,-52,2,-15,29,63,51,-8,75,10],'Left':[-40,438,345,214,4,-47,0,201,18,173,18,51,225,0],\
            'Right':[16,322,330,260,87,79,0,13,71,66,18,2,61,16]}
    trainedSPd = pd.DataFrame(trainedS)
    t3 = trainedSPd.drop('States',axis = 1)
    
    if version == 'start':
        table = t1.to_numpy()
        display = startPd
    elif version == 'learnedQL':
        table = t2.to_numpy()
        display = trainedQLPd
    elif version == 'learnedSARSA':
        table = t3.to_numpy()
        display = trainedSPd

    if disp == True:
        output = display
    else:
        output = table
        
    return output

def catRef(cat,index, value):
    if index == 0:
        cat.Right = value
    elif index == 1:
        cat.Front = value
    elif index == 2:
        cat.rightFront = value
    elif index == 3:
        cat.Left = value
    return cat

def stateDis(bot,states):
    allSides = np.array([bot.Right, bot.Front, bot.rightFront, bot.Left])
    idxSide = find_nearest(allSides, bot.min)
    state = [0, '!!!']
    for x in range (4):
        if x == 0:
            side = bot.Right
            subStates = np.array([[0,0.2,0.3,0.4,0.5],[0, 1, 2, 3, 4],['R.TooClose','R.Close','R.Med','R.Far','R.TooFar']])
        elif x == 1:
            side = bot.Front
            subStates = np.array([[0,0.2,0.3,0.4,0.5],[7, 8, 9, 10, 11],['F.TooClose','F.Close','F.Med','F.Far','F.TooFar']])
        elif x == 2:
            side = bot.rightFront
            subStates = np.array([[0,1.2],[12, 13],['RF.Close','RF.Far']])
        elif x == 3:
            side = bot.Left
            subStates = np.array([[0,0.5],[5,6],['L.Close','L.Far']])
            
        size = len(subStates[0])-1
        for i in range(0, size):
            if float(subStates[0][i]) < side <= float(subStates[0][i+1]):
                state = [int(subStates[1][i]), subStates[2][i]]
            elif side > float(subStates[0][size]):
                state = [int(subStates[1][size]), subStates[2][size]]
        
        if state[1] == '!!!':
            print(bot.Right, bot.Front,bot.rightFront,bot.Left)
            print(side, size)
            
        catRef(states, x, state)
        
        if x == idxSide:
            bot.ref = state
        
        
        
    #print(bot.ref, bot.Right, bot.Front, bot.rightFront, bot.Left)
    #print(states.Right, states.Front, states.rightFront,states.Left)
    
    return bot, states
                    
    
            
