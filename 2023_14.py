from aoc import *

######## PART 1 #######
data = load(14,2023,test=True).togameboard()
rock = data.add_type('O')
block = data.add_type('#')
data.compile()
i = 0
while True:
    print('Iteration')
    diff = data.move_up([rock,], [], [block,])
    if diff == 0:
        break
total = 0
for item in data.items:
    if item.type is not rock:
        continue
    total += data.iy - item.iy
    

print(data, i)

print(f'Solution to part 1: {total}')

######## PART 2 #######

data = load(14,2023,test=False).togameboard()
rock = data.add_type('O')
block = data.add_type('#')
data.compile()
icycle = 0

states = [1*data.nboard for _ in range(100)]
difference = None
while True:
    while True:
        diff = data.move_up([rock,], [], [block,])
        if diff == 0:
            break
    while True:
        diff = data.move_left([rock,], [], [block,])
        if diff == 0:
            break
    while True:
        diff = data.move_down([rock,], [], [block,])
        if diff == 0:
            break
    while True:
        diff = data.move_right([rock,], [], [block,])
        if diff == 0:
            break
    data.update()
    difference = [sum(abs(istate.flatten()-data.nboard.flatten())) for istate in states]
    print(list(difference)[:20])
    icycle += 1
    if any([d==0 for d in difference]):
        break
    states = [1*data.nboard,] + states[:-1]

Ncycle = difference.index(0)

Nfurther = (1000000000 - icycle) % (Ncycle + 1)

for N in range(Nfurther):
    while True:
        diff = data.move_up([rock,], [], [block,])
        if diff == 0:
            break
    while True:
        diff = data.move_left([rock,], [], [block,])
        if diff == 0:
            break
    while True:
        diff = data.move_down([rock,], [], [block,])
        if diff == 0:
            break
    while True:
        diff = data.move_right([rock,], [], [block,])
        if diff == 0:
            break

total = 0
for item in data.items:
    if item.type is not rock:
        continue
    total += data.iy - item.iy
    
print(total)