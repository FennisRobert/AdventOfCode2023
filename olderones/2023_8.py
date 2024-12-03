from aoc import *
import numpy as np
from math import gcd, lcm
data = load(8,2023).symbgroup()

instr = data[0].split().map({'L':0, 'R':1}).unpack().tolist()

maps = data[1]

maps = {a: (b,c) for a,b,c in maps.findgroups('(\w{3}) = \((\w{3}), (\w{3})\)').unpack()}

if False:
    loc = 'AAA'
    steps = 0
    N = len(instr)
    while loc != 'ZZZ':
        choice = instr[steps % N]
        loc = maps[loc][choice]
        print(steps, loc)
        steps += 1
    print(loc, steps)


def finished(lst):
    return all([l=='QQQ' for l in lst])

maps['QQQ'] = ('QQQ','QQQ')


## PART 2 Req Info

sls = ['VBA', 'TVA', 'DVA', 'VPA', 'AAA', 'DTA']

loop = {
    'VBA': [(0, 'VBA'), (4, 'LSB', 4), (4, 'LSB', 16047)],
    'TVA': [(0, 'TVA'), (2, 'SCX', 2), (2, 'SCX', 20779)],
    'DVA': [(0, 'DVA'), (6, 'XKG', 6), (6, 'XKG', 13945)],
    'VPA': [(0, 'VPA'), (2, 'SMP', 2), (2, 'SMP', 18675)],
    'AAA': [(0, 'AAA'), (4, 'JQL', 4), (4, 'JQL', 11313)],
    'DTA': [(0, 'DTA'), (2, 'GQF', 2), (2, 'GQF', 17623)]
}
zlocs = {'VBA': [(0, 'DVZ', 16043)], 'TVA': [(0, 'XKZ', 20777)], 'DVA': [(0, 'HSZ', 13939)], 'VPA': [(0, 'GGZ', 18673)], 'AAA': [(0, 'ZZZ', 11309)], 'DTA': [(0, 'HLZ', 17621)]}


for s in sls:
    print(f'start = {s}, start loop = {loop[s][1][2]}, period = {loop[s][2][2]-loop[s][1][2]}, Z at {zlocs[s][0][2]}')
    
Starts = np.array([loop[s][1][2] for s in sls]).astype(np.ulonglong)
Periods = np.array([loop[s][2][2]-loop[s][1][2] for s in sls]).astype(np.ulonglong)
DZs = np.array([zlocs[s][0][2]-loop[s][1][2] for s in sls]).astype(np.ulonglong)

 
print(Starts)
Ns = np.zeros(Periods.shape, dtype=np.ulonglong)
for j in range(6):
    Ns[j] = product([p for i,p in enumerate(Periods) if j != i])

print('LCM',lcm(*Periods))
print('LCM Test:', lcm(5,6))
print(Ns, gcd(*(Ns)))
Ns = 13740108158591//Periods - 1

np.set_printoptions(formatter={'int': '{:d}'.format})
Nsteps = Starts.astype(np.ulonglong)+(Ns)*((Periods.astype(np.ulonglong)))+DZs.astype(np.ulonglong)
#steps = (Ns-1)*(Periods.astype(np.ulonglong))

print(13740108158591,Nsteps)

nn = 0
S = Starts[0] + DZs[0]
P = Periods[0]

print((13740108158591-Starts-DZs) % Periods)
# while True:
#     steps = S + np.ulonglong(nn)*P
#     if all([x==0 for x in ((steps-Starts-DZs) % Periods)]):
#         print(steps)
#         break
#     nn += 1
#     print(steps)
###

locations = [key for key in maps.keys() if key[-1]=='A']
steps = 1
N = len(instr)
newlocs = [l for l in locations]
visited = {l: [] for l in locations}
visitedsteps = {l: [] for l in locations}
remove = []
loops = {l: [(0,l)] for l in locations}
if True:
    while not finished(newlocs):
        inr = (steps) % N
        newlocs = [maps[l][instr[inr-1]] for l in newlocs]
        for i,l in enumerate(newlocs):
            if l=='QQQ':
                continue
            lb = locations[i]
            visitedsteps[lb].append((inr,l,steps))
            if (inr,l) in visited[lb]:
                for (I,L,stepnr) in (visitedsteps[lb]):
                    if (I,L)==(inr,l):
                        loops[lb].append((inr,l,stepnr))
                remove.append(i)
            visited[lb].append((inr,l))
        for i in remove:
            newlocs[i]='QQQ'
        steps += 1
        if steps % 5000 == 0:
            print(locations, steps)
    print(visitedsteps['VBA'][:20])
    print(loops)
    zvisits = {l: [v for v in visits if v[1][-1]=='Z'] for l, visits in visitedsteps.items()}
    print(zvisits)