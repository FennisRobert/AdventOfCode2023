from aoc import *

N = load(3,2020).len
D = load(3,2020)
print(sum([1 for row in range(N) if D[row][(3*row) % len(D[0])]=='#']))\
    
print(product([sum([1 for row in range(N//a) if D[row*a][(b*row) % len(D[0])]=='#']) for b,a in [(1,1), (3,1), (5,1),(7,1),(1,2)]]))