from aoc import *
from collections import defaultdict
import numpy as np
from tqdm import tqdm
######## PART 1 #######
data = load(23,2024,test=False).split('-').tolist()

conn = defaultdict(set)
for a,b in data:
    conn[a].add(b)
    conn[b].add(a)
    
threes = set()
for cA in tqdm(conn.keys()):
    for cB in conn[cA]:
        for cC in conn[cB]:
            if cA in conn[cC]:
                threes.add(tuple(sorted((cA,cB,cC))))

def numerate(ca,cb,cc):
    if ca[0]=='t' or cb[0]=='t' or cc[0]=='t':
        return 1
    return 0 

print(f'Solution to part 1: {sum([numerate(*trip) for trip in threes])}')

# ######## PART 2 #######
total_network = list(conn.keys())

clusters = set()
for cA,cB in data:
    basenet = {cA,cB}
    for cC in total_network:
        if basenet <= conn[cC]:
            basenet.add(cC)
    clusters.add(tuple(sorted(list(basenet))))

print(f'Solution to part 2: {",".join(max(list(clusters), key=lambda x: len(x)))}')

    