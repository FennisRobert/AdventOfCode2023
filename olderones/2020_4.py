from aoc import *
import re
#print(re.findall(r'(\w+):(\w+)', 'lifsejf:324234'))
print(load(4,2020).symbgroup('').split(' ').combine(1).find(r'(\w+):([\#\w]+)',0))

print(sum(load(4,2020).symbgroup('').split(' ').combine(1).find(r'(\w+):([\#\w]+)',0).contains(('byr','iyr','eyr','hgt','hcl','pid','ecl'))))

print(load(4,2020).symbgroup('').split(' ').combine(1))
m1 = Match(r'byr:(\d{4})$', lambda x: 1920 <= int(x) <= 2002)
m2 = Match(r'iyr:(\d{4})$', lambda x: 2010 <= int(x) <= 2020)
m3 = Match(r'eyr:(\d{4})$', lambda x: 2020 <= int(x) <= 2030)
m4 = Match(r'hgt:{INT}(in|cm)$', lambda x: ((150 <= int(x[0]) <=193 and x[1]=='cm') or (59 <= int(x[0]) <= 76 and x[1]=='in')))
m5 = Match(r'ecl:(amb|blu|brn|gry|grn|hzl|oth)$', lambda x: True)
m6 = Match(r'hcl:#([0-9a-f]{6})$', lambda x: True)
m7 = Match(r'pid:[0-9]{9}$', lambda x: True)
print(load(4,2020).symbgroup('').split(' ').combine(1).mustmatch((m1,m2,m3,m4,m5,m6,m7)).sum())
print(load(4,2020).symbgroup('').split(' ').combine(1).len)

print(m7('pid:0000000000'))