from aoc import *



print(load(1,2023).findgroups('\d').applyto(lambda x: (x[0],x[-1])).combine().toint().sum())

pats = 'zero|one|two|three|four|five|six|seven|eight|nine'
mapper = {x: str(i) for i, x in enumerate(pats.split('|'))}
print(load(1,2023).findgroups(f'({pats}|\d)',overlap=True).replace(mapper).applyto(lambda x: (x[0],x[-1])).combine().toint().sum())