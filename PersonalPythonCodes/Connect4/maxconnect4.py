import sys
import os.path
from os import path
from scipy.signal import convolve2d
import helperFuctionsConnect4 as f
import numpy as np
import math
import random as r
import time

#Translate provided txt into numpy for use in algorithm
def readInput(fileName):
    if path.exists(fileName)==False:
       npBoard = np.zeros([6,7])
       player = '1'
    else:
        lines = []
        with open(fileName) as f:
            lines = f.readlines()
        player = lines.pop()
        npBoard = np.zeros([6,7])
        for x,row in enumerate(lines):
            for y,i in enumerate(row):
                if i != '\n':
                    npBoard[x][y]=int(i)
    return (int(player), npBoard)

#Switch between players given computer and human can be either 1 or 2
def switchPlayer_main(player):
    turn = player[0]
    title = player[1]
    if turn == 1:
        turn = 2
    else:
        turn = 1
    if title == 'Computer':
        title = 'Human'
    else:
        title = 'Computer'
    return [turn, title]
        
#Save board to designated txt file
def saveBoard(board, player, fileName):
    f=open(fileName,'a')
    f.truncate(0)
    np.savetxt(f, board, fmt='%d',delimiter='')
    f.write(player)
    f.close() 

#Allow play between computer and human using minimax
def InteractiveMode(boardState, player, depth):
    while True:
        if player[1] == 'Computer':
            if np.all(boardState!=0):
                score = f.scoring(boardState)
                print("Game Over")
                print("P1 Score: ", score[0,0]," P2 Score: ", score[1,0])
                break
            print("COMPUTERS TURN (",player[0],')')
            move = f.minimax(boardState, depth, -math.inf, math.inf, player[0], True)
            boardState = f.makeMove(boardState, move[0], player[0])
            saveBoard(boardState,  str(player[0]), 'computer.txt')
            print(boardState)
            player = switchPlayer_main(player)
        if player[1] == 'Human':
            if np.all(boardState!=0):
                score = f.scoring(boardState)
                print("Game Over")
                print("P1 Score: ", score[0,0]," P2 Score: ", score[1,0])
                break
            print("HUMAN TURN (",player[0],')')
            move = int(input("Choose your move (ie value 1-7)\n"))-1
            while move not in range(0,7):
                print("Invalid input select a value 1-7\n")
                move = int(input("Choose your move (ie value 1-7)\n"))-1
            while f.isLegal(boardState, move)==False:
                print("that row is full select a new value \n")
                move = int(input("Choose your move (ie value 1-7)\n"))-1
            boardState = f.makeMove(boardState, move, player[0])
            print(boardState)
            saveBoard(boardState, str(player[0]), 'human.txt')
            player = switchPlayer_main(player)
    return boardState, score

#use random number generator to test play statistics of algorithm
def evalInteractiveMode(boardState, player, depth):
    while True:
        if player[1] == 'Computer':
            if np.all(boardState!=0):
                score = f.scoring(boardState)
                break
            move = f.minimax(boardState, depth, -math.inf, math.inf, player[0], True)
            boardState = f.makeMove(boardState, move[0], player[0])
            player = switchPlayer_main(player)
        if player[1] == 'Human':
            if np.all(boardState!=0):
                score = f.scoring(boardState)
                break
            possMove = []
            for col in range(0,7):
                if f.isLegal(boardState, col):
                    possMove.append(col)
            move = r.choice(possMove)
            boardState = f.makeMove(boardState, move, player[0])
            player = switchPlayer_main(player)
    return boardState, score

#alternate to main when running evalInteractive mode
def evaluate():
    mode = 'interactive'
    inputFile = 'case2_input.txt'
    gameNums = 10
    
    nextPlayer,board = readInput(inputFile)
    player = [nextPlayer,'Computer']
    results = []
    tracking = np.zeros([gameNums,2])
    for depth in range(3,4):
        for i in range(gameNums):
            start = time.time()
            boardState, score = evalInteractiveMode(board, player, depth)
            end = time.time()
            timeElapse = end - start
            if score[0, 0] > score[1,0]:
                tracking[i]= [1,0]
            elif score[0, 0] < score[1,0]:
                tracking[i] = [0,1]
            else:
                tracking[i] = [0,0]
            print(player, "depth:", depth,"results:",tracking.sum(axis=0), timeElapse)
    results.append(tracking.sum(axis=0))
    return results
    

#Test main for inside IDE
def main2():
    mode = 'interactive'
    inputFile = 'case2_input.txt'
    firstPlayer = 'Computer'
    depth = 5
    
    nextPlayer,board = readInput(inputFile)
    if firstPlayer == 'Computer':
        player = [nextPlayer,'Computer']
    else:
        player = [nextPlayer, 'Human']
        
    if mode == 'interactive':
        InteractiveMode(board, player, depth)
    else:
        move = f.minimax(board, depth, -math.inf, math.inf, player[0], True)
        if move[0] == None:
            print(board)
            print("Game Over - Board is full")
            return
        board = f.makeMove(board, move[0], player[0])
        saveBoard(board, str(player[0]))
        print(board)

#Section to use to enable command line level options        
def main(argv):
    if len(sys.argv) == 5:
        mode = sys.argv[1]
        if mode == 'interactive':
            inputFile = sys.argv[2]                
            playerSel = sys.argv[3]
            depth = int(sys.argv[4])
            
            nextPlayer,board = readInput(inputFile)
            if playerSel == 'computer-next':
                player = [nextPlayer,'Computer']
            else:
                player = [nextPlayer, 'Human']
                
            InteractiveMode(board, player, depth)
        else:
            inFile = sys.argv[2]
            outFile = sys.argv[3]
            depth = int(sys.argv[4])
            
            nextPlayer,board = readInput(inFile)
            
            if np.all(board!=0):
                score = f.scoring(board)
                print("Board Full:")
                print("Game Over:")
                print("P1 Score: ", score[0,0]," P2 Score: ", score[1,0])
                return
            move = f.minimax(board, depth, -math.inf, math.inf, nextPlayer, True)
            board = f.makeMove(board, move[0], nextPlayer)
            score = f.scoring(board)
            saveBoard(board, str(f.switchPlayer(nextPlayer)), outFile)
            print(board)
            print("P1 Score: ", score[0,0]," P2 Score: ", score[1,0])
    else:
        print("Incorrect number of inputs provided...")
        
    
        
        
if __name__ == "__main__":
    main(sys.argv[1:])
#    main2()
#    assess = evaluate()