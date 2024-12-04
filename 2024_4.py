from aoc import *

######## PART 1 #######
data = load(4,2024,test=False).split().tomatrix()

WORD = 'XMAS'

w = data.width
h = data.height
WL = len(WORD)
counter = 0

def inrange(xs, ys) -> bool:
    return all([0<=x<w for x in xs]) and all([0<=y<h for y in ys])

for ix,iy in [(i,j) for i in range(w) for j in range(h)]:
    #right
    if ix <= w-WL:
        I = list(range(ix,ix+WL))
        J = [iy for _ in range(WL)]
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            counter += 1
    #left
    if ix >= WL-1:
        I = list(range(ix,ix-WL,-1))
        J = [iy for _ in range(WL)]
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            counter += 1
    
    #down
    if iy <= h-WL:
        J = list(range(iy,iy+WL))
        I = [ix for _ in range(WL)]
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            counter += 1
    #up
    if iy >= WL-1:
        J = list(range(iy,iy-WL,-1))
        I = [ix for _ in range(WL)]
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            counter += 1
            
    #rightdown
    I = list(range(ix,ix+WL))
    J = list(range(iy,iy+WL))
    if inrange(I,J):
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            counter += 1
    
    #rightup
    I = list(range(ix,ix+WL))
    J = list(range(iy,iy-WL,-1))
    if inrange(I,J):
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            counter += 1
    
    #leftup
    I = list(range(ix,ix-WL,-1))
    J = list(range(iy,iy-WL,-1))
    if inrange(I,J):
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            counter += 1

    #leftdown
    I = list(range(ix,ix-WL,-1))
    J = list(range(iy,iy+WL))
    if inrange(I,J):
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            counter += 1
        
print(data.tostring())

print(f'Solution to part 1: {counter}')

######## PART 2 #######
data = load(4,2024,test=False).split().tomatrix()

WORD = 'MAS'

w = data.width
h = data.height
WL = len(WORD)
counter = 0

def inrange(xs, ys) -> bool:
    return all([0<=x<w for x in xs]) and all([0<=y<h for y in ys])

for ix,iy in [(i,j) for i in range(w) for j in range(h)]:
    hits = 0
    #rightdown
    I = list(range(ix-1,ix+2))
    J = list(range(iy-1,iy+2))
    if inrange(I,J):
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            hits+=1
    
    #rightup
    I = list(range(ix-1,ix+2))
    J = list(range(iy+1,iy-2,-1))
    if inrange(I,J):
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            hits += 1
    
    #leftup
    I = list(range(ix+1,ix-2,-1))
    J = list(range(iy+1,iy-2,-1))
    if inrange(I,J):
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            hits += 1

    #leftdown
    I = list(range(ix+1,ix-2,-1))
    J = list(range(iy-1,iy+2))
    if inrange(I,J):
        word = data.sample(I,J)
        if ''.join(word) == WORD:
            hits += 1
    counter += np.floor(hits//2)
print(data.tostring())

print(f'Solution to part 2: {counter}')
