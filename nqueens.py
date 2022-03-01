"""
Created on Sep 29 2020

@author: Tianyi Zhao
"""
import random

def succ(state, static_x, static_y):
    if state[static_x] != static_y:  # check whether a queen is on static point
        return []
    succList = [] 
    for i in range (0, len(state)):
        if i == static_x:
            continue
        succ1 = state.copy()
        succ2 = state.copy()
        if succ1[i]+1 != len(state): # check whether a move will excess the bound
            succ1[i] += 1
            succList.append(succ1)   # check whether a move will excess the bound
        if succ2[i]-1 != -1:
            succ2[i] -= 1
            succList.append(succ2)
    succList.sort()
    return succList

def f(state):
    f = 0
    for i in range (0, len(state)):
        for j in range (0, len(state)):
            if i == j:
                continue
            if abs(state[i]-state[j]) == abs(i-j) or state[i] == state[j]:
                f += 1
                break
    return f

def choose_next(curr, static_x, static_y):
    if curr[static_x] != static_y:  # check whether a queen is on static point
        return None
    succList = succ(curr, static_x, static_y)
    succList.append(curr)
    succList.sort()
    fList = []
    fList.append([succList[0],f(succList[0])])
    for i in range (1, len(succList)):   # find the succ with smallest f
        if f(succList[i]) < fList[0][1]: 
            fList.insert(0,[succList[i],f(succList[i])])
    return fList[0][0]
    
def n_queens(initial_state, static_x, static_y, print_path=True): 
    curr = initial_state 
    currF = f(curr)
    if print_path:
        print(initial_state, ' - f=', currF, sep = '')
    while f(curr) != 0:       # check whether f=0 is met
        curr = choose_next(curr, static_x, static_y)
        prevF = currF
        currF = f(curr)
        if print_path:
            print(curr, ' - f=', currF, sep = '')
        if(prevF == currF):   # end the funcion if two loop creates the same f value
            break
    return curr

def n_queens_restart(n, k, static_x, static_y, print_path=True):
    initial_state = [0]*n
    resultList = []
    while k!=0:
        for i in range (0, n):      # intialize a random state and set the static point
            if i == static_x:
                initial_state[i] = static_y
            else:
                initial_state[i] = random.randint(0,n-1)
        result = n_queens(initial_state, static_x, static_y, print_path=False)
        if f(result) == 0:    # if f=0 is found, print the result and end the function
            print(result, ' - f=', f(result), sep = '')
            return 
        resultList.append(result)
        k-=1   
    minF = f(resultList[0])   # if f=0 is not reached, put all smallest result into a list
    minList = []
    for i in range(1, len(resultList)):
        if f(resultList[i]) < minF:
            minF = f(resultList[i])
    for i in range(0, len(resultList)):
        if f(resultList[i]) == minF:
            minList.append(resultList[i])
    minList.sort()           # sort the list of smallest result and print
    for i in range(0, len(minList)):
        print(minList[i], ' - f=', minF, sep = '')
        
        

print((8-7)/2) 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    