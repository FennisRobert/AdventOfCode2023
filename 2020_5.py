from aoc import *

mapping = {
    'F': '0',
    'B': '1',
    'L': '0',
    'R': '1',
}
print(load(5,2020).replace(mapping).apply(lambda x:int(x[:-3],2)*8+int(x[-3:],2)).max())

print(List.range(9,977).diff(load(5,2020).replace(mapping).apply(lambda x:int(x[:-3],2)*8+int(x[-3:],2))))