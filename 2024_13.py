from aoc import *
from icecream import ic
######## PART 1 #######
data = load(13,2024,test=False).symbgroup().findgroups(r'\d+').toint()

cost_pt1 = 0
cost_pt2 = 0
for solset in data:
    A, B, S = solset
    xa, ya = A
    xb, yb = B
    x, y = S
    nb = (x - xa*(y/ya))/(xb - (yb*xa)/ya)
    na = (y - nb *yb)/ya
    # This tests if the decimals of the float solution for nA and nB yield an resultant error creater than 1 step
    if (abs((round(na)-na)*max(xa,ya)) < 1) and (abs((round(nb)-nb)*max(xb,yb)) < 1):
        cost_pt1 += 3*round(na)+round(nb)

    x += 10000000000000
    y += 10000000000000
    nb = (x - xa*(y/ya))/(xb - (yb*xa)/ya)
    na = (y - nb *yb)/ya
    if (abs((round(na)-na)*max(xa,ya)) < 1) and (abs((round(nb)-nb)*max(xb,yb)) < 1):
        cost_pt2 += 3*round(na)+round(nb)
    
print(f'Solution to part 1: {cost_pt1} == 29877')
print(f'Solution to part 2: {cost_pt2} == 99423413811305')
