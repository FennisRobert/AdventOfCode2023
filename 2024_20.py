from aoc import *
import numpy as np
from collections import defaultdict
import tqdm
import numba as nb
######## PART 1 #######
data = load(20,2024,test=False).split().tomatrix()

walls = data.find('#')
route = data.find('.')
start = data.find('S')[0]
end = data.find('E')[0]

## Generate the path of the race track
dist = lambda a,b: abs(b[0]-a[0]) + abs(b[1]-a[1])

path = [start,]
options = [r for r in route]
while options:
    last = path[-1]
    nxt = None
    for o in options:
        if dist(o,last)>1:
            continue
        nxt = o
        break
    path.append(nxt)
    options.remove(nxt)

path.append(end)

for i,p in enumerate(path):
    x,y = p
    data.dt[y][x] = i

possible_leaps = defaultdict(int)
stored_leaps = defaultdict(list)
for i,p in enumerate(tqdm.tqdm(path)):
    x,y = p
    step = data[y][x]
    for jx, jy in [(1,0),(-1,0),(0,1),(0,-1)]:
        if not data.inside(x+2*jx,y+2*jy):
            continue
        dest = data[y+2*jy][x+2*jx]
        inter = data[y+jy][x+jx]
        if isinstance(dest,int) and inter=='#':
            possible_leaps[dest-step - 2] += 1
            stored_leaps[dest-step-2].append((p,(x+jx,y+jy),(x+2*jx,y+2*jy)))
            

total = 0
for key,value in possible_leaps.items():
    if key>=100:
        total += value
        


print(f'Solution to part 1: {total}')

######## PART 2 #######

# data = load(20,2024,test=True).split().tomatrix()
# data = data.replace({'.': 0, '#': 1, 'S': 0, 'E': 1})

# mp = np.array(data.dt)

# print(mp)

nppath = np.array(path)

@nb.njit
def compute_leaps(path):
    N = path.shape[0]
    possible_leaps = np.zeros((N,)).astype(np.int64)
    I = 100
    for i1 in range(N-I):
        p1 = path[i1]
        for i2 in range(i1+1,N):
            p2 = path[i2]
            x1, y1 = p1
            x2, y2 = p2
            mhdist = abs(x2-x1)+abs(y2-y1)
            if mhdist > 20:
                continue
            if i2-i1-mhdist > 0:
                possible_leaps[i2-i1-mhdist] += 1
    return possible_leaps

total = 0
leaps = compute_leaps(nppath)

print(f'Solution to part 2: {np.sum(leaps[100:])}')

#42298115 was too high
#1009299