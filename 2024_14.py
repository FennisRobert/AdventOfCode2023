from aoc import *

######## PART 1 #######
test = False
data = load(14,2024,test=test).findgroups(r'([+-]?\d+)').toint()

W = 101
H = 103
if test:
    W = 11
    H = 7

pos = []
N = 100
for line in data:
    x, y, vx, vy = line
    x2 = (x+N*vx)%W
    y2 = (y+N*vy)%H
    pos.append((x2,y2))

M = np.zeros((H,W))

for x,y in pos:
    M[y,x] += 1

Q1 = M[:H//2, :W//2]
Q2 = M[H//2+1:, :W//2]
Q3 = M[H//2+1:, W//2 +1:]
Q4 = M[:H//2, W//2 +1:]

ans = np.prod([np.sum(x.flatten()) for x in [Q1, Q2, Q3, Q4]])
print(f'Solution to part 1: {ans}')

######## PART 2 #######
data = load(14,2024,test=True)
import matplotlib.pyplot as plt

data = load(14,2024,test=test).findgroups(r'([+-]?\d+)').toint()

# 12  88 113 191
W = 101
H = 103

pos = []
N = 100
Nframes = 200000
robots = []
for line in data:
    x, y, vx, vy = line
    robots.append((x,y,vx,vy))

fig, ax = plt.subplots(1,1)

field = np.zeros((W,H))
M = Matrix([[' ' for _ in range(W)] for _ in range(H)])
zeros = np.zeros((H,W))
for i in range(Nframes):
    M = 0*zeros
    for x,y,vx,vy in robots:
        M[y,x] += 1
    #p
    if max(M.flatten())==1:
        coords = [(x,y) for x,y,a,b in robots]
        M = Matrix([[' ' for _ in range(W)] for _ in range(H)])
        print(M.tostring(W,H,mark=(coords,'X'),nospace=True))
        input(f'{i}')
    for i, rob in enumerate(robots):
        x,y,vx,vy = rob
        x2 = (x+1*vx)%W
        y2 = (y+1*vy)%H
        
        
        robots[i] = (x2,y2,vx,vy)
    
    