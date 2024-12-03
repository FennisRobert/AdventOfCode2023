from aoc import *
from math import *
import numpy as np

data = load(6,2023).findgroups('\d+').toint()

T = np.array(data[0].items)
D = np.array(data[1].items)
print('Part 1 short = ',product(np.floor((T+np.sqrt(T**2-4*(D+0.001)))/2) - np.ceil((T-np.sqrt(T**2-4*(D+0.001)))/2)+1))


data = load(6,2023,False).findgroups('\d+').combine().toint()
T = data[0]
D = data[1]

t1 = ceil((T-sqrt(T**2-4*D))/2)
t2 = floor((T+sqrt(T**2-4*D))/2)

print(f'Part 2 = {t2-t1+1} ways')