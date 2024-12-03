from aoc import *
import math
symap = {
    'F': '┌',
    '7': '┐',
    'L': '└',
    'J': '┘',
    '|': '│',
    '-': '─',
    '.': ' ',
}

test = False
data = load(10,2023,test)#.replace(symap)
M = Matrix(data.split().tolist())
W = len(data[0])
H = data.len

class Network:
    
    def __init__(self):
        self.nodes = []
        self.setnodes = set()
        self.conn = dict()
        
    def add_node(self, node) -> int:
        if node[:2] in self.setnodes:
            i, oldnode = [(i,n) for i, n in enumerate(self.nodes) if n[:2] == node[:2]][0]
            if node[-1] < oldnode[-1]:
                self.nodes[i] = node
            return i
        i = len(self.nodes)
        self.nodes.append(node)
        self.setnodes.add(node[:2])
        self.conn[i] = []
        return i
    
    def __getitem__(self, slice):
        return self.conn[slice]
    
    def __setitem__(self, key, value):
        self.conn[key] = value
    
    def inside(self, row, col):
        return self.Rinside(row,col) and self.Uinside(row,col)# and self.Binside(row,col) and self.Linside(row,col)
    
        if (row,col) in self.setnodes:
            return False
        ccounter = 0
        for ic in range(col+1,W):
            if (row,ic) in self.setnodes and M[row,ic] in ['7','|','F','J','L','S']:
                ccounter += 1
        if (ccounter % 2 )==1:
            return True
        return False
    
    def Rinside(self, row, col):
        if (row,col) in self.setnodes:
            return False
        ccounter = 0
        for ic in range(col+1,W):
            if (row,ic) in self.setnodes and M[row,ic] in ['7','|','F','J','L','S']:
                ccounter += 1
        if (ccounter % 2 )==1:
            return True
        return False
    
    def Linside(self, row, col):
        if (row,col) in self.setnodes:
            return False
        ccounter = 0
        for ic in range(0,col-1):
            if (row,ic) in self.setnodes and M[row,ic] in ['7','|','F','J','L','S']:
                ccounter += 1
        if (ccounter % 2 )==1:
            return True
        return False
    
    def Uinside(self, row, col):
        if (row,col) in self.setnodes:
            return False
        ccounter = 0
        for ir in range(row+1,H):
            if (ir,col) in self.setnodes and M[ir,col] in ['7','-','F','J','L','S']:
                ccounter += 1
        if (ccounter % 2 )==1:
            return True
        return False
    
    def Binside(self, row, col):
        if (row,col) in self.setnodes:
            return False
        ccounter = 0
        for ir in range(0,row-1):
            if (ir,col) in self.setnodes and M[ir,col] in ['7','-','F','J','L','S']:
                ccounter += 1
        if (ccounter % 2 )==1:
            return True
        return False
        


N = Network()
r, c = M.find('S')

startpt = (r,c)
print('Startpoint =',startpt)
visited = {startpt,}

tovisit = []
cur = startpt + (0,'S')

while True:
    ic = N.add_node(cur)
    r,c,n,S = cur
    visited.add((r,c))
    
    
    A, B, L, R = M.above(r,c), M.below(r,c), M.left(r,c), M.right(r,c)
    if A in ['F','7','|','S'] and M[r,c] in ['L','J','|','S']:
        tovisit.append((r-1,c,n+1,A))
        i = N.add_node((r-1,c,n+1,A))
        N[ic].append(i)
    if B in ['J','|','L','S'] and M[r,c] in ['F','7','|','S']:
        tovisit.append((r+1,c,n+1,B))
        i = N.add_node((r+1,c,n+1,B))
        N[ic].append(i)
    if L in ['L','F','-','S'] and M[r,c] in ['7','J','-','S']:
        tovisit.append((r,c-1,n+1,L))
        i = N.add_node((r,c-1,n+1,L))
        N[ic].append(i)
    if R in ['7','J','-','S'] and M[r,c] in ['L','F','-','S']:
        tovisit.append((r,c+1,n+1,R))
        i = N.add_node((r,c+1,n+1,R))
        N[ic].append(i)

    
            
    tovisit = [p for p in tovisit if p[:2] not in visited]
    #for p in tovisit:
    #    i = N.add_node(p)
    #    if i not in N[ic]:
    #        N[ic].append(i)
    #print(tovisit)
    
    
    if not tovisit:
        break
    
    cur = tovisit[0]
    tovisit = tovisit[1:]
    
print(f'Part 1 = {max([n[2] for n in N.nodes])}')

## Part 2
print(N.conn)
loop = [0,]
while True:
    i = loop[-1]
    a,b = N.conn[i]
    if b not in loop:
        loop.append(b)
        continue
    if a not in loop:
        loop.append(a)
        continue
    break
print(loop)
CC = [N.nodes[i][:2] for i in loop]
CC.append(CC[0])
print(CC)
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
A = PolyArea(*zip(*CC))

LA = 0
for n in loop:
    sym = N.nodes[n][-1]
    print(sym)
    if sym=='F':
        LA += 0.25
    if sym=='L':
        LA += 0.25
    if sym=='7':
        LA += 0.75
    if sym=='J':
        LA += 0.75
    if sym in ['|','-']:
        LA += 0.5

print(f'Area = {A}, length = {math.ceil(LA)}, Area = {A-math.ceil(LA)+1}')
## Part 2
nodes = set([n[:2] for n in N.nodes])

A = 0
M2 = Matrix(data.split().replace(symap).tolist())
for c in range(W):
    for r in range(H):
        if N.inside(r,c):
            A += 1
            M2.dt[r][c] = 'X'
print('\n'.join([''.join(row) for row in M2.dt]))
            
print(f'Part 2 area = {A}')

