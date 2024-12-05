from aoc import *

######## PART 1 #######
data = load(15,2023,test=False).split(',').split()

nums = []
for line in data[0]:
    value = 0
    for c in line:
        value = ((value + ord(c))*17) % 256
    
    nums.append(value)


print(f'Solution to part 1: {sum(nums)}')

######## PART 2 #######
data = load(15,2023,test=True).split(',').split()
from collections import defaultdict
def hsh(chars: list[str]) -> int:
    VAL = 0
    for c in chars:
        VAL = ((VAL + ord(c))*17) % 256
    return VAL

class Box:
    
    def __init__(self):
        self.items = []
        self.inv = dict()
        
    def __repr__(self) -> str:
        return str(self.items)
    
    def totvalue(self, nr: int) -> int:
        val = 0
        for i, (lab, num) in enumerate(self.items):
            val += (i+1)*int(num)*nr
        return val
    
    def add(self, label, num):
        if label in self.inv:
            i = self.inv[label]
            self.items[i] = (label, num)
        else:
            self.items.append((label,num))
            self.inv = {l[0]: i for i,l in enumerate(self.items)}
    
    def remove(self, label):
        if label in self.inv:
            self.items.pop(self.inv[label])
        self.inv = {l[0]: i for i,l in enumerate(self.items)}
        
boxes = defaultdict(Box)

for instr in data[0]:
    instr = ''.join(instr)
    if '=' in instr:
        chars, num = instr.split('=')
        boxnr = hsh([c for c in chars])
        boxes[boxnr].add(chars,num)
        
    else:
        chars = instr.split('-')[0]
        boxnr = hsh([c for c in chars])
        boxes[boxnr].remove(chars)

val = 0
for key, box in boxes.items():
    val += box.totvalue(key+1)
    
    
print(f'Solution to part 2: {val}')

    