from aoc import *
from functools import cache
from collections import defaultdict
######## PART 1 #######
data = load(11,2024,test=False).split(' ').toint()[0].tolist()

@cache
def calc_new(num: int, amount: int) -> list[tuple]:
    nd = len(str(num))
    if num==0:
        return [(1,amount),]
    elif nd%2==0:
        nl = int(str(num)[:nd//2])
        nr = int(str(num)[nd//2:])
        return [(nl,amount),(nr,amount)]
    else:
        return [(num*2024,amount),]

def compute_blinks(N: int) -> int:
    stone_counter = {n: 1 for n in data}
    for _ in range(N):
        newcounter = defaultdict(int)
        for num, amount in stone_counter.items():
            for newnum, newamount in calc_new(num, amount):
                newcounter[newnum] += newamount
        stone_counter = newcounter
    return sum([v for v in stone_counter.values()])

print(f'Part 1 = {compute_blinks(25)}')
print(f'Part 2 = {compute_blinks(75)}')

