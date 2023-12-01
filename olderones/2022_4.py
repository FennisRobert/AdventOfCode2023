from aoc import *

def overlaps(pairs: List) -> int:
    A = set(range(pairs[0][0],pairs[0][1]+1))
    B = set(range(pairs[1][0],pairs[1][1]+1))
    #print(A,B)
    if A.issubset(B) or B.issubset(A):
        return 1
    return 0

def intersects(pairs: List) -> int:
    A = set(range(pairs[0][0],pairs[0][1]+1))
    B = set(range(pairs[1][0],pairs[1][1]+1))
    #print(A,B)
    if len(A.intersection(B)):
        return 1
    return 0

print(load(4,2022).split(',').split('-').toint().apply(overlaps, False).sum())
print(load(4,2022).split(',').split('-').toint().apply(intersects, False).sum())
