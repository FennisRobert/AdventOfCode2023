from aoc import *
from math import *

data = load(6,2023).findgroups('\d+').toint()
T = data[0]
D = data[1]

nways = []
for t,d in zip(T,D):
    D = d+0.001
    t1 = ceil((t-sqrt(t**2-4*D))/2)
    t2 = floor((t+sqrt(t**2-4*D))/2)
    nways.append(t2-t1+1)
    
print(f'Part 1 = {product(nways)} ways')

data = load(6,2023,False).findgroups('\d+').combine().toint()
T = data[0]
D = data[1]

t1 = ceil((T-sqrt(T**2-4*D))/2)
t2 = floor((T+sqrt(T**2-4*D))/2)

print(f'Part 2 = {t2-t1+1} ways')