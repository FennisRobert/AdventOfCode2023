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

class SliceLim:
    
    def __init__(self, shape):
        self.shape = shape
        
    def __getitem__(self, slc):
        if isinstance(slc, tuple):
            if isinstance(slc[0],(int,np.int64)):
                return tuple([min(max(s,0),mx) for s,mx in zip(slc, self.shape)])    
            return tuple([slice(min(max(s.start,0),mx), min(max(s.stop,0),mx)) for s,mx in zip(slc, self.shape)])
        if isinstance(slc, slice):
            return slice(min(max(slc.start,0),self.shape[0]), min(max(slc.stop,0),self.shape[0]),slc.step)
        return min(max(slc,0),self.shape[0])

class Matrix:
    
    def __init__(self, items: list[list]):
        self.dt = items
        self.width = len(self.dt[0])
        self.height = len(self.dt)
        w = np.arange(self.width)
        h = np.arange(self.height)
        self.W,self.H = np.meshgrid(w,h)
        self._SL = SliceLim((self.width, self.height))
        
    def __str__(self) -> str:
        return f'{self.dt}'
    
    def mod(self, col, row):
        return self.dt[col % self.width][row & self.height]
    
    def __call__(self, col, row):
        if (0 > col) or (col >= self.width) or (0 > row) or (row >= self.height):
            return None
        return self[row][col]
    
   
    def above(self, row, col):
        return self(col, row-1)
    
    def below(self, row, col):
        return self(col, row+1)
    
    def right(self, row, col):
        return self(col+1, row)
    
    def left(self, row, col):
        return self(col-1, row)
    
    def around(self, row, col):
        print(self._SL[-4:4,-5:200])
        Cs = self.H[col-1:col+2,row-1:row+2].flatten()
        Rs = self.W[col-1:col+2,row-1:row+2].flatten()
        print(Cs.flatten(),Rs.flatten())
        return [self[r,c] for r,c in zip(Rs,Cs) if (r,c) is not (row,col)]
        return [x for x in [self(row+r,col+c) for r,c in zip([0, -1, -1, -1, 0, 1, 1, 1],[-1, -1, 0, 1, 1, 1, 0, -1])] if x is not None]
        
    def __getitem__(self, slc):
        if isinstance(slc, tuple):
            return self.dt[slc[0]][slc[1]]
        return self.dt[slc]
    
    
        
        

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