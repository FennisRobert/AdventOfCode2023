from aoc import *
print(load(2,2020).find(r'(\d+)-(\d+) (\w): (\w+)'))
print(sum([1 for mn, mx, lttr, pswrd in load(2,2020).find(r'(\d+)-(\d+) (\w): (\w+)') if (int(mn) <= pswrd.count(lttr) <= int(mx))]))

print(sum([1 for mn, mx, lttr, pswrd in load(2,2020).find(r'(\d+)-(\d+) (\w): (\w+)') if ((pswrd[int(mn)-1]==lttr) ^ (pswrd[int(mx)-1]==lttr))]))