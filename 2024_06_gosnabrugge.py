# -*- coding: utf-8 -*-
"""
Advent of Code day 6 script
"""
import numpy as np
import matplotlib.pyplot as plt
import time

#### helper functions ####
def moveGuard(grid):
    # initial conditions
    direction = 0   # guard's movement direction (0: up, 1: right, 2:down, 3:left)
    cRow = 69      # guard's current row position
    cCol = 74      # guard's current col position
    guardStates = [[direction,cRow, cCol]]
    
    guardOnGrid = True
    guardInLoop = False
    nSpaces = 1
    
    while guardOnGrid and not guardInLoop:     
        if direction == 0: # move up
            moveLine = grid[cRow::-1,cCol]
            moveSteps = np.where(moveLine == -1)[0]
            if len(moveSteps) >= 1:
                moveSteps = int(moveSteps[0])
                grid[cRow:cRow-moveSteps:-1,cCol] = 1
                cRow = cRow-moveSteps+1
            else:
                grid[cRow::-1,cCol] = 1
                guardOnGrid = False
                
        elif direction == 1: # move right
             moveLine = grid[cRow,cCol::]
             moveSteps = np.where(moveLine == -1)[0]
             if len(moveSteps) >= 1:
                 moveSteps = int(moveSteps[0])
                 grid[cRow,cCol:cCol+moveSteps] = 1
                 cCol = cCol+moveSteps-1
             else:
                 grid[cRow,cCol::] = 1
                 guardOnGrid = False
                 
        elif direction == 2: # move down
             moveLine = grid[cRow::,cCol]
             moveSteps = np.where(moveLine == -1)[0]
             if len(moveSteps) >= 1:
                 moveSteps = int(moveSteps[0])
                 grid[cRow:cRow+moveSteps,cCol] = 1
                 cRow = cRow+moveSteps-1
             else:
                 grid[cRow::,cCol] = 1
                 guardOnGrid = False

        elif direction == 3: # move left
             moveLine = grid[cRow,cCol::-1]
             moveSteps = np.where(moveLine == -1)[0]
             if len(moveSteps) >= 1:
                 moveSteps = int(moveSteps[0])
                 grid[cRow,cCol:cCol-moveSteps:-1] = 1
                 cCol = cCol-moveSteps+1
             else:
                 grid[cRow,cCol::-1] = 1
                 guardOnGrid = False
        
        # count number of covered spaces
        gridFlat = grid.ravel()
        nSpaces = len(np.where(gridFlat == 1)[0]) 
        
        # update guard state and check if guard is in loop
        direction = (direction+1)%4  # turn 90 degrees
        matches = [i for i,state in enumerate(guardStates) if state == [direction,cRow,cCol]]
        if len(matches) > 0:
            guardInLoop = True
        else:
            guardStates.append([direction,cRow,cCol])
        
        # # show movement animation
        # plt.imshow(grid)
        # time.sleep(0.01)
        # plt.show()
        
    return nSpaces, grid, guardInLoop
             
    
#%%# read input file #%%#
with open('2024/day6.txt') as file:
    lines = [line.rstrip() for line in file]
nRows = len(lines)
nCols = len(lines[0])

# convert input to numpy matrix    
grid = np.zeros([nRows,nCols])
for i in range(nRows):
    for j in range(nCols):
        if lines[i][j] == '#':   grid[i][j] = -1
        elif lines[i][j] == '^': 
            print(i,j)
            grid[i,j] = 1      

# plt.imshow(grid)
# time.sleep(0.01)
# plt.show()
            
#%%%# Part 1 #%%#
resultsPart1, solvedGrid, guardInLoop = moveGuard(grid)
print('Part 1: '+ str(resultsPart1))

#%%%# Part 2 #%%#75 70
solvedGrid[69,74] = 2 # mark starting point
resultsPart2 = 0
t0 = time.time()
for i in range(nRows):
    for j in range(nCols):
        if solvedGrid[i,j] == 1:
            newGrid = np.array(grid, copy=True)
            newGrid[i,j] = -1
            _, _, guardInLoop = moveGuard(newGrid)
            if guardInLoop: resultsPart2 += 1
tEnd = time.time()
tTotal = tEnd-t0
print(tTotal)            

print('Part 2: '+ str(resultsPart2))