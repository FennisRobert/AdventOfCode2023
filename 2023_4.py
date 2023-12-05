from aoc import *
from math import floor
import numpy as np


#print(load(4,2023,False).split('|').findgroups('\d+').toint().apply(lambda x: floor(2**(len(set(x[1]).intersection(set(x[0][1:])))-1)),False))
data = load(4,2023,False).split('|').findgroups('\d+').toint().apply(lambda x: floor(2**(len(set(x[1]).intersection(set(x[0][1:])))-1)),False).sum()
print(data)

data = load(4,2023,False).split('|').findgroups('\d+').toint().apply(lambda x: len(set(x[1]).intersection(set(x[0][1:]))),False)

cc = {i+1: 1 for i in range(data.len)}

for i in range(1,data.len+1):
    N = data[i-1]
    for j in range(i+1,i+N+1):
        if j in cc:
            cc[j] += 1*cc[i]
print(sum(cc.values()))


data = load(4,2023,True).split('|').findgroups('\d+').toint().apply(lambda x: len(set(x[1]).intersection(set(x[0][1:]))),False)
  
N = data.len
M = np.zeros((N,N))
for i, n in enumerate(data):
    print(i,n)
    M[i+1:min(N,i+1+n),i] = 1
    M[i,i] = 1

print(M**20 @ np.ones((N,1)))
print(M @ M @ M @ M @ M)