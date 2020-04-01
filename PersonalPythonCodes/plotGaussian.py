#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 10:41:43 2020

@author: cveney
"""

from matplotlib import pyplot as plt
import numpy as np
import math

def gaussian(x, meu, sig):
    return 1./(sig*math.sqrt(2**math.pi))*np.exp(-0.5*np.power((x - meu)/sig, 2.))

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

<<<<<<< HEAD
x = np.linspace(0.2, 0.5, 100)
plt.plot(x, gaussian(x,0.35, 0.03))
=======
x = np.linspace(-0.5, 0.5, 100)
plt.plot(x, gaussian(x, 0, 0.15))
>>>>>>> parent of a146a3e... small updates to ref doc and added Gaussian plot example in python codes

y = np.array([x,gaussian(x, 0.35, 0.03)])

plt.show()

idx = find_nearest(y[0],0.3)
check = y[1][idx]

print(check)
 
