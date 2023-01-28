## A* algorithm to search the best way to the goal.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import random
import os
from time import sleep
from termcolor import colored

#Example matrix
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
    
#A recursive fuction wich do the movements using closeSet, OpenSet and a taboo list called badWays to not display the ways in which the algorithm stuck due to no solutions
def startMoving(matrix, currentPosition, openSet: set, closeSet: set, index: int = 0, anterior = None, badWays : set = set()):
    x,y = currentPosition[0]
    iterations=0
    
    #stop Condition (find G)
    if matrix[x][y] != 'G':   
        i = index + 1   
        if index==0:
            matrix[x][y]="S"
            closeSet.add(currentPosition)
        # Movements which we can do
        listaMovimientos = [(1,0), (-1,0), (0,1), (0,-1)]
        # Got all the possible movements and put it in our openSet
        for (posX,posY) in listaMovimientos:
            proxMov = ( x+posX, y+posY )
            # Check if the movement is correct ( len )
            if(checkCorrectPosition(proxMov,matrix)):
                move= (proxMov,manhatamDistance(proxMov), i)
                gotItFlag=False
                # Check if the movement is already in out closeSet (this is for the index, because a new it have a upper index)
                for movimientos in closeSet:
                    if( proxMov == movimientos[0]):
                        gotItFlag = True
                # If we dont have it, and is not in our badWays ( this avoid bas ways in which the alogrith couldnt find the goal)
                if(gotItFlag == False and (move not in badWays)):
                    openSet.add(move)
                    
        #Obtenemos el mejor movimiento( el que tiene menor coste )
        bestMoveOfOpenset=checkBestmove(openSet)

        #Removemos el mejor movimiento de nuestro OpenSet
        openSet.remove(bestMoveOfOpenset)
        ##Borramos los caminos inutiles  
        openSet, closeSet, badWays = deleteBadWays(bestMoveOfOpenset, closeSet,openSet,badWays)  
        #añadimos el mejor movimiento a nuestro closeSet  
        closeSet.add(bestMoveOfOpenset)
        bestMove=bestMoveOfOpenset[0]
        paintCells(matrix,closeSet)
        startMoving(matrix,bestMoveOfOpenset, openSet,closeSet,index=i, anterior=index,badWays=badWays)
    else:
        print("G encontrada en pos: ",currentPosition[0])
        iterations=currentPosition[2]

    return (openSet,closeSet,badWays,iterations)
#This fuction delete the badWays in closeSet and their corresponding paths generated
def deleteBadWays(bestMove, closeSet,openSet,badWays):
        ##Borramos los caminos inutiles
        indexActual = bestMove[2]
        
        #Check if the way was not valid
        deleteFlag=False
        for movimientos in closeSet:
            move,cost,indexMov=movimientos
            if indexActual == indexMov:
                deleteFlag=True
        #If was not valid, then delete
        if deleteFlag:
            for movimientos in closeSet.copy():
                move,cost,indexMov=movimientos
                if indexActual == indexMov:
                    badWays.add(movimientos)
                    closeSet.discard(movimientos)
                elif indexActual < indexMov:
                    closeSet.discard(movimientos)
            for movimientos in openSet.copy():
                move,cost,indexMov=movimientos
                if indexActual <= indexMov:
                    openSet.discard(movimientos)
        return openSet,closeSet,badWays
    
# This show us the procces of the algorithm
def paintCells(matrix, closeset: set):
    #os.system('CLS')
    showMatrix(matrix,color=True,closeSet=closeset) 
    print()      
    #sleep(0.5)



# Check the best move checking the cost of all the movements in the openSet
def checkBestmove(openSet):
    min=9999999
    bestMoveOfOpenset=0
    for mov in openSet:
        coste = mov[1]
        if coste < min:
            bestMoveOfOpenset=mov
            min=coste
    return bestMoveOfOpenset
    
        
                
    
    
# Check if the position is correct    
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

# This is the heuristic to be used in our algorithm, which measures the distance from our actual cell to the goal cell     
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
    startPosition = ((0, 0), 0, 0)
    
    showMatrix(staticMatrix)
    openSet, closeSet, badWays, iterations = startMoving(staticMatrix,startPosition , openSet, closeSet)
    print(colored("Best way : ","light_green"),closeSet ,colored("\n\nBadWays: ","light_green"), badWays,colored("\n\nNumber of iterations: ","light_green"),iterations)
    
    
    
main()        
    
    
    