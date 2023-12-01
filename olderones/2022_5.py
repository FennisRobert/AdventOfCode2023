from aoc import *

text = load(5,2022)

part1 = text[0:8]
part2 = text[10:]
stacks = part1.split(recursive=False).transpose()[1::4].remove(' ').tolist()

for N, frm, to in part2.find('\d+').toint():
    stacks[to-1] = stacks[frm-1][0:N][::-1]+ stacks[to-1]
    stacks[frm-1] = stacks[frm-1][N:]

print(''.join([x[0] for x in stacks]))

stacks = part1.split(recursive=False).transpose()[1::4].remove(' ').tolist()

for N, frm, to in part2.find('\d+').toint():
    stacks[to-1] = stacks[frm-1][0:N]+ stacks[to-1]
    stacks[frm-1] = stacks[frm-1][N:]

print(''.join([x[0] for x in stacks]))
    