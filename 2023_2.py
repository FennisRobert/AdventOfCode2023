from aoc import *


R = Match('(\d+) red', lambda x: int(x) <= 12)
G = Match('(\d+) green', lambda x: int(x) <= 13)
B = Match('(\d+) blue', lambda x: int(x) <= 14)

print(load(2,2023).apply(lambda x: int(re.findall('Game (\d+)',x)[0]) * all([m(x) for m in (R,G,B)])).sum())
#print(load(2,2023).testitems((R,G,B)))
#for line in load(2,2023):
#    print(line)
#    print(((R(line),G(line),B(line))))
#    break

print(load(2,2023).apply(lambda x: product([max([int(x) for x in re.findall((f'(\d+) {col}'), x)]) for col in ['red','green','blue']])).sum())