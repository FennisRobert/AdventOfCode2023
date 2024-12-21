from aoc import *
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from functools import cache
######## PART 1 #######
data = load(21,2024,test=False)

mhdist = lambda a,b: abs(b[1]-a[1]) + abs(b[0]-a[0])
kpd = {
    '7': (0,3),
    '8': (1,3),
    '9': (2,3),
    '4': (0,2),
    '5': (1,2),
    '6': (2,2),
    '1': (0,1),
    '2': (1,1),
    '3': (2,1),
    None: (0,0),
    '0': (1,0),
    'A': (2,0), 
}
arrowkp = {
    (0,1): (1,1),
    'A': (2,1),
    (-1,0): (0,0),
    None: (0,1),
    (0,-1): (1,0),
    (1,0): (2,0),
}

npstart = kpd['A']
arrstart = arrowkp['A']


@cache
def gen_instr_series(loc1: tuple[int,int], loc2: tuple[int, int]):
    dx = loc2[0]-loc1[0]
    dy = loc2[1]-loc1[1]
    
    x1, y1 = loc1
    x2, y2 = loc2
    if dx == 0:
        dxp = []
    else:
        dxp = abs(dx)*[arrowkp[(int(np.sign(dx)),0)],]
    if dy == 0:
        dyp = []
    else:
        dyp = abs(dy)*[arrowkp[(0,int(np.sign(dy)))],]
    series = []
    
    if y1==0 and x2==0:
        return dyp + dxp + [arrowkp['A'],]
    if x1==0 and y2==0:
        return dxp + dyp + [arrowkp['A'],]
    
    if dx < 0:
        return dxp + dyp + [arrowkp['A'],]
    if dx > 0 and dy < 0:
        return dyp + dxp + [arrowkp['A'],]
    return dyp + dxp + [arrowkp['A'],]

@cache
def gen_instr_series2(loc1: tuple[int,int], loc2: tuple[int, int]):
    dx = loc2[0]-loc1[0]
    dy = loc2[1]-loc1[1]
    x1, y1 = loc1
    x2, y2 = loc2
    
    if dx == 0:
        dxp = []
    else:
        dxp = abs(dx)*[arrowkp[(int(np.sign(dx)),0)],]
    
    if dy == 0:
        dyp = []
    else:
        dyp = abs(dy)*[arrowkp[(0,int(np.sign(dy)))],]
    
    if x1==0 and y2==1:
        return dxp + dyp + [arrowkp['A'],]
    if x2==0 and y1==1:
        return dyp + dxp + [arrowkp['A'],]
    
    if dx < 0:
        return dxp + dyp + [arrowkp['A'],]
    if dx > 0 and dy < 0:
        return dyp + dxp + [arrowkp['A'],]
    return dyp + dxp + [arrowkp['A'],]
    


def gen_arrow_series(password: str, Nrobot=2):
    locs = [npstart,] + [kpd[c] for c in password]
    series = [arrowkp['A'],]
    for l1, l2 in zip(locs[:-1], locs[1:]):
        series.extend(gen_instr_series(l1, l2))
    
    series_counter = defaultdict(int)
    for l1, l2 in zip(series[:-1], series[1:]):
        series_counter[(l1,l2)] += 1
    
    for nn in range(Nrobot):
        new_counter = defaultdict(int)
        for (l1, l2), Noccur in series_counter.items():
            newseries = [arrowkp['A'],] + gen_instr_series2(l1,l2)
            for L1, L2 in zip(newseries[:-1],newseries[1:]):
                new_counter[(L1,L2)] += Noccur
        series_counter = new_counter
    
    Ntotal = sum([n for n in series_counter.values()])
    #print(f'Ntotal = {N}, NA = {Acounter} sum = {N + Acounter}')
    return Ntotal

def compute(Nrobots):
    score = 0
    for passcode in data:
        N = gen_arrow_series(passcode, Nrobots)
        # print(N)
        num = int(passcode.replace('A',''))
        score = score + N*num
    return score

print(f'Solution to part 1: {compute(2)}')
print(f'Solution to part 2: {compute(25)}')

sols = {
    1: 25392,
    2: 53772,
    3: 126384,
    4: 310188,
    5: 757754,
    6: 1881090,
    7: 4656624,
    8: 11592556,
    9: 28805408,
    10: 71674912,
    11: 178268300,
    12: 443466162,
    13: 1103192296,
    14: 2744236806,

}
for n in range(1,26):
    print(f'{n} = {compute(n)} diff = {sols[n+1]-compute(n)}')
# 214358 is too high
# 206798 is to

######## PART 2 #######
# 208477261143644 is too low
# 208477261143644 
# 168131499374324
# 102823720810854
# 
# 515143013425166 is too high


# A B C D E F G H I
# start - A: 1
# A-B: 1
# B-C: 1
# C-D: 1