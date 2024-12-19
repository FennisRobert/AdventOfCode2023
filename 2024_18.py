from aoc import *
from collections import defaultdict
import numpy as np


######## PART 1 #######
blocks = load(18,2024,test=False).split(',').toint()

W,H = 71,71

data = Matrix([[' ' for _ in range(W)] for _ in range(H)])

N = 1024

for x,y in blocks[:N]:
    data.dt[y][x] = '#'


start = (0,0)
end = (W,H)

def get_options(point: tuple[int,int], excludeset: set) -> list[int,int,int]:
    x,y = point
    newxy = []
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx,ny = x+dx,y+dy
        
        if not ((0 <= nx < W) and (0 <= ny < H)):
            continue
        if data[ny][nx] == '#' or (nx,ny) in excludeset:
            continue
        newxy.append(((nx,ny),1))
    return newxy

deffunc = lambda: (np.inf, [])
explored = dict()
unexplored = defaultdict(deffunc)
explored[start] = (0, [start,])


pos = start
cost = 0
path = [start,]
while True:
    for newpos, dcost in get_options(pos, explored):
        if dcost+cost < unexplored[newpos][0]:
            unexplored[newpos] = (dcost+cost, path+[newpos,])
    
    #print(unexplored)
    if len(unexplored)==0:
        break
    
    newposition = min(unexplored, key=lambda x: unexplored[x][0])
    explored[newposition] = unexplored[newposition]
    cost, path = unexplored[newposition]
    pos = newposition
    del unexplored[pos]
    
    if (W,H) in explored:
        break
    
    
fpath = None
for pos, (cost, path) in explored.items():
    if pos==(70,70):
        fpath = path
        break
print(fpath)
print(data.tostring(71,71,nospace=True,mark=(fpath,'O')))

print(f'Solution to part 1: {len(fpath)-1}')

######## PART 2 #######

N = 1024

for i in range(1,len(blocks)-1):
    
    newx,newy = blocks[N+i]
    data.dt[newy][newx] = '#'
    print(newx,newy)

    deffunc = lambda: (np.inf, [])
    explored = dict()
    unexplored = defaultdict(deffunc)
    explored[start] = (0, [start,])

    pos = start
    cost = 0
    path = [start,]
    while True:
        for newpos, dcost in get_options(pos, explored):
            if dcost+cost < unexplored[newpos][0]:
                unexplored[newpos] = (dcost+cost, path+[newpos,])
        
        #print(unexplored)
        if len(unexplored)==0:
            break
        
        newposition = min(unexplored, key=lambda x: unexplored[x][0])
        explored[newposition] = unexplored[newposition]
        cost, path = unexplored[newposition]
        pos = newposition
        del unexplored[pos]
        
        if (W,H) in explored:
            break
        
    if (70,70) not in explored:
        break

print(f'Not possible after {newx,newy}')
    