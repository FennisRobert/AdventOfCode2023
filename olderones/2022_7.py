from aoc import *
from collections import defaultdict
import re

space = 70000000
requnused = 30000000
used = 42476859
avail = space-used
tofree = requnused - avail
print(tofree)

dataset = dict()
instructions = load(7,2022,False).items

cwd = ('/',)

data = RecDict()
data['/'] = RecDict()
cwdict = dict()
for i, instruction in enumerate(instructions):
    #print('')
    #print(f'Instruction {i}: {instruction}')
    #print(f'CWD: {cwd}')
    if directory := reget(instruction, r'cd ([\.\/\w]+)'):
        if directory[0]=='..':
            cwd = cwd[:-1]
        elif directory[0]=='/':
            cwd = (cwd[0],)
        else:
            cwd = cwd + (directory[0],)
        continue
    if dirname := reget(instruction, r'dir (\w+)'):
        data[cwd + (dirname[0],)] = RecDict()
        #print(f'Data: {data}')
        continue
    if size := reget(instruction, r'(\d+) (\w+\.?\w*)'):
        data[cwd][size[1]] = int(size[0])
        #print(f'Data: {data}')
        continue
    
#print(data.asdict())
totvalue, sol1set = data.eval(sum)
print(sol1set)
counter = 0
options = []
for key, value in sol1set.items():
    if value <= 100000:
        counter += value
    if value >= tofree:
        options.append(value)

print(f'sol1: {counter}')
print(f'sol2: {min(options)}')