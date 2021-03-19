from scipy.signal import convolve2d
import numpy as np
import random
import math

def switchPlayer(player):
    if player == 1:
        player = 2
    else:
        player = 1
    return player
        
def scoring(board):
    #Kernels to check direction connections
    horizontal_kernel = np.array([[ 1, 1, 1, 1]])
    vertical_kernel = np.transpose(horizontal_kernel)
    diagR_kernel = np.eye(4, dtype=np.uint8)
    diagL_kernel = np.fliplr(diagR_kernel)
    detection_kernels = [horizontal_kernel, vertical_kernel, diagR_kernel, diagL_kernel]

    p1Board = (board == 2)*-1 + (board == 1)*1
    p2Board = (board == 2)*1 + (board == 1)*-1
    #create scoreboard of number of 4,3, and 2 connections.
    scores = np.zeros([2,4])
    for kernel in detection_kernels:
        p1connections = convolve2d(p1Board, kernel, mode="valid")
        p2connections = convolve2d(p2Board, kernel, mode="valid")

        #4 connections
        scores[0][0] += np.count_nonzero(p1connections == 4)
        scores[1][0] += np.count_nonzero(p2connections == 4)
        #3 connections
        scores[0][1] += np.count_nonzero(p1connections == 3)
        scores[1][1] += np.count_nonzero(p2connections == 3)
        #2 connections
        scores[0][2] += np.count_nonzero(p1connections == 2)
        scores[1][2] += np.count_nonzero(p2connections == 2)
        
    #Kernels to check for gaps
    close_horizontal = np.array([[ 1, 0, 1, 1]])
    close_horizontal2 = np.array([[ 1, 1, 0, 1]])
    close_vertical = np.transpose(close_horizontal)
    close_vertical2 = np.transpose(close_horizontal2)
    close_diagR = np.eye(4, dtype=np.uint8)
    close_diagR[1][1] = 0
    close_diagR_2 = np.copy(close_diagR)
    close_diagR_2[2][2] = 0
    close_diagL = np.fliplr(close_diagR)
    close_diagL[1][1] = 0
    close_diagL_2 = np.copy(close_diagL)
    close_diagL_2[2][2] = 0
    close_kernels = [close_horizontal, close_horizontal2, close_vertical, close_vertical2, close_diagR, close_diagL]

    for kernel in close_kernels:
        p1connections = convolve2d(p1Board, kernel, mode="valid")
        p2connections = convolve2d(p2Board, kernel, mode="valid")
        
        scores[0][3] += np.count_nonzero(p1connections == 3)
        scores[1][3] += np.count_nonzero(p2connections == 3)

    return scores

def isLegal(board, column):
    check = np.where(board[:, [column]] == 0)
    if np.size(check) > 0:
        return True
    else:
        return False

def makeMove(board, column, player):        
    temp = np.copy(board)
    for i in reversed(range(6)):
        if temp[i][column] == 0:
            temp[i][column] = player
            return temp
        
def minimax(node, depth, alpha, beta, playerNum, maxPlayer):
    valid_moves = {}
    gameOver = np.all(node!=0) #check if board is full
    
    if depth == 0 or gameOver:
        score = heuristic(node, playerNum, maxPlayer)
        return None, score
        
    #create list of legal moves and the heuristic scores
    for col in range(7):
        if isLegal(node,col):
            temp = makeMove(node, col, playerNum)
            score = heuristic(temp, playerNum, maxPlayer)
            valid_moves[col]= score
            
    if maxPlayer:
        value = -math.inf
        column = 8
        sortedValues = sorted(valid_moves.items(), key=lambda x: x[1], reverse=True)
        for col, score in sortedValues:
            child = makeMove(node, col, playerNum)
            newscore = minimax(child, depth-1, alpha, beta, switchPlayer(playerNum), False)[1]
            if newscore > value:
                value = newscore
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = 8
        sortedValues = sorted(valid_moves.items(), key=lambda x: x[1], reverse=True)
        sortedValues.reverse()
        for col, score in sortedValues:
            child = makeMove(node,col,playerNum)
            newscore = minimax(child, depth-1, alpha, beta, switchPlayer(playerNum), True)[1]
            if newscore < value:
                value = newscore
                column = col
            beta = min(beta, value)
            if beta <= alpha:
                break
        return column, value

def heuristic(state, curr_player, maxPlayer):
    scores = scoring(state)
    if maxPlayer:
        if curr_player ==1:
            total = sum(scores[0]*[1000,100,10,100]) - sum(scores[1]*[1000,100,10,100])
        else:
            total = sum(scores[1]*[1000,100,10,100]) - sum(scores[0]*[1000,100,10,100])
    else:
        if curr_player ==1:
            total = sum(scores[1]*[1000,100,10,100]) - sum(scores[0]*[1000,100,10,100])
        else:
            total = sum(scores[0]*[1000,100,10,100]) - sum(scores[1]*[1000,100,10,100])
    return total

