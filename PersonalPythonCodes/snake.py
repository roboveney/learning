#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 17:14:03 2020

@author: cveney
"""
import pygame
import time
import random

#establish game window
pygame.init()

xMax = 400
yMax = 600
dis = pygame.display.set_mode((xMax,yMax))
pygame.display.set_caption('Christinas Game')

#set global variables
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
white = (255, 255, 255)
black = (0,0,0)

dis.fill(black)
clock = pygame.time.Clock()
bit = 10

def message(msg,color,size,x,y):
    font_style = pygame.font.SysFont(None, size)
    text = font_style.render(msg,True,color)
    dis.blit(text, [x, y])

def randBlock(axis):
    return round(random.randrange(0, axis - bit))

def snake(bit, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, white, [x[0], x[1], bit, bit])
        
def gameLoop(): 
    game_over = False
    game_close = False
    snake_speed = 10
    score = 0

    x1 = xMax/2
    y1 = yMax/2
    x1_change = 0
    y1_change = 0
            
    snake_list = []
    length_of_snake = 1    
    
    foodx = randBlock(xMax)
    foody = randBlock(yMax)
    poisonx = randBlock(xMax)
    poisony = randBlock(yMax)
    treatx = xMax+20
    treaty = yMax+20
    treat = False
        
    while not game_over:
        while game_close == True:
            dis.fill(white)
            message("You Lost! Press Q-Quit or P-Play Again", red, 20, xMax/3, 30)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        dis.fill(black)
                        snake_speed = 10
                        score = 0
                        gameLoop()
                        game_close = False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -bit 
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = bit
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -bit
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = bit

        #Update position        
        x1 += x1_change
        if x1 > xMax:
            x1 = 0
        elif x1 < 0:
            x1 = xMax
        y1 += y1_change
        if y1 > yMax:
            y1 = 0
        elif y1 < 0:
            y1 = yMax
        
        dis.fill(black)
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]
                
        snake(bit,snake_list)
        
        pygame.draw.rect(dis,white, [x1,y1,bit,bit])
        pygame.draw.rect(dis,green, [foodx, foody, bit, bit])
        pygame.draw.rect(dis,red, [poisonx, poisony, bit, bit])
        pygame.draw.rect(dis,blue, [treatx, treaty, bit, bit])
        message("Score: ", green, 30, xMax-100, yMax-50)
        message(str(score), green, 30, xMax-30, yMax-50)
        
        pygame.display.update()
        
        if foodx-8 <= x1 <= foodx+8 and foody-8 <= y1 <= foody+8:
            pygame.draw.rect(dis,black, [foodx,foody,10,10])
            foodx = randBlock(xMax)
            foody = randBlock(yMax)
            snake_speed += 1
            length_of_snake += 1
            score += 1
            
        if poisonx-8 <= x1 <= poisonx+8 and poisony-8 <= y1 <= poisony+8:
            print("I feel sick")
            game_close = True
        
        if treatx-8 <= x1 <= treatx+8 and treaty-8 <= y1 <= treaty+8:
            if snake_speed > 15:
                snake_speed -=10
                treatx = randBlock(xMax)
                treaty = randBlock(yMax)
                pygame.draw.rect(dis,black, [treatx, treaty, bit, bit])
                
        pygame.draw.rect(dis,black, [x1,y1,10,10])
        pygame.draw.rect(dis,black, [xMax-30, yMax-50, 30, 100])
        clock.tick(snake_speed)          
        
    pygame.quit()
    quit()
            
gameLoop()

