from aoc import *

######## PART 1 #######
data = load(16,2023,test=False).split().tomatrix().pad(1,'#')
STOP = (-1,-1,-1,-1)

mirror = {
    '\\': {
        (1,0): (0,1),
        (0,1): (1,0),
        (0,-1): (-1,0),
        (-1,0): (0,-1),
    },
    '/': {
        (1,0): (0,-1),
        (0,1): (-1,0),
        (-1,0): (0,1),
        (0,-1): (1,0)
    }
}
splitter = {
    '|': {
        (1,0): (0,1,0,-1),
        (-1,0): (0,1,0,-1),
        (0,1): (0,1),
        (0,-1): (0,-1),
    },
    '-':{
        (1,0): (1,0),
        (-1,0): (-1,0),
        (0,1): (-1,0,1,0),
        (0,-1):(-1,0,1,0)
        }
}
current_path = [(-1,0,1,0)]
new_paths = []
finished_paths = []
past_dirs = set()
while current_path:
    while True:
        x,y,dx,dy = current_path[-1]
        nx, ny = x+dx, y+dy
        object = data[ny+1][nx+1]
        if object in mirror:
            dxn, dyn = mirror[object][(dx,dy)]
            newstate = (nx,ny,dxn,dyn)
            if newstate not in past_dirs:
                past_dirs.add(newstate)
                current_path.append((nx,ny,dxn,dyn))
            else:
                current_path.append(STOP)
            continue
        elif object in splitter:
            if len(splitter[object][(dx,dy)])==4:
                (dx1, dy1,dx2, dy2) = splitter[object][(dx,dy)]
                newstate = (nx,ny,dx2,dy2)
                newstate2 = (nx,ny,dx1,dy1)
                if newstate not in past_dirs:
                    new_paths.append([newstate])
                    past_dirs.add(newstate)
                if newstate2 not in past_dirs:
                    current_path.append(newstate2)
                    past_dirs.add(newstate2)
                else:
                    current_path.append(STOP)
                continue
            else:
                current_path.append((nx,ny,dx,dy))
                continue
        elif object == '#':
            current_path.append(STOP)
        else:
            current_path.append((nx,ny,dx,dy))
            continue
        if current_path[-1] == STOP:
            finished_paths.append(current_path)
            break
    if not new_paths:
        break
    else:
        current_path = new_paths.pop(0)
         
counter = 0
locations = set()
for path in finished_paths:
    for x, y,dx,dy in path:
        if (x,y,dx,dy) == STOP:
            continue
        locations.add((x,y))
        
        
print(f'Solution to part 1: {len(locations)-1}')

######## PART 2 #######

def try_path(start_state: tuple):
    current_path = [start_state]
    new_paths = []
    finished_paths = []
    past_dirs = set()
    while True:
        while True:
            x,y,dx,dy = current_path[-1]
            nx, ny = x+dx, y+dy
            object = data[ny+1][nx+1]
            if object in mirror:
                dxn, dyn = mirror[object][(dx,dy)]
                newstate = (nx,ny,dxn,dyn)
                if newstate not in past_dirs:
                    past_dirs.add(newstate)
                    current_path.append((nx,ny,dxn,dyn))
                else:
                    current_path.append(STOP)
                continue
            elif object in splitter:
                if len(splitter[object][(dx,dy)])==4:
                    (dx1, dy1,dx2, dy2) = splitter[object][(dx,dy)]
                    newstate = (nx,ny,dx2,dy2)
                    newstate2 = (nx,ny,dx1,dy1)
                    if newstate not in past_dirs:
                        new_paths.append([newstate])
                        past_dirs.add(newstate)
                    if newstate2 not in past_dirs:
                        current_path.append(newstate2)
                        past_dirs.add(newstate2)
                    else:
                        current_path.append(STOP)
                    continue
                else:
                    current_path.append((nx,ny,dx,dy))
                    continue
            elif object == '#':
                current_path.append(STOP)
            else:
                current_path.append((nx,ny,dx,dy))
                continue
            if current_path[-1] == STOP:
                finished_paths.append(current_path)
                break
        if not new_paths:
            break
        else:
            current_path = new_paths.pop(0)
            
    locations = set()
    for path in finished_paths:
        for x, y,dx,dy in path:
            locations.add((x,y))
    return len(locations)-2

print(try_path((-1,0,1,0)))
W = data.width-2
H = data.height-2
maxL = 0

for i in range(W):
    maxL = max(maxL, try_path((i,-1,0,1)))
for i in range(W):
    maxL = max(maxL, try_path((i,W+1,0,-1)))
for i in range(H):
    maxL = max(maxL, try_path((-1,i,1,0)))
for i in range(H):
    maxL = max(maxL, try_path((H+1,i,-1,0)))
print(f'Solution to part 2: {maxL}')

    