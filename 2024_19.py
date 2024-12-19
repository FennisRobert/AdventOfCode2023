from aoc import *
import re
import numpy as np
from typing import List, Dict
from collections import defaultdict
from tqdm import tqdm
######## PART 1 #######
towels, designs = load(19,2024,test=False).symbgroup()
towels = towels.split(', ').reduce(lambda a,b: a.extend(b), False)

towelpats = [re.compile(towel) for towel in towels]

towellengs = {i: len(towel) for i, towel in enumerate(towels)}


def check_design(design: str, patterns: list[re.Pattern]) -> list:
    options = defaultdict(list)
    for ipat, pat in enumerate(patterns):
        for match in pat.finditer(design):
            if match is None:
                continue
            options[match.start()].append(match.end()-match.start())
            
    #print(options)
    counter = np.zeros((len(design)*2,)).astype(np.int64)
    counter[0] = 1
    Nd = len(design)
    for i in range(Nd):
        for L in options[i]:
            counter[i+L] += counter[i]
    print(f'Design {design}, {counter[Nd]}')
    return counter[Nd]

all_possible = np.zeros((len(designs),)).astype(np.int64)
for i, design in enumerate(designs):
    all_possible[i] = check_design(design, towelpats)

Npossible = np.sum(all_possible)

print(f'Solution to part 1: {Npossible}')

# 415287142411864
# 503262593786615