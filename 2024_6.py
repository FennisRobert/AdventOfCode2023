from aoc import *
from tqdm import tqdm
######## PART 1 #######
data = load(6,2024,test=False).split().tomatrix().pad(1,'F').replace({'.':''})

guard = [(i,j) for i in range(data.width) for j in range(data.height) if data[j][i]=='^'][0]

x,y = guard
dx,dy = 0,-1
counter = 1

havebeen = set([(x,y)])

path_states = list()

rotations = []
while True:
    
    nx, ny = x+dx, y+dy
    if data[ny][nx]=='F':
        break
    elif data[ny][nx]=='#':
        dx, dy = -dy, dx
        rotations.append((x,y))
        continue
    else:
        path_states.append((x,y,dx,dy))
        x,y = nx, ny
        if not (x,y) in havebeen:
            counter += 1
            havebeen.add((x,y))

print(f'Solution to part 1: {counter}')

######## PART 2 #######

import numpy as np
mapper = {
    '': 0,
    '#': 1,
    'F': 2,
    '^': 0
}
data = np.array([[mapper[x] for x in row] for row in data.dt])

coords = [(x,y) for x,y,_,_ in path_states]
coords_check = set(coords)
loop_options = set()

for x0,y0,dx0,dy0 in tqdm(path_states):
    
    testfield = 1*data
    
    testfield[y0+dy0,x0+dx0] = 1
    # Start 2 steps earlier than the first occurance of the block location if the block is in the path. 
    if (x0+dx0,y0+dy0) in coords_check:
        x,y,dx,dy = path_states[coords.index((x0+dx0,y0+dy0))-2]
    else:
        x,y = guard
        dx,dy = 0,-1
    
    havebeen = set()
    while True:
        nx, ny = x+dx, y+dy
        
        if (x,y,dx,dy) in havebeen:
            loop_options.add((x0+dx0,y0+dy0))
            break
        
        havebeen.add((x,y,dx,dy))
        if testfield[ny,nx]==2:
            break
        elif testfield[ny,nx]==1:
            dx, dy = -dy, dx
            continue
        else:
            x,y = nx, ny

print(f'Solution to part 2: {len(loop_options)}')

    