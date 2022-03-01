# -*- coding: utf-8 -*-
"""
Created on Sep 22 2020

@author: Tianyi Zhao
"""

import heapq as pq

#helper method to get successors of a given state
def get_succ(state):
    list = []                       #initialize a list of successors
    indexOf0 = state.index(0)       #get the index of the empty grid 0
    succ1 = state.copy()
    succ2 = state.copy()
    succ3 = state.copy()
    succ4 = state.copy()
    if indexOf0 == 0:               #get successor based on the index of 0
        succ1[0] = state[1]
        succ1[1] = 0
        succ2[0] = state[3]
        succ2[3] = 0
        list.append(succ1)
        list.append(succ2) 
    if indexOf0 == 1:
        succ1[1] = state[0]
        succ1[0] = 0
        succ2[1] = state[2]
        succ2[2] = 0
        succ3[1] = state[4]
        succ3[4] = 0
        list.append(succ1)
        list.append(succ2)
        list.append(succ3)
    if indexOf0 == 2:
        succ1[2] = state[1]
        succ1[1] = 0
        succ2[2] = state[5]
        succ2[5] = 0
        list.append(succ1)
        list.append(succ2)
    if indexOf0 == 3:
        succ1[3] = state[4]
        succ1[4] = 0
        succ2[3] = state[0]
        succ2[0] = 0
        succ3[3] = state[6]
        succ3[6] = 0
        list.append(succ1)
        list.append(succ2)
        list.append(succ3)
    if indexOf0 == 4:
        succ1[4] = state[3]
        succ1[3] = 0
        succ2[4] = state[5]
        succ2[5] = 0
        succ3[4] = state[1]
        succ3[1] = 0
        succ4[4] = state[7]
        succ4[7] = 0
        list.append(succ1)
        list.append(succ2)
        list.append(succ3)
        list.append(succ4)
    if indexOf0 == 5:
        succ1[5] = state[4]
        succ1[4] = 0
        succ2[5] = state[2]
        succ2[2] = 0
        succ3[5] = state[8]
        succ3[8] = 0
        list.append(succ1)
        list.append(succ2)
        list.append(succ3)
    if indexOf0 == 6:
        succ1[6] = state[3]
        succ1[3] = 0
        succ2[6] = state[7]
        succ2[7] = 0
        list.append(succ1)
        list.append(succ2)
    if indexOf0 == 7:
        succ1[7] = state[6]
        succ1[6] = 0
        succ2[7] = state[8]
        succ2[8] = 0
        succ3[7] = state[4]
        succ3[4] = 0
        list.append(succ1)
        list.append(succ2)
        list.append(succ3)
    if indexOf0 == 8:
        succ1[8] = state[5]
        succ1[5] = 0
        succ2[8] = state[7]
        succ2[7] = 0
        list.append(succ1)
        list.append(succ2)
    list.sort()                
    return list

#helper method to calculate the heuristic value of given state
def getHeuristic(successor):
    distance = 0
    #calculate distance differently for each line
    for i in range (1, 4): 
        distance += (int)(successor.index(i)/3) + abs(successor.index(i)%3 - (i-1))
    for i in range (4, 7):
        distance += abs(1 - int(successor.index(i)/3)) + abs(successor.index(i)%3 - (i-4)) 
    for i in range (7, 9):
        distance += 2 - (int)(successor.index(i)/3) + abs(successor.index(i)%3 - (i-7))
    return distance
    
def print_succ(state):
    succList = get_succ(state)     #generate successor list with helper method
    for i in range (0,len(succList)):  #calculate heuristic value for succ
        print(succList[i], ' h=' , getHeuristic(succList[i]), sep='')
    
    
def solve(state):
    openQueue = []                           #priority queue for successors
    moves = 0         
    parentIndex = -1
    pq.heappush(openQueue,((moves + getHeuristic(state)), state, 
                           (moves, getHeuristic(state), parentIndex)))
    closedList = []                          #list of visited states
    while(len(openQueue)!=0):
        currState = pq.heappop(openQueue)    #visit the state with highest priority
        closedList.append(currState)
        if(currState[1] == [1,2,3,4,5,6,7,8,0]): #check if goal state is met
            j = len(closedList) - 1
            printList = []
            while(j != -1):             #trace back the path by using parent index in closedList
                printList.append([closedList[j][1], closedList[j][2][1], closedList[j][2][0]])
                j = closedList[j][2][2]
            j = len(printList) - 1
            while(j != -1):             #print the path with corresponding h and move value
                print(printList[j][0], ' h=', printList[j][1], ' moves: ', printList[j][2], sep='')
                j -= 1
            return
        succStates = get_succ(currState[1]) #generate successors of poped and visited state
        moves = currState[2][0] + 1         #update value of moves and parentIndex
        parentIndex = len(closedList) - 1
        for i in range (0, len(succStates)): #push successors into the prioprity queue
            if succStates[i] in (closedList[0][1], closedList[len(closedList)-1][1]):
                continue  #ignore visited successor 
            if len(openQueue) != 0:
                if succStates[i] in (openQueue[0][1], openQueue[len(openQueue)-1][1]):
                    continue
            pq.heappush(openQueue, ((moves + getHeuristic(succStates[i])), 
             succStates[i], (moves, getHeuristic(succStates[i]), parentIndex)))
            
    print('Failed to find the goal state')

print(solve([8,7,6,5,4,3,2,1,0]))
    
    
    
    
    
    
    
    
    
    