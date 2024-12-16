from aoc import *
from collections import defaultdict
import numpy as np
######## PART 1 #######
data = load(16,2024,test=False).split().tomatrix()


W, H = data.dims 
S = data.find('S')[0]
E = data.find('E')[0]
ends = [(E[0],E[1],1+0j),(E[0],E[1],-1+0j),(E[0],E[1],0+1j),(E[0],E[1],0-1j)]
state = (S[0], S[1], 1)

rotcost = {
    1+0j: 1,
    0+1j: 1001,
    0-1j: 1001,
    -1: 10000001,
}

walls = set(data.find('#'))

def get_routes(state: tuple[int, int, complex], explored: dict):
    x, y, r = state
    options = []
    for dr in [1., 1j, -1j, -1]:
        xn = int(x + dr.real)
        yn = int(y + dr.imag)
        cost = rotcost[dr/r]
        if dr/r == -1:
            continue
        if not (xn,yn) in walls:
            options.append(((xn,yn,dr),cost))
    return options

definit = lambda: (np.inf, [tuple(),])

route = [(state,)]

curstate, curroute, curcost = state, route, 0

explored = defaultdict(definit)
explored[curstate] = (curcost, curroute)
unexplored = defaultdict(definit)

while True:
    
    routeoptions = get_routes(curstate, explored)
    #print(routeoptions)
    for dest, cost in routeoptions:
        newcost = curcost + cost
        if dest in explored:
            continue
            #if newcost == explored[dest][0]:
            #    #print(explored[dest][1])
            #    explored[dest][1].extend([r + (dest,) for r in curroute ])
            #    continue
        if newcost < unexplored[dest][0]:
            unexplored[dest] = (newcost, [r + (dest,) for r in curroute ])
        elif newcost == unexplored[dest][0]:
            unexplored[dest][1].extend([r + (dest,) for r in curroute ])
            print('does this happend?')
        else:
            continue
        #unexplored.append((state[0]+cost,dest, state[2]+((dest),)))
    
    if len(unexplored)==0:
        break
    
    snext = min([key for key in unexplored.keys()], key=lambda x: unexplored[x][0])
    explored[snext] = unexplored[snext]
    #print(curcost, curstate)
    #input('')
    curstate, curroute, curcost = snext, explored[snext][1], explored[snext][0]
    
    del unexplored[curstate]


solutions = [sol for sol in explored.keys() if sol in ends]
print(solutions)
minkey = min(solutions, key=lambda x: explored[x][0])
print(solutions)

print(f'Solution to part 1: {explored[minkey][0]}')

blocks = set()
for route in explored[minkey][1]:
    nr = [(x,y) for x,y,_ in route]
    blocks = blocks.union(set(nr))


print(data.tostring(20,20,mark=(list(blocks),'x')))
print(len(blocks))