from aoc import *

######## PART 1 #######

pad = 4
data = load(4,2024,test=False).split().tomatrix().pad(pad,' ')



WORD = 'XMAS'

w = data.width
h = data.height
WL = len(WORD)
counter = 0

def inrange(xs, ys) -> bool:
    return all([0<=x<w for x in xs]) and all([0<=y<h for y in ys])

for ix,iy in [(i,j) for i in range(pad-1,w-pad) for j in range(pad-1,h-pad)]:
    #right
    I = list(range(ix,ix+WL))
    J = [iy for _ in range(WL)]
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        counter += 1
    #left
    I = list(range(ix,ix-WL,-1))
    J = [iy for _ in range(WL)]
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        counter += 1
    
    #down
    J = list(range(iy,iy+WL))
    I = [ix for _ in range(WL)]
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        counter += 1
    #up
    J = list(range(iy,iy-WL,-1))
    I = [ix for _ in range(WL)]
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        counter += 1
            
    #rightdown
    I = list(range(ix,ix+WL))
    J = list(range(iy,iy+WL))
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        counter += 1
    
    #rightup
    I = list(range(ix,ix+WL))
    J = list(range(iy,iy-WL,-1))
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        counter += 1
    
    #leftup
    I = list(range(ix,ix-WL,-1))
    J = list(range(iy,iy-WL,-1))
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        counter += 1

    #leftdown
    I = list(range(ix,ix-WL,-1))
    J = list(range(iy,iy+WL))
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        counter += 1
        
print(data.tostring())

print(f'Solution to part 1: {counter}')

######## PART 2 #######
pad = 1
data = load(4,2024,test=False).split().tomatrix().pad(pad,' ')


WORD = 'MAS'

w = data.width
h = data.height
WL = len(WORD)
counter = 0

def inrange(xs, ys) -> bool:
    return all([0<=x<w for x in xs]) and all([0<=y<h for y in ys])

for ix,iy in [(i,j) for i in range(pad-1,w-pad) for j in range(pad-1,h-pad)]:
    hits = 0
    #rightdown
    I = list(range(ix-1,ix+2))
    J = list(range(iy-1,iy+2))
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        hits+=1
    
    #rightup
    I = list(range(ix-1,ix+2))
    J = list(range(iy+1,iy-2,-1))
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        hits += 1
    
    #leftup
    I = list(range(ix+1,ix-2,-1))
    J = list(range(iy+1,iy-2,-1))
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        hits += 1

    #leftdown
    I = list(range(ix+1,ix-2,-1))
    J = list(range(iy-1,iy+2))
    word = data.sample(I,J)
    if ''.join(word) == WORD:
        hits += 1
    counter += int(np.floor(hits//2))
print(data.tostring())

print(f'Solution to part 2: {counter}')
