from aoc import *

######## PART 1 #######
data = load(3,2024,test=False)
finder = Match('mul\((\d+),(\d+)\)')

solution = data.apply(lambda x: List(finder(x))).apply(lambda x: int(x[0])*int(x[1])).sum().sum()

print(f'Solution to part 1: {solution} = 174561379')

######## PART 2 #######

data = load(3,2024,test=False)

mulpat = Match('(mul\((\d+),(\d+)\))')
dopat = Match('(do\(\))')
dontpat = Match('(don\'t\(\))')
allpat = mulpat + dopat + dontpat

total = 0
active = True

for line in data:
    out = List(allpat(line))
    for results in out:
        if results[-1]=="don't()":
            active = False
        elif results[-2]=="do()":
            active = True 
        elif active:
            a = int(results[1])
            b = int(results[2])
            total += a*b
print(f'Solution to part 2: {total} = 106921067')

    