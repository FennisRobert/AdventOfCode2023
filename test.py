from aoc import *


M = Matrix(load(3,2023,True).split().tolist())

print(M.around(1,1))
print(M.W[2:4,2:4])
#print(M.dt[1])