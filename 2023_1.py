from aoc import *



print(load(1,2023).findgroups('\d').applyto(lambda x: (x[0],x[-1])).combine().toint().sum())

pats = r'(zero|one|two|three|four|five|six|seven|eight|nine)'
mapper = {x: str(i) for i, x in enumerate(pats[1:-1].split('|'))}
print(load(1,2023).findgroups(r'(zero|one|two|three|four|five|six|seven|eight|nine|\d)',overlap=True).replace(mapper).applyto(lambda x: (x[0],x[-1])).combine().toint().sum())