from aoc import *
from collections import defaultdict

######## PART 1 #######
data = load(5,2024,test=False).symbgroup()

rules = data[0].split('|').toint()
below = defaultdict(list)
above = defaultdict(list)
for a,b in rules:
    below[b].append(a)
    above[a].append(b)

page_sets = data[1].split(',').toint()

class Page:
    def __init__(self, number):
        self.num = number
        
    def __lt__(self, other):
        if other.num in above[self.num]:
            return True
        elif other.num in below[self.num]:
            return False
        else:
            return KeyError(f'This pairing {self.num},{other.num} is not specified :(')
    
    def __repr__(self):
        return f'P[{self.num}]'
    
part_1_total = 0
part_2_total = 0
for i, pages in enumerate(page_sets):
    pgs = [Page(i) for i in pages]
    sorted_pgs = sorted(pgs)
    
    if not all(p1==p2 for p1,p2 in zip(pgs,sorted_pgs)):
        part_2_total += sorted_pgs[(len(sorted_pgs)-1)//2 ].num
    else:
        part_1_total += pgs[(len(pgs)-1)//2].num
        
print(f'Solution to part 1: {part_1_total}')

######## PART 2 #######

print(f'Solution to part 2: {part_2_total}')

    