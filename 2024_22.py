from aoc import *
import numpy as np
from collections import defaultdict
from tqdm import tqdm
######## PART 1 #######
data = load(22,2024,test=False).toint()

def mix(num, snum):
    return num % snum

def prune(num):
    return num % 16777216
def parse_number(num, Ntimes: int = 1):
    store = np.zeros((Ntimes+1,)).astype(np.int64)
    for i in range(Ntimes):
        store[i] = num
        n2 = (((num*64) ^ num) % 16777216)
        n3 = ((round(n2//32) ^ n2) % 16777216)
        n4 = (((n3*2048) ^ n3) % 16777216)
        num = n4
    store[-1] = num
    store = np.mod(store,10)
    dstore = store[1:]-store[:-1]
    valmap = defaultdict(int)
    for i in range(Ntimes-4):
        valmap[tuple(dstore[Ntimes-1-4-i:Ntimes-1-i])] = store[Ntimes-1-i]
    return num, valmap
    
    print(num, n2, n3, n4)
    
#parse_number(123,50)
dicts = []
for num in tqdm(data):
    num, mapper = parse_number(num, 2000)
    dicts.append(mapper)

allkeys = set()
for dct in dicts:
    allkeys.update(set(dct.keys()))

bestkey = (0,0,0,0)
bestval = 0
for key in tqdm(allkeys):
    value = sum([dct[key] for dct in dicts])
    if value > bestval:
        bestkey = key
        bestval = value
        print(bestkey, bestval)

print(f'Solution to part 1: {sum([parse_number(num,2000) for num in data])}')

######## PART 2 #######
data = load(22,2024,test=True)

print(data)

print(f'Solution to part 2: {None}')

    