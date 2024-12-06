from aoc import *
from tqdm import tqdm
######## PART 1 #######
data = load(6,2024,test=False).split().tomatrix().pad(1,'F').replace({'.':''})

viewer = data.copy()

guard = [(i,j) for i in range(data.width) for j in range(data.height) if data[j][i]=='^'][0]

x,y = guard
dx,dy = 0,-1
counter = 1
viewer[y][x] = 'X'
havebeen = set([(x,y)])

path_states = list()

pss = {
    (0,1): '│',
    (1,0): '─',
    (0,-1): '│',
    (-1,0): '─',
}
rotpss = {
    (0,1): '┘',
    (1,0): '┐',
    (0,-1): '┌',
    (-1,0): '└',
}
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
        viewer[ny][nx] = pss[(dx,dy)]
        if not (x,y) in havebeen:
            counter += 1
            havebeen.add((x,y))
    
    #print(viewer.tostring())
print(viewer.tostring())

print(f'Solution to part 1: {counter}')

######## PART 2 #######

viewer = data.copy()

loop_options = set()
for x0,y0,dx0,dy0 in tqdm(path_states):
    
    testfield = data.copy()
    
    testfield.dt[y0+dy0][x0+dx0] = '#'
    #viewer = testfield.copy()
    
    x,y = guard
    dx,dy = 0,-1
    
    havebeen = set()
    while True:
        nx, ny = x+dx, y+dy
        
        if (x,y,dx,dy) in havebeen:
            loop_options.add((x0+dx0,y0+dy0))
            #print(viewer.tostring())
            break
        
        havebeen.add((x,y,dx,dy))
        if testfield[ny][nx]=='F':
            break
        elif testfield[ny][nx]=='#':
            #viewer[y][x] = rotpss[(dx,dy)]
            dx, dy = -dy, dx
            rotations.append((x,y))
            continue
        else:
            x,y = nx, ny
            #viewer[ny][nx] = pss[(dx,dy)]
            


print(f'Solution to part 2: {len(loop_options)}')

    