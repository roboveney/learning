#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 17:14:03 2020

@author: cveney
"""
import pygame


#establish game window
pygame.init()

xMax = 400
yMax = 600
game_over = True
dis = pygame.display.set_mode((xMax,yMax))
pygame.display.update()
pygame.display.set_caption('Christinas Game')
        
while game_over == False:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game_over=True

pygame.quit()
quit()
