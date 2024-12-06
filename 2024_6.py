from aoc import *
from tqdm import tqdm
######## PART 1 #######
data = load(6,2024,test=False).split().tomatrix().pad(1,'F')

viewer = data.copy()

guard = [(i,j) for i in range(data.width) for j in range(data.height) if data[j][i]=='^'][0]

x,y = guard
dx,dy = 0,-1
counter = 1
viewer[y][x] = 'X'
havebeen = set([(x,y)])

xydxdys = list()

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
        xydxdys.append((x,y,dx,dy))
        x,y = nx, ny
        viewer[ny][nx] = 'X'
        if not (x,y) in havebeen:
            counter += 1
            havebeen.add((x,y))
    
    #print(viewer.tostring())
print(viewer.tostring())

print(f'Solution to part 1: {counter}')

######## PART 2 #######

viewer = Matrix(data.dt)

loop_options = list()
for x0,y0,dx0,dy0 in tqdm(xydxdys):
    
    testfield = data.copy()
    
    
    testfield.dt[y0+dy0][x0+dx0] = '#'
    viewer = testfield.copy()
    
    x,y = guard
    dx,dy = 0,-1
    #x,y,dx,dy = xydxdys[i]
    havebeen = set()
    while True:
        nx, ny = x+dx, y+dy
        
        if (x,y,dx,dy) in havebeen:
            loop_options.append((x0+dx0,y0+dy0))
            #print(viewer.tostring())
            #input('')
            break
        
        havebeen.add((x,y,dx,dy))
        if testfield[ny][nx]=='F':
            break
        elif testfield[ny][nx]=='#':
            dx, dy = -dy, dx
            rotations.append((x,y))
            continue
        else:
            x,y = nx, ny
            viewer[ny][nx] = 'X'
            
        
        #print(viewer.tostring())
        #input('')
print(viewer.tostring())
loop_options = set(loop_options)
print(loop_options)
print(f'Solution to part 2: {len(loop_options)}')

    