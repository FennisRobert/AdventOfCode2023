from aoc import *
import math

test = True
######## PART 1 #######
data = load(8,2024,test=test).split().tomatrix()

symbols = load(8,2024,test=test)
symbols = list(set(''.join(symbols.tolist())))
symbols.pop(symbols.index('.'))

ant_locations = {sym: data.find(sym) for sym in list(symbols)}

unique_locs = set()
processed = set()
for symbol, locs in ant_locations.items():
    for i, (x1,y1) in enumerate(locs):
        for jp, (x2,y2) in enumerate(locs[i+1:]):
            j=jp+i
            dx,dy = x2-x1, y2-y1
            unique_locs.add((x2+dx,y2+dy))
            unique_locs.add((x1-dx,y1-dy))

unique_locs = list(unique_locs)
x,y = zip(*unique_locs)
unique_locs = [(x,y) for (x,y) in unique_locs if data.inside(x,y)]

print(data.tostring(mark=(unique_locs,'#')))
print(f'Solution to part 1: {len(unique_locs)}')

######## PART 2 #######
data = load(8,2024,test=test).split().tomatrix()

symbols = load(8,2024,test=test)
symbols = list(set(''.join(symbols.tolist())))
symbols.pop(symbols.index('.'))

ant_locations = {sym: data.find(sym) for sym in list(symbols)}
diam = math.sqrt(data.width**2+data.height**2)
unique_locs = set()
processed = set()
for symbol, locs in ant_locations.items():
    for i, (x1,y1) in enumerate(locs):
        for jp, (x2,y2) in enumerate(locs[i+1:]):
            j=jp+i
            dx,dy = x2-x1, y2-y1
            n = math.gcd(dx,dy)
            dx = dx//n
            dy = dy//n
            N = int(math.ceil(diam/math.sqrt(dx**2+dy**2)))
            for n in range(N):
                unique_locs.add((x2+n*dx,y2+n*dy))
                unique_locs.add((x1-n*dx,y1-n*dy))

unique_locs = list(unique_locs)
x,y = zip(*unique_locs)
unique_locs = [(x,y) for (x,y) in unique_locs if data.inside(x,y)]

print(data.tostring(mark=(unique_locs,'#')))

print(f'Solution to part 2: {len(unique_locs)}')

    