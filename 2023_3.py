from aoc import *
import re
from collections import defaultdict
#print(load(3,2023).lines)
data = load(3,2023,False)
N = len(data[0])

def adjacent(li, si, ei):
    ics = lrange(si-1,ei+1)
    lines = [li,] + [li-1,]*len(ics) + [li,] + [li+1,]*len(ics)
    chars = [si-1,] + ics + [ei+1] + ics[::-1]
    for L,C in zip(lines,chars):
        if L<0 or L >= data.len:
            continue
        if C<0 or C >= N:
            continue
        yield (L,C)
        
    
nums = []

geardict = defaultdict(list)
for il, line in enumerate(data):
    
    for match in re.finditer('(\d+)',line):
        s, e = match.start(), match.end()
        if not all(data[l][c] in '.01234567890' for l,c in adjacent(il, s, e-1)):
            for l,c in adjacent(il, s, e-1):
                if data[l][c]=='*':
                    geardict[(l,c)].append(int(match.group()))
            
            nums.append(int(match.group()))
print(nums)
print(sum(nums))
print(geardict)
sumval = 0
for key, value in geardict.items():
    if len(value) == 2:
        sumval += product(value)
print(sumval)