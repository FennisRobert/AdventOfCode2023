from aoc import *
from collections import defaultdict

######## PART 1 #######
data = load(10,2024,test=False).split().toint().tomatrix().pad(1,-1)

W = data.width
H = data.height

trailheads = defaultdict(list)

def find_paths(current_height: int, current_path: list, paths: dict):
    x,y = current_path[-1]
    if current_height == 9:
        paths[(x,y)].append(current_path)
        return paths
    for xn,yn in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        if data[yn][xn] == current_height + 1:
            paths = find_paths(current_height+1, current_path + [(xn,yn),], paths)
    return paths

for x,y in data.find(0):
    trailheads[(x,y)] = find_paths(0, [(x,y)], defaultdict(list))

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

    