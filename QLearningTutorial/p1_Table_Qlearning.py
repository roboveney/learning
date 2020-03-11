#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gym

    #Load the environment to run Q learning in and ensure it is reset
env = gym.make("MountainCar-v0")
env.reset() 

done = False
while not done:
    action = 2 #option for what the car can do in this car go right"
    new_state, reward, done, _ = env.step(action)
    print(new_state)
    env.render()
    
env.close()