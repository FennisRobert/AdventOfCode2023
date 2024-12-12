from aoc import *
import numpy as np
import tqdm
import numba as nb
######## PART 1 #######
data = load(12,2024,test=False).split().tomatrix().pad(1,'#')

W = data.width
H = data.height

fields = dict()
included = set()

# Collect the fields from a starting point
def collect(x,y):
    symb = data[y][x]
    field = set()
    cue = [(x,y)]
    while cue:
        neighbors = []
        for x0,y0 in cue:
            for (X,Y) in [(x0-1,y0),(x0+1,y0),(x0,y0-1),(x0,y0+1)]:
                if ((X,Y) not in field) and (data[Y][X] == symb) and ((X,Y) not in cue) and ((X,Y) not in neighbors):
                    neighbors.append((X,Y))
        field = field.union(set(cue))
        cue = neighbors
    return (symb,x,y), field


# Find all the unique fields
for x,y in [(x,y) for x in range(1,W-1) for y in range(1,H-1)]:
    if (x,y) in included or data[y][x]=='#':
        continue
    key, value = collect(x,y)
    fields[key] = value
    included = included.union(value)

areamap = np.zeros((W,H)).astype(np.int32)

total_part_1 = 0
total_part_2 = 0


#This functions counts the unique series of circumpherances. 
# A single row will contain something like 0 0 0 1 1 1 1 0 -1 -1 -1 0
# This function will count all the series of 1's and -1's as blocks and returns those
# A +1 is a left or up moving area and -1 a right or down moving.
@nb.njit(cache=True)
def measure_circumference_p2(Mx, My):
    totsides = 0
    for i in range(Mx.shape[0]):
        sides = 0
        cur_number = 0
        for j in range(Mx.shape[1]):
            numy = My[j,i]
            if numy != cur_number:
                sides += np.abs(numy)*2 # Number of unique H-sides == unique V-sides.
                cur_number = numy
        totsides += sides   
    return totsides

for key, areas in tqdm.tqdm(fields.items()):
    area = len(areas)
    Mx = 0*areamap
    My = 0*areamap
    for x,y in areas:
        Mx[x+1,y] -= 1
        Mx[x,y] += 1
        My[x,y+1] += 1
        My[x,y] -= 1
    
    total_part_2 += measure_circumference_p2(Mx,My)*area
    circumference = np.sum(np.abs(Mx).flatten())+np.sum(np.abs(My).flatten())
    total_part_1 += area*circumference
    

print(f'Solution to part 1: {total_part_1}')
print(f'Solution to part 2: {total_part_2}')
