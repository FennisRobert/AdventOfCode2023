from aoc import *
import itertools
onsens = load(12,2023,True).split(' ').split(',')

def replace(string, new, indices):
    for i in indices:
        string = string[:i] + new + string[i+1:]
    return string

def validate(data: str, nums: tuple):
    onsgroups = [len(x) for x in data.split('.') if x]
    return tuple(onsgroups) == nums

def noptions(data: str, nums: list[int]):
    
    T = sum(nums)
    p = data.count('#')
    new = T-p
    if new < 0:
        return 0
    noptions = 0
    options = [i for i,c in enumerate(data) if c=='?']
    for comb in itertools.combinations(options, new):
        newstr = replace(data,'#',comb).replace('?','.')
        if validate(newstr, nums):
            noptions += 1
    return noptions
     
tsum = 0
for ons in onsens:
    data = ons[0][0]
    nums = tuple(ons[1].toint().items)
    
    tsum += noptions(data, nums)
print(f'Part 1 = {tsum}')

tsum = 0
for ons in onsens:
    data = ons[0][0]
    nums = tuple(ons[1].toint().items)

    loptions = {i: noptions(data + i, nums) for i in ['.','#']}
    coptions = {(i,j): noptions(i+data+j, nums) for i,j in itertools.product(['.','#'],['.','#'])}
    roptions = {i: noptions(i + data, nums) for i in ['.','#']}
    N = 0
    for c1, c2, c3, c4 in itertools.product(['.','#'],['.','#'],['.','#'],['.','#']):
        N += loptions[c1] * coptions[(c1,c2)] * coptions[(c2,c3)] * coptions[(c3,c4)] * roptions[c4]
    print(data, N)
    tsum += N
    
    
print(f'Part 2 = {tsum}')