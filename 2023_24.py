from aoc import *

import sympy as sp
from itertools import combinations
px1, py1, px2, py2, vx1, vy1, vx2, vy2, a, b = sp.symbols('px1 py1 px2 py2 vx1 vy1 vx2 vy2 a b')

eq1 = sp.Eq(px1 + a*vx1, px2 + b*vx2)
eq2 = sp.Eq(py1 + a*vy1, py2 + b*vy2)

sol = sp.solve([eq1, eq2], a,b)

print(f'a={sol[a]}')
print(f'b={sol[b]}')
print(f'x= {px1 + sol[a]*vx1}')
print(f'y= {py1 + sol[a]*vy1}')

######## PART 1 #######
data = load(24,2023,test=False).batchreplace([('@',''),(',','')]).split(' ').remove('').toint()
print(data)
stones = []

for line in data:
    px,py,pz,vx,vy,vz = line.tolist()
    stones.append(((px,py,pz,vx,vy,vz)))
    
N = len(stones)
counter = 0

for i,j in combinations(range(N),2):
    if i==j:
        continue
    
    px1, py1, pz1, vx1, vy1, vz1 = stones[i]
    px2, py2, pz2, vx2, vy2, vz2 = stones[j]
    if (vx1*vy2 - vx2*vy1) == 0:
        continue
    a=(-px1*vy2 + px2*vy2 + py1*vx2 - py2*vx2)/(vx1*vy2 - vx2*vy1)
    b=(-px1*vy1 + px2*vy1 + py1*vx1 - py2*vx1)/(vx1*vy2 - vx2*vy1)
    x= px1 + vx1*(-px1*vy2 + px2*vy2 + py1*vx2 - py2*vx2)/(vx1*vy2 - vx2*vy1)
    y= py1 + vy1*(-px1*vy2 + px2*vy2 + py1*vx2 - py2*vx2)/(vx1*vy2 - vx2*vy1)
    if 7 <= x <= 27 and 7 <= y <= 27 and a>0 and b>0:
        counter += 1
    if 200000000000000 <= x <= 400000000000000 and 200000000000000 <= y <= 400000000000000 and a>0 and b>0:
        counter += 1

print(f'Solution to part 1: {counter}')

######## PART 2 #######
from z3 import Int, solve, Real, Solver

Ncases = 4

variables = []
symbs = ('pix','piy','piz','vix','viy','viz')


solvefor = [Real(t.replace('i','0')) for t in symbs]
px, py, pz, vx, vy, vz = solvefor

s = Solver()

eqs = []
for i in range(1,Ncases+1):
    pvs = stones[i-1]#[Real(t.replace('i',str(i))) for t in symbs]
    pix, piy, piz, vix, viy, viz = pvs
    ti = Real(f't{i}')
    variables.append(pvs)
    s.add(pix + ti*vix == px + ti*vx)
    s.add(piy + ti*viy == py + ti*vy)
    s.add(piz + ti*viz == pz + ti*vz)

print(s.check())
print(s.model())
print(f'Solution to part 2: {s.model()[px].as_long() + s.model()[py].as_long() + s.model()[pz].as_long()}')

    