from aoc import *
from rich import print
import string

# Generate a string containing lowercase and uppercase letters
lowercase = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
uppercase = string.ascii_uppercase  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

combined_letters = lowercase + uppercase
vmap = {s: i+1 for i, s in enumerate(combined_letters)}
print(load(3,2022).split('',n_groups=2).apply(lambda x: set(x)).reduce(lambda a,b: list(a.intersection(b))[0]).map(vmap).sum())


print(load(3,2022).group(3).apply(lambda x: set(x)).reduce(lambda a,b: a.intersection(b)).apply(lambda x: list(x)[0]).map(vmap).sum())