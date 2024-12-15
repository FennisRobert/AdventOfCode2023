from aoc import *
import numpy as np

######## PART 1 #######
if False:
    world, instr = load(15,2024,test=False).symbgroup()
    world = world.split().tomatrix()

    user = world.find('@')[0]
    ids = world.find('O')
    wall = world.find('#')
    W = world.width
    H = world.height

    wld = np.zeros((W,H))
    for x,y in wall:
        wld[x,y] = -1
    for x,y in ids:
        wld[x,y] = 1

    def plotworld(pos, world):
        wp = Matrix([[' ' for _ in range(W)] for _ in range(H)])
        for x,y in [(x,y) for x in range(W) for y in range(H)]:
            if wld[x,y]==-1:
                wp.dt[y][x] = '#'
            if wld[x,y]==[1]:
                wp.dt[y][x] = 'O'
        x,y = pos
        wp.dt[y][x] = '@'
        print(wp.tostring())
        
    def move_user(pos: tuple, world: np.ndarray, direction: str):
        x,y = pos
        if direction == '>':
            idw = np.argwhere(world[x+1:,y] == -1)[0][0] + x+1
            idsel = np.argwhere(world[x+1:idw, y]==0) + x+1
            if idsel.shape[0]==0: # Can't move because there is no free position in principle
                #print('cant move right')
                return pos, world
            tfid = idsel[0][0]
            world[x+1:tfid+1,y] = world[x:tfid,y]
            world[x,y] = 0
            pos = (x+1,y)
            return pos,world
        if direction == 'v':
            idw = np.argwhere(world[x, y+1:] == -1)[0][0] + y+1
            idsel = np.argwhere(world[x, y+1:idw] == 0) + y+1
            if idsel.shape[0]==0: # Can't move because there is no free position in principle
                #print('cant move down')
                return pos, world
            tfid = idsel[0][0]
            world[x,y+1:tfid+1] = world[x,y:tfid]
            world[x,y] = 0
            pos = (x,y+1)
            return pos,world
        if direction == '<':
            idw = np.argwhere(world[:x,y] == -1)[-1][0]
            idsel = np.argwhere(world[idw:x,y]==0) + idw
            if idsel.shape[0]==0: # Can't move because there is no free position in principle
                #print('cant move left')
                return pos, world
            tfid = idsel[-1][0]
            world[tfid:x,y] = world[tfid+1:x+1,y]
            world[x,y] = 0
            pos = (x-1,y)
            return pos,world
        if direction == '^':
            idw = np.argwhere(world[x,:y] == -1)[-1][0]
            idsel = np.argwhere(world[x,idw:y]==0) + idw
            if idsel.shape[0]==0: # Can't move because there is no free position in principle
                #print('cant move up')
                return pos, world
            tfid = idsel[-1][0]
            world[x,tfid:y] = world[x,tfid+1:y+1]
            world[x,y] = 0
            pos = (x,y-1)
            return pos,world
        raise Exception('This is not supposed to happen')
        
    instr = ''.join(instr.tolist())
    plotworld(user,wld)
    for i in instr:
        user, wld = move_user(user, wld, i)
        #plotworld(user,wld)
        #print(i)
        #input('')
    plotworld(user,wld)
    score = 0
    for x,y in [(x,y) for x in range(W) for y in range(H)]:
        if wld[x,y]==1:
            score+=100*y+x
    print(f'Solution to part 1: {score}')

    ######## PART 2 #######
world, instr = load(15,2024,test=False).symbgroup()
world = world.split().tomatrix()

user = world.find('@')[0]
ids = world.find('O')
wall = world.find('#')
W = world.width
H = world.height


class Block:
    
    def __init__(self, x: int, y: int, i):
        self.x = x
        self.y = y
        self.i = i
    
    @property
    def score(self):
        return self.x + 100*self.y
    def __repr__(self) -> str:
        return f'Block[{self.i}]'
    @property
    def xys(self):
        return self.x, self.y, self.x+1, self.y

    def __hash__(self):
        return self.i
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        
    def blank(self, world):
        world[self.x, self.y] = 0
        world[self.x+1, self.y] = 0
        return world
    
    def write(self, world):
        world[self.x, self.y] = self.i
        world[self.x+1, self.y] = self.i
        return world
    
blocks = dict()
wld = np.zeros((W*2,H))
for x,y in wall:
    wld[x*2,y] = -1
    wld[x*2+1,y] = -1
for i, (x,y) in enumerate(ids):
    wld[x*2,y] = i+1
    wld[x*2+1,y] = i+1
    blocks[i+1] = Block(x*2,y,i+1)
    
px, py = 2*user[0], user[1]

def plotworld(pos, world, blocks: dict[int, Block]):
    wp = Matrix([[' ' for _ in range(W*2)] for _ in range(H)])
    for x,y in [(x,y) for x in range(W*2) for y in range(H)]:
        if wld[x,y]==-1:
            wp.dt[y][x] = '#'
    for b in blocks.values():
        x1, y1, x2, y2 = b.xys
        wp.dt[y1][x1] = '['
        wp.dt[y2][x2] = ']'
    x,y = pos
    wp.dt[y][x] = '@'
    print(wp.tostring(2*W,H,nospace=True))
    
def find_movement(x: int, y: int, wld: np.ndarray, dr:str, moved: set, blocks: dict[int, Block]):
   #print(f'Looking at {x},{y},{dr}')
    if dr=='>':
        xn, yn = x+1,  y
    elif dr=='v':
        xn, yn = x, y+1
    elif dr=='<':
        xn, yn = x-1, y
    elif dr=='^':
        xn, yn = x, y-1
        
    if wld[xn,yn]==-1:
        return False, moved
    elif wld[xn,yn]==0:
        return True, moved
    else:
        blck = blocks[wld[xn,yn]]
        print(f'Found block {blck}')
        x1, y1, x2, y2 = blck.xys
        if dr=='<':
            return find_movement(x1, y1, wld, dr, moved.union({blck,}), blocks)
        if dr=='>':  
            return find_movement(x2, y2, wld, dr, moved.union({blck,}), blocks)
        else:
            cm1, moved1 = find_movement(x1, y1, wld, dr, moved.union({blck,}), blocks)
            cm2, moved2 = find_movement(x2, y2, wld, dr, moved.union({blck,}), blocks)
            if cm1 is True and cm2 is True:
                moved = moved1.union(moved2)
                return True, moved
            return False, moved

instr = ''.join(instr.tolist())
dxy = {
    '>': (1,0),
    'v': (0,1),
    '<': (-1,0),
    '^': (0,-1)
}
plotworld((px,py),wld,blocks)
for i in instr:
    canmove, moved = find_movement(px,py, wld, i, set(), blocks)
    if canmove:
        dx, dy = dxy[i]
        px, py = px+dx, py+dy
        for b in moved:
            wld = b.blank(wld)
        for b in moved:
            b.move(dx,dy)
        for b in moved:
            wld = b.write(wld)
    
    # plotworld((px,py),wld,blocks)
    # print(i)
    # input('')
plotworld((px,py),wld,blocks)

score = sum([b.score for b in blocks.values()])

print(f'Solution to pt2 = {score}')