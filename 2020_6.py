from aoc import *

print(load(6,2020).symbgroup().combine().split().unique().applytoself(lambda x: x.len).sum())

print(sum(load(6,2020).symbgroup().applytoself(lambda x: x.split()).applytolast(lambda x: x.common()).applytoself(lambda x: x.len).unpack()))