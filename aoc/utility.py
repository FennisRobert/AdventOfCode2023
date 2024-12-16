from __future__ import annotations
import re
from rich import print
import numpy as np
from functools import reduce
from typing import Callable

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


class _SliceGetter:
    
    def __getitem__(self, slc):
        return slc
    
slicegetter = _SliceGetter()

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
    
    @property
    def dims(self) -> tuple[int,int]:
        return self.width, self.height
    
    def copy(self) -> Matrix:
        return Matrix([[x for x in row] for row in self.dt])
        
    def pad(self, n: int, filler) -> Matrix:
        emptyrow = [filler for _ in range(self.width+2*n)]
        padding = [filler for _ in range(n)]
        rows = [emptyrow]*n + [padding+ row +padding for row in self.dt ]  + [emptyrow]*n
        return Matrix(rows)
    
    def rot_cw(self) -> Matrix:
        return Matrix([[self.dt[y][x] for y in range(self.height-1,-1,-1)]for x in range(self.width)])
    
    def rot_cw_45(self, filler=None) -> Matrix:
        newW = int(np.ceil(np.sqrt(self.width**2/2+ self.height**2/2)))
        matrix = Matrix([[None for _ in range(newW)] for _ in range(newW)])
        for i in range(newW):
            for j in range(newW):
                pass
                
        
        return Matrix([[self.dt[y][x] for y in range(self.height-1,-1,-1)]for x in range(self.width)])
    
    def sample(self, xlist, ylist) -> list:
        return [self.dt[y][x] for x,y in zip(xlist, ylist)]
    
    def rot_ccw(self) -> Matrix:
        return Matrix([[self.dt[y][x] for y in range(self.height)]for x in range(self.width-1,-1,-1)])
    
    def above(self, row, col):
        return self(col, row-1)
    
    def below(self, row, col):
        return self(col, row+1)
    
    def right(self, row, col):
        return self(col+1, row)
    
    def left(self, row, col):
        return self(col-1, row)
    
    def around(self, row, col):
        Cs = self.H[col-1:col+2,row-1:row+2].flatten()
        Rs = self.W[col-1:col+2,row-1:row+2].flatten()
        return [self[r,c] for r,c in zip(Rs,Cs) if (r,c) is not (row,col)]
        return [x for x in [self(row+r,col+c) for r,c in zip([0, -1, -1, -1, 0, 1, 1, 1],[-1, -1, 0, 1, 1, 1, 0, -1])] if x is not None]
    
    def find(self, content) -> list[tuple[int,int]]:
        return [(i,j) for i in range(self.width) for j in range(self.height) if self.dt[j][i]==content]
    
    def __getitem__(self, slc):
        if isinstance(slc, tuple):
            return Matrix([_row[slc[1]] for _row in self.dt[slc[0]]])
        return self.dt[slc]
    
    def ifinside(self, coord):
        x,y = coord
        if (0 <= x <= self.width-1) and (0 <= y <= self.height-1):
            return coord
        return None
    
    def inside(self, x,y):
        return (0 <= x <= self.width-1) and (0 <= y <= self.height-1)
    
    def flipx(self) -> Matrix:
        return Matrix([_row[::-1] for _row in self.dt])
    
    def flipy(self) -> Matrix:
        return Matrix(self.dt[::-1])
    
    def splitx(self, index) -> tuple[Matrix, Matrix]:
        return self[:, :index+1], self[:, index+1:]
    
    def splity(self, index) -> tuple[Matrix, Matrix]:
        return self[:index+1, :], self[index+1:, :]
    
    def count(self, identifier) -> int:
        return sum([sum([1 for x in row if x == identifier]) for row in self.dt])
    
    def tostring(self, xmax: int = 15, ymax: int = 15, separator: str = '', mark=None, nospace=False) -> str:
        if nospace is False:
            sep = separator + ' '
        else:
            sep = separator
            
        if mark is None:
            domark = []
            marker = ''
        else:
            domark, marker = mark
            
        def get_display_indices(total, max_display):
            if total <= max_display:
                return list(range(total)), False
            else:
                num_display = max_display - 1  # Leave space for '...'
                first_part = num_display // 2
                second_part = num_display - first_part
                indices = list(range(first_part)) + [-1] + list(range(total - second_part, total))
                return indices, True

        cols_to_display, cols_truncated = get_display_indices(self.width, xmax)
        rows_to_display, rows_truncated = get_display_indices(self.height, ymax)

        data_to_display = []
        for row_idx in rows_to_display:
            if row_idx == -1:
                data_to_display.append(None)  # Indicates '...'
            else:
                row_data = []
                for col_idx in cols_to_display:
                    if col_idx == -1:
                        row_data.append(None)  # Indicates '...'
                    else:
                        if (col_idx,row_idx) in domark:
                            row_data.append(marker)
                        else:
                            row_data.append(str(self[row_idx][col_idx]))
                data_to_display.append(row_data[:])

        # Compute column widths for alignment
        column_widths = [0] * len(cols_to_display)
        for col_idx in range(len(cols_to_display)):
            max_width = 0
            for row in data_to_display:
                if row is None:
                    continue
                cell = row[col_idx]
                if cell is None:
                    cell_str = '...'
                else:
                    cell_str = cell
                max_width = max(max_width, len(cell_str))
            column_widths[col_idx] = max_width

        # Compute data width and line width
        data_width = sum(column_widths) + (len(column_widths) - 1) * len(sep)
        line_width = data_width + 2  # For the '│' at start and end

        # Build top and bottom lines with box drawing characters
        top_line = '┍' + ' ' * (line_width - 2) + '┐'
        bottom_line = '┕' + ' ' * (line_width - 2) + '┙'

        lines = [top_line]

        for row in data_to_display:
            if row is None:
                # Row representing '...'
                ellipsis = '...'
                padding = line_width - 2 - len(ellipsis)
                left_padding = padding // 2
                right_padding = padding - left_padding
                row_line = '│' + ' ' * left_padding + ellipsis + ' ' * right_padding + '│'
            else:
                row_items = []
                for idx, cell in enumerate(row):
                    if cell is None:
                        cell_str = '...'
                    else:
                        cell_str = cell
                    cell_str_padded = cell_str.rjust(column_widths[idx])
                    row_items.append(cell_str_padded)
                row_content = sep.join(row_items)
                row_line = '│' + row_content + '│'
            lines.append(row_line)

        lines.append(bottom_line)
        return '\n'.join(lines)
    
    def replace(self, dictionary: dict) -> Matrix:
        return Matrix([[dictionary.get(x,x) for x in row] for row in self.dt])
            
    def merge(self, other: Matrix) -> Matrix:
        return Matrix([[(elemA, elemB) for elemA, elemB in zip(rowA, rowB)] for rowA, rowB in zip(self.dt, other.dt)])

    def apply(self, function: Callable) -> Matrix:
        return Matrix([[function(x) for x in row] for row in self.dt])

    def all(self, truth_checker: Callable = lambda x: x==True) -> bool:
        return all([all(row) for row in self.dt])
    
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
    
    def __init__(self, regexpat: str):
        
        self.pat = regexpat.replace("{INT}","(\d+)").replace('{FLOAT}','([+-]?\d+\.\d+)').replace('{STRING}','(\w+)')
        self.items = None
        
    def __call__(self, arg):
        if re.findall(self.pat,arg):
            return re.findall(self.pat, arg)
        return False
    
    def __add__(self, other) -> Match:
        return Match(self.pat + '|' + other.pat)
