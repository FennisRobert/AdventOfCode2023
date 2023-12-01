from aoc import *

line = load(6,2022)[0]
i=0
for chars in groupiter(line, 4):
    if len(set(chars))==len(chars):
        print(i + 4)
        break
    i+=1
    
i=0
for chars in groupiter(line, 14):
    if len(set(chars))==len(chars):
        print(i + 14)
        break
    i+=1
    