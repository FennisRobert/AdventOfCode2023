import re
from rich import print
import numpy as np
from functools import reduce

def splitlen(lst: list, NSplit: int = 2) -> list:
    sN = len(lst)//NSplit
    return [lst[sN*i:sN*(i+1)] for i in range(NSplit)]

def sort(_list: list, descend=False):
    if not descend:
        return tuple(zip(*sorted([(x, i) for i, x in enumerate(_list)], key=lambda x: x[0])))
    return tuple(zip(*sorted([(x, i) for i, x in enumerate(_list)], key=lambda x: x[0], reverse=True)))

def groupiter(toiter, N: int):
    for i in range(len(toiter)-N):
        yield toiter[i:i+N]
        
def reget(input_string, pattern):
    # Find the first occurrence of the pattern in the input string
    match = re.search(pattern, input_string)
    
    if match:
        return match.groups()  # Return the matched substring (match group)
    else:
        return None  # Return None if no match is found


def lrange(start,end):
    return list(range(start,end+1))

def product(lst):
    return reduce(lambda a,b: a*b,lst)


class Matrix:
    
    def __init__(self, items: list[list]):
        self.M = np.array(items)
        

class RecDict:
    
    def __init__(self, defaultval = None):
        self._dict = dict()
        self._defaultval = defaultval
    
    
    def asdict(self) -> dict:
        dct = dict()
        for key, value in self._dict.items():
            if isinstance(value, RecDict):
                dct[key] = value.asdict()
                continue
            dct[key] = value
        return dct
    
    def __repr__(self) -> str:
        return f'RecDict{self._dict}'
    
    def __getitem__(self, key: tuple):
       # print('get', self, key)
        if not isinstance(key,tuple):
            return self._dict[key]
        if len(key)==1:
            return self._dict[key[0]]
        return self._dict[key[0]][key[1:]]
    
    def __setitem__(self, key: tuple, value) -> None:
        #print('set', self, key, value)
        if not isinstance(key, tuple):
            self._dict[key] = value
            return
        if len(key)==1:
            #print(f'Key is: {key}')
            self._dict[key[0]] = value
            return
        self._dict[key[0]][key[1:]] = value
        return None
    
    def eval(self, function: callable, collector: dict = None, basekey=''): 
        if collector is None:
            collector = dict()
        locallist = []
        for key, value in self._dict.items():
            if isinstance(value, RecDict):
                value, collector = value.eval(function, collector, f'{basekey}/{key}')
                locallist.append(value)
                collector[f'{basekey}/{key}'] = value
            else:
                locallist.append(value)
        return function(locallist), collector
    
class Match:
    
    def __init__(self, regexpat: str, verification: callable):
        
        self.pat = regexpat.replace("{INT}","(\d+)").replace('{FLOAT}','([+-]?\d+\.\d+)').replace('{STRING}','(\w+)')
        self.verification = verification
        self.items = None
        
    def __call__(self, arg):
        if re.findall(self.pat,arg):
            #print(re.findall(self.pat, arg))
            #print([self.verification(x) for x in re.findall(self.pat, arg)])
            return all([self.verification(x) for x in re.findall(self.pat, arg)])
        return False