from aoc import *

######## PART 1 #######
orig = load(17,2023,test=True).split().toint().tomatrix()
data = orig.pad(1,99)

print(data.tostring())

def neighbors(x,y):
    xs = [x+i for i in [-1,0,1,0]]
    ys = [y+i for i in [0,1,0,-1]]
    return [(X,Y) for X,Y in zip(xs,ys) if data[Y+1][X+1] != 99]


W = data.width-2
H = data.height-2

unexplored = {(i,j): (200,[]) for i in range(W) for j in range(H)}
explored = {}

unexplored[(0,0)] = (data[1][1],[(0,0)])

viewer = Matrix([[999 for _ in range(W)] for _ in range(H)])

def pickmin(unex: dict):
    return min(unex, key=lambda x: unex[x][0])

path = []
while unexplored:
    current = pickmin(unexplored)
    currentval,path = unexplored[current]
    nodes = neighbors(*current)
    options = [(x,y,data[y+1][x+1]) for x,y in nodes if (x,y) not in explored and (x,y) not in path]
    touched = []
    for x,y,value in options:
        
        if len(path) > 2:
            proposed_path = path[-3:] + [(x,y),]
            print(proposed_path)
            deltas = [(x2-x1,y2-y1) for (x1,y1),(x2,y2) in zip(proposed_path[:-1],proposed_path[1:])]
            print(deltas)
            if deltas[0]==deltas[1]==deltas[2]:
                continue
        unexplored[(x,y)] = min(unexplored[(x,y)],(value+currentval,path+[(x,y)]), key=lambda x: x[0])
        viewer[y][x] = unexplored[(x,y)][0]
    unexplored.pop(current)
    explored[current] = (currentval, path)
    viewer[current[1]][current[0]] = currentval
    print(viewer.tostring(mark=(path,'x')))
    input('')

value,shortestpath = explored[(W-1,H-1)]
print(shortestpath)
print(viewer.tostring(mark=(shortestpath[:-1],'x')))
print(f'Solution to part 1: {None}')

######## PART 2 #######
data = load(17,2023,test=True)

print(data)

print(f'Solution to part 2: {None}')

    