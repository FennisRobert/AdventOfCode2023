from __future__ import annotations
from pathlib import Path
from functools import reduce
from .utility import sort, splitlen, Matrix, Match
import numpy as np
import re
from itertools import product
from typing import Callable
from rich import print
from .game import GameBoard

class List:
    def __init__(self, lines: list[str | int | float], sortids = None):
        if isinstance(lines, (set, list, tuple)):
            lines = list(lines)
        else:
            lines = [lines,]
        self.items = lines
        self.sortids = sortids
    
    @property
    def level(self) -> List:
        levels = [self.items,[]]
        while True:
            for item in levels[-2]:
                if isinstance(item, List):
                    levels[-1].append(item)
            if levels[-1] == []:
                break
            levels[-1] = reduce(lambda a,b: a+b, levels[-1])
            levels.append([])
        return [List(level) for level in levels[:-1]]
            
    @property
    def len(self) -> int:
        return len(self.items)
    
    @property
    def lines(self) -> str:
        return '\n'.join([str(x) for x in self.items])
    
    @property
    def has_lists(self) -> bool:
        if self.len==0:
            return False
        return isinstance(self.items[0], List)
    
    @property
    def dtype(self):
        return type(self.items[0])
    
    def __len__(self) -> int:
        return len(self.items)
    
    def __str__(self) -> str:
        return f'List{self.items}'
    
    def __repr__(self) -> str:
        return f'List{self.items}'
    
    def __getitem__(self, slice) -> List:
        if isinstance(slice,int):
            return self.items[slice]
        if self.sortids:
            return List(self.items[slice], self.sortids[slice])
        return List(self.items[slice])
    
    def all(self) -> bool:
        return all(self.items)
    
    def apply(self, function, recursive=True):
        '''Applies the provided function to all elements in the lists of lists.'''
        if self.has_lists and recursive:
            return List([x.apply(function) for x in self.items])
        return List([function(x) for x in self.items])
    
    def apply_to_list(self, function, recursive=True):
        '''Applies the provided function to the list contained in the List objects instead of the items in the list'''
        if self.has_lists and recursive:
            return List([x.apply_to_list(function) for x in self.items])
        return List(function(self.items))
    
    def apply_to_deepest(self, function):
        '''Applies the function to the deepest List object that does not contain lists.'''
        if self.has_lists :
            return List([x.apply_to_deepest(function) for x in self.items])
        return function(self)
    
    def apply_to_deepest_items(self, function, recursive=True):
        if self.has_lists and recursive:
            return List([x.apply_to_deepest_items(function) for x in self.items])
        return function(self)
    
    def abstract_diff(self, merger: Callable, recursive=True) -> List:
        if self.has_lists and recursive:
            return List([x.abstract_diff(merger) for x in self.items])
        return List([merger(a,b) for a,b in zip(self.items[:-1], self.items[1:])])
    
    def reduce(self, rfunc: callable, recursive=True):
        if self.has_lists and recursive:
            return List([x.reduce(rfunc) for x in self.items])
        return reduce(rfunc, self.items)
    
    def rectify(self, toadd) -> List:
        maxL = max([len(x) for x in self.items])
        return List([x + (maxL-len(x))*toadd for x in self.items])
    
    def transpose(self) -> List:
        lists = self.tolist()
        transposed_lists = list(map(list, zip(*lists)))
        return List([List(x) for x in transposed_lists])
    
    def remove(self, item, recursive=True) -> List:
        return self.apply_to_list(lambda _list: [x for x in _list if x is not item])
    
    def find(self, pattern, selection=None) -> List:
        if selection is not None:
            return self.apply(lambda x: List(re.findall(pattern, x)[0])[selection])
        return self.apply(lambda x: List(re.findall(pattern, x)[0]))
    
    def findgroups(self, pattern, overlap=False) -> List:
        if overlap:
            pattern = f'(?={pattern})'
        return self.apply(lambda x: List(re.findall(pattern, x)))
    
    def findlist(self, listpat) -> List:
        return self.apply(lambda x: List(reduce(lambda a,b: a+b, [re.findall(pat, x) for pat in listpat])))
    
    def toint(self, recursive=True) -> List:
        return self.apply(lambda x: int(x), recursive=recursive)

    def sum(self, recursive=True) -> List:
        return self.reduce(lambda a,b: a+b, recursive=recursive)
    
    def max(self, recursive=True):
        return self.reduce(lambda a,b: max(a,b), recursive=recursive)

    def split(self, splitter=None, n_groups: int = None, n_items: int = None, recursive=True) -> List:
        if n_groups is not None:
            return self.apply(lambda x: List(splitlen(x,2)), recursive=recursive)
        elif n_items is not None:
            return self.apply(lambda x: List(splitlen(x, len(x)//n_items)),recursive=recursive)
        if splitter is None:
            return self.apply(lambda x: List([c for c in x]), recursive=recursive)
        return self.apply(lambda x: List(x.split(splitter)), recursive=recursive)
    
    def group(self, groupsize: int) -> List:
        return List([List(self.items[groupsize*i:groupsize*(i+1)]) for i in range(self.len//groupsize)])
    
    def map(self, mapping: dict, recursive=True) -> List:
        return self.apply(lambda x: mapping[x], recursive=recursive)
    
    def replace(self, mapping: dict, rescursive=True) -> List:
        def replaceall(string, dct):
            for key, value in dct.items():
                string = string.replace(key,value)
            return string
        return self.apply(lambda x: replaceall(x, mapping))
    
    def unpack(self):
        items = self.items
        if self.dtype == List:
            items = [x.unpack() for x in items]
        if len(items)==1:
            return self.items[0]
        return items
    
    def sort(self, descend=False) -> List:
        V, I = sort(self.items, descend)
        return List(V,I)
    
    def iter(self, recursive=True):
        if recursive:
            for item in self.items:
                if isinstance(self.dtype, List):
                    item.iter(recursive)
                else:
                    yield item
        else:
            for item in self.items:
                yield item
    
    def first(self, check: Callable) -> int:
        checklist = self.apply(check, False).items
        if True in checklist:
            return checklist.index(True)
        else:
            return None
    
    def without(self, indices: list[int]) -> List:
        return List([item for i,item in enumerate(self.items) if i not in indices])
    
    def tolist(self, recursive=True):
        if self.has_lists:
            return [x.tolist(recursive=recursive) for x in self.items]
        return self.items
        
    def toset(self, recursive=True):
        if self.has_lists and recursive:
            return List([x.toset() for x in self.items])
        return ListSet(self.items, self.sortids)
    

    def count(self, truthtest: callable) -> int:
        return sum([truthtest(x) for x in self.items])
    
    def tomatrix(self) -> Matrix:
        return Matrix(self.tolist())
    
    def togameboard(self) -> GameBoard:
        return GameBoard(self.tolist())
    def iterpermute(self, depth: int = 2):
        return list(product(*[self.items for x in range(depth)]))
    
    def combine(self, function = lambda x: x.sum(False), iterations=-1):
        if self.has_lists and iterations != 0:
            return List([x.combine(function, iterations-1) for x in self.items])
        return function(self)
    
    def merge(self, merger: Callable) -> List:
        base = self.items[0].tolist()
        for item in self.items[1:]:
            base = [merger(a,b) for a,b in zip(base, item)]
        return List(base)

    def __add__(self, other: List) -> List:
        if isinstance(other, List):
            return List(self.items+other.items)
            
    def contains(self, items: tuple, recursive=True):
        return self.apply_to_deepest_items(lambda x: all([(it in x.items) for it in items]), recursive=recursive)
    
    def test(self, function: callable):
        return any([function(x) for x in self.items])
    
    def mustmatch(self, matches: tuple[Match], recursive=True):
        return self.apply_to_deepest_items(lambda x: all([x.test(m) for m in matches]), recursive=recursive)
    
    def testitems(self, matches: tuple[Match], recursive=True):
        return self.apply(lambda x: all([m(x) for m in matches]), recursive=True)
    
    def __and__(self, other: List):
        #print(set(self.items), set(other.items), set(self.items).intersection(set(other.items)))
        return List(list(set(self.items).intersection(set(other.items)))) 
    
    def diff(self, other: List) -> List:
        return List([x for x in self.items if x not in other.items])
    
    @staticmethod
    def range(*args):
        return List(list(range(*args)))
    
    def unique(self, recursive=True):
        return self.apply_to_list(lambda x: list(set(x)), recursive=recursive)
    
    def common(self):
        return List(reduce(lambda a,b: a.__and__(b), self.items))
    
class ListSet(List):
     def __init__(self, lines: list[str], sortids = None):
        self.items = set(lines)
        self.sortids = sortids
    
    
class AOCFile(List):
    
    def __init__(self, lines: List, sortids = None, previous = None):
        super().__init__(lines, sortids)
        self.prevoius = previous

    def __str__(self) -> str:
        return f'AOCFile{self.items}'
    
    def __repr__(self) -> str:
        return f'AOCFile{self.items}'
    
                
    def symbgroup(self, groupsymb='') -> AOCFile:
        groups = []
        collector = []
        for line in self.iter():
            if line==groupsymb:
                groups.append(List(collector))
                collector = []
                continue
            collector.append(line)
        groups.append(List(collector))
        return AOCFile(groups, self)
     
    
def load(day: int, year: int = 2024, test=False) -> AOCFile:
    if test: 
        toadd = 'test'
    else:
        toadd = ''
    filename = Path(f'{year}/day{day}{toadd}.txt')
    data = []
    with open(filename.absolute(), 'r') as file:
        data = file.read().split('\n')
    return AOCFile(data)
   
