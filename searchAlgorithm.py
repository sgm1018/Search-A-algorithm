## A* algorithm to search the best way to the goal.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import random
import os
from time import sleep
from termcolor import colored
staticMatrix = [["S", 0, 0, "X", 0, "X", "X", "X", "X", "X", 0, "X", "X", 0, 0, "X", "X", 0, 0],
                ["X", 0, "X", 0, 0, 0, 0, 0, "X", 0, "X", 0, 0, "X", "X", 0, "X", "X", 0],
                [0, 0, "X", "X", 0, 0, 0, "X", "X", 0, 0, 0, 0, 0, 0, 0, 0, 0, "X"],
                [0, 0, 0, 0, 0, 0, 0, "X", 0, 0, 0, 0, 0, "X", 0, "X", 0, "X", "X"],
                [0, 0, 0, 0, 0, "X", 0, 0, 0, 0, "X", 0, 0, 0, "X", 0, 0, 0, 0],
                [0, 0, 0, 0, "X", "X", "X", 0, 0, "X", 0, 0, "X", "X", 0, 0, 0, "X", "G"]]
#First we create a N:M matrix.
#N: is the number of rows.
#M: is the number of colunms.
def createMatrix(N,M):
    matrix=[]
    for x in range(N):
        matrix.append([])
        for y in range(M):
            matrix[x].append(0)
    return matrix

#show the matrix.
#matrix: the matrix to show.
def showMatrix(matrix,color=False,closeSet=None):
    if(color == False):
        for row in matrix:
            print("")
            for number in row:
                print(number,end=" ")      
    else:
        listNodos=set()
        for NodoCerrado in closeSet:
            listNodos.add(NodoCerrado[0])
        for x in range(len(matrix)):
            print("")
            for y in range(len(matrix[x])):
                if (x,y) in listNodos: 
                   print(colored(matrix[x][y], 'red'),end=" ") 
                else: 
                   print(colored(matrix[x][y], 'green'),end=" ")  
                

#this fuction genre obstacles in out matrix
# matrix : matrix to generae obstacles
# nObstacles : number of obstacles to be generated
# This fuction generate number of obstacles through a random number, the row will be the division with this number
# and the column will be the rest with this number.
# I use a set to set obstacles on no repeat positions.
def generateRandomObstacles(matrix, nObstacles):
    cont=0
    positionSet = set()
    while(cont < nObstacles):
        randoPosition = random.randint(0,len(matrix)* len(matrix[0])-1)
        if randoPosition not in positionSet:   
            positionSet.add(randoPosition)
            rowPos = int(randoPosition / len(matrix[0]))
            colPos = int(randoPosition % len(matrix[0]))
            matrix[rowPos][colPos] = "X"
            cont += 1    
    return matrix
    
def nextMove(matrix,currentPosition, openSet: set, closeSet: set, index: int = 0):
    if matrix[currentPosition[0]][currentPosition[1]] != 'G':     
        currentPoswithCost=(currentPosition, manhatamDistance(currentPosition))
        closeSet.add(currentPoswithCost)
        x,y = currentPosition
        listaMovimientos = [(1,0), (-1,0), (0,1), (0,-1)]
        for (posX,posY) in listaMovimientos:
            proxMov = ( x+posX, y+posY )
            if(checkCorrectPosition(proxMov,matrix)):
                move= (proxMov,manhatamDistance(proxMov))
                if(move not in closeSet):
                    openSet.add(move)
        bestMoveOfOpenset=checkBestmove(openSet)
        #print("\nopenSet: ",openSet)
        #print("\ncloseSet: ",closeSet)
        openSet.remove(bestMoveOfOpenset)
        bestMove=bestMoveOfOpenset[0]
        #print("bestMove: ",bestMove )
        #print("openSetDespues: ",openSet)
        paintCells(matrix,closeSet)
        nextMove(matrix,bestMove, openSet,closeSet)
    else:
        print("G encontrada en pos: ",currentPosition)
        return closeSet
 

def paintCells(matrix, closeset: set):
    os.system('CLS')
    showMatrix(matrix,color=True,closeSet=closeset) 
    sleep(0.5)
    print()      



 
def checkBestmove(openSet):
    min=9999999
    bestMoveOfOpenset=0
    for mov in openSet:
        xymove, coste = mov
        if coste < min:
            bestMoveOfOpenset=mov
            min=coste
    return bestMoveOfOpenset
    
        
                
    
    
    
def checkCorrectPosition(move,matrix):
    x,y = move
    correct = False
    if( 0 > x or 0 > y or x > len(matrix)-1 or y > len(matrix[0])-1):
        correct = False
    elif( matrix[x][y] == "X"): 
        correct = False
    else:
        correct=True
    return correct
                 
def manhatamDistance(move, goal=(5,18)):
    xA,yA = move
    xG,yG = goal
    return (abs(xA-xG)+abs(yA-yG))
        




def main():
    #matrix = createMatrix(6,20)
    #matrix = generateRandomObstacles(matrix,40)
    openSet=set()
    closeSet=set()
    state = True
    currentPosition=(0,0)
    showMatrix(staticMatrix)
    nextMove(staticMatrix,currentPosition, openSet, closeSet)
    
    
main()        
    
    
    