from aoc import *
from functools import reduce
data = load(11,2023,False)

emptycols = []
emptyrows = []

filledcols = []
for ir, line in enumerate(data):
    if not '#' in line:
        emptyrows.append(ir)
    filledcols.append(set([i for i,c in enumerate(line) if c=='#']))

emptycols = [i for i in range(len(data[0])) if i not in reduce(lambda a,b: a.union(b), filledcols)]

newuniverse = []
NC = len(data[0])+len(emptycols)

for ir, line in enumerate(data):
    newline = ''
    for ic, c in enumerate(line):
        newline += c
        if ic in emptycols:
            newline += '.'
    newuniverse.append(newline)
    if ir in emptyrows:
        newuniverse.append('.'*NC)

print('\n'.join(newuniverse))
universes = []
for ir, line in enumerate(newuniverse):
    for ic, c in enumerate(line):
        if c=='#':
            universes.append((ir,ic))

sumV = 0
npairs = 0
for i1, u1 in enumerate(universes[:-1]):
    for i2, u2 in enumerate(universes[i1+1:]):
        npairs += 1
        #print(i1+1, i2+i1+2, abs(u2[1]-u1[1])+abs(u2[0]-u1[0]), u1, u2)
        sumV += abs(u2[1]-u1[1])+abs(u2[0]-u1[0])
print(f'Part 1 solution: {sumV}')

## part 2 use the simpler solution obviously

newuniverse = [line for line in data]

universes = []
for ir, line in enumerate(newuniverse):
    for ic, c in enumerate(line):
        if c=='#':
            universes.append((ir,ic))

extra = 1000000-1
sumV = 0
npairs = 0
for i1, u1 in enumerate(universes[:-1]):
    for i2, u2 in enumerate(universes[i1+1:]):
        npairs += 1
        sumV += abs(u2[1]-u1[1])+abs(u2[0]-u1[0])
        for ic in emptycols:
            if min(u1[1],u2[1]) < ic < max(u1[1],u2[1]):
                sumV += extra
        for ir in emptyrows:
            if min(u1[0],u2[0]) < ir < max(u1[0],u2[0]):
                sumV += extra
               
print(f'Part 2 solution: {sumV}')