#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 15:25:21 2020

@author: cveney
"""

import csv
import numpy as np

#Fwd = []
#Left = []
#Right = []
#
#with open('/home/cveney/catkin_ws/src/d2_christina_veney/QresultSARSA.out') as csvDataFile:
#    csvReader = csv.reader(csvDataFile, delimiter=',')
#    #csvReader = csv.reader()
#    for row in csvReader:
#        Fwd.append(row[0])
#        Left.append(row[1])
#        Right.append(row[2])

#print(Fwd)
#print(Left)
#print(Right)


#output = np.genfromtxt('/home/cveney/catkin_ws/src/d2_christina_veney/QresultSARSA.out',delimiter=',')
output2 = np.genfromtxt('/home/cveney/catkin_ws/src/d2_christina_veney/QresultQL.out',delimiter=',')

#print(output)
#print("    ")
print(output2)
