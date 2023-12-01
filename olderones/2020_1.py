from aoc import *

print([a*b*c for a,b,c in load(1,2020).toint().iterpermute(3) if a+b+c==2020])