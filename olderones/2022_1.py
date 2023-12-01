from aoc import *
from rich import print
print(load(1,2022).symbgroup().toint().sum())
print(load(1,2022).symbgroup().toint().sum().max())
print(load(1,2022).symbgroup().toint().sum().sort(True)[:3].sum())