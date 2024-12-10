from aoc import *
from collections import defaultdict

######## PART 1 #######
data = load(10,2024,test=False).split().toint().tomatrix()

W = data.width
H = data.height

trailheads = defaultdict(list)

def find_paths(current_height: int, current_pos: tuple, current_path: list, paths: dict):
    x,y = current_pos
    if current_height == 9:
        paths[(x,y)].append(current_path)
        return paths
    for xn,yn in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if not data.inside(xn,yn):
            continue
        if data[yn][xn] == current_height + 1:
            paths = find_paths(current_height+1, (xn,yn), current_path + [(xn,yn),], paths)
    return paths

for x,y in [(x,y) for x in range(W) for y in range(H)]:
    if data[y][x] != 0:
        continue
    paths = defaultdict(list)
    paths = find_paths(0, (x,y), [(x,y)], paths)
    trailheads[(x,y)] = paths
    

counter_part_1 = 0
counter_part_2 = 0
for start, paths in trailheads.items():
    for end, path in paths.items():
        counter_part_1 += 1
        for p in path:
            counter_part_2 += 1
        

print(f'Solution to part 1: {counter_part_1} = 682')

######## PART 2 #######


print(f'Solution to part 2: {counter_part_2} = 1511')

    