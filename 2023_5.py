from aoc import *

test = False

maps = []

class RangeDict: 
    def __init__(self):
        self.Ranges = []
        self.iRanges = []
        
    def __str__(self):
        return f'RangeDict{tuple(self.Ranges)}'
    
    def __repr__(self):
        return f'RangeDict{tuple(self.Ranges)}'
    
    
    def add_range(self, to, frm, rng):
        self.Ranges.append((frm, frm+rng-1, to-frm))
        self.iRanges.append((to, to+rng-1, frm-to))
        
    def rmap(self, inptrange):
        for r in self.iRanges:
            if r[1] >= inptrange >= r[0]:
                return inptrange + r[2]
        return inptrange
        
    def map(self, inptrange):
        for r in self.Ranges:
            if r[1] >= inptrange >= r[0]:
                return inptrange + r[2]
        return inptrange
    
for listgroup in load(5,2023,test).symbgroup()[1:]:
    line1 = listgroup[0]
    newdict = RangeDict()
    for line in listgroup[1:].split(' ').toint():
        newdict.add_range(*line.items)
    maps.append(newdict)

seeds = load(5,2023,test).symbgroup()[0].split(' ')[0][1:].toint()
original_seeds = [s for s in seeds]
newints = []
for mp in maps:
    for seed in seeds:
        newints.append(mp.map(seed))
    seeds = newints
    newints = []
  
print(f'Part 1: = {min(seeds)}')

ranges = list(zip(original_seeds[0::2],original_seeds[1::2]))

def inrange(value):
    return any([s <= value <= s+d-1 for s,d in ranges])

i = 0
io = 1
while True:
    i += 1
    io = i
    for mp in maps[::-1]:
        io = mp.rmap(io)
    #print(f'{i} maps to {io}')
    if inrange(io):
        print(f'Part 2: Seed found! location {i} for seed {io}')
        break

    