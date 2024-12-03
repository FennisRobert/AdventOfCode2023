import numpy as np
from typing import Callable

class PieceType:
    def __init__(self, identifier, index: int):
        self.identifier = identifier
        self.index: int = index
        self.symbol = identifier
        
OOB = PieceType('', index=-99)
EMPTY = PieceType(' ', index=-100)

class Item:
    
    def __init__(self, ix: int, iy: int, type: PieceType, id: int):
        self.ix = ix
        self.iy = iy
        self.type = type
        self.i = type.index
        self.id = id
    
    @property
    def symb(self) -> str:
        return self.type.symbol
    
    
    def __repr__(self):
        return self.type.symbol

OOBBlock = Item(None, None, type=OOB, id=-99)
EMPTYBlock = Item(None, None, type=EMPTY, id=-100)

class GameBoard:
    
    def __init__(self, data: list[list]):
        self.data: list[list] = data
        self.shape = (len(self.data[0]), len(self.data))
        self.iy = len(self.data)
        self.ix = len(self.data[0])
        self.cboard = np.full(self.shape, ' ', dtype='<U1')
        self.nboard = np.zeros(self.shape, dtype=np.int32)
        self.iboard = np.zeros(self.shape, dtype=np.int32)-1
        self.ixboard = np.pad(self.iboard, pad_width=1, mode='constant', constant_values=-2)
        self.types: dict[str, PieceType] = dict()
        self.items: list[Item] = []
        
    def add_type(self, symbol: str) -> None:
        ptype = PieceType(symbol, len(self.types)+1)
        self.types[symbol] = ptype
        return ptype
    
    def all_ij(self) -> list[tuple[int, int]]:
        return [(i,j) for i in range(self.shape[0]) for j in range(self.shape[1])]
    
    def compile(self):
        i = 0
        for ix, iy in self.all_ij():
            symb = self.data[iy][ix]
            if symb not in self.types:
                continue
            self.items.append(Item(ix,iy,self.types[symb], i))
            i += 1
        self.update()
        
    def update(self) -> None:
        self.nboard = 0*self.nboard
        self.iboard = 0*self.iboard - 1
        for item in self.items:
            self.nboard[item.iy, item.ix] = item.i
            self.iboard[item.iy, item.ix] = item.id   
        self.ixboard = np.pad(self.iboard, pad_width=1, mode='constant', constant_values=-2)  
    
    def fupdate(self) -> None:
        self.ixboard = np.pad(self.iboard, pad_width=1, mode='constant', constant_values=-2) 
    
    def get(self, ix, iy) -> Item:
        i = self.ixboard[iy+1, ix+1]
        if i==-2:
            return OOBBlock
        elif i==-1:
            return EMPTYBlock
        else:
            return self.items[i]
        
    def move_up(self, types: list[PieceType], free: list[PieceType], blockers: list[PieceType]) -> None:
        free = free + [EMPTY,]
        blockers = blockers + [OOBBlock,]
        i_original = self.iboard*1
        for item in sorted(self.items, key=lambda it: it.iy):
            
            if item.type not in types:
                continue
            ix, iy = item.ix, item.iy
            if self.get(ix, iy-1).type in free:
                item.iy -= 1
                self.iboard[iy-1,ix] = item.id
                self.iboard[iy,ix] = -1
        self.fupdate()
        return int(sum(np.abs(i_original.flatten()-self.iboard.flatten())))

    def move_down(self, types: list[PieceType], free: list[PieceType], blockers: list[PieceType]) -> None:
        free = free + [EMPTY,]
        blockers = blockers + [OOBBlock,]
        i_original = self.iboard*1
        for item in sorted(self.items, key=lambda it: it.iy, reverse=True):
            if item.type not in types:
                continue
            ix, iy = item.ix, item.iy
            if self.get(ix, iy+1).type in free:
                item.iy += 1
                self.iboard[iy+1,ix] = item.id
                self.iboard[iy,ix] = -1
        self.fupdate()
        return int(sum(np.abs(i_original.flatten()-self.iboard.flatten())))
    
    def move_left(self, types: list[PieceType], free: list[PieceType], blockers: list[PieceType]) -> None:
        free = free + [EMPTY,]
        blockers = blockers + [OOBBlock,]
        i_original = self.iboard*1
        for item in sorted(self.items, key=lambda it: it.ix):
            if item.type not in types:
                continue
            ix, iy = item.ix, item.iy
            if self.get(ix-1, iy).type in free:
                item.ix -= 1
                self.iboard[iy,ix-1] = item.id
                self.iboard[iy,ix] = -1
        self.fupdate()
        return int(sum(np.abs(i_original.flatten()-self.iboard.flatten())))

    def move_right(self, types: list[PieceType], free: list[PieceType], blockers: list[PieceType]) -> None:
        free = free + [EMPTY,]
        blockers = blockers + [OOBBlock,]
        i_original = self.iboard*1
        for item in sorted(self.items, key=lambda it: it.ix, reverse=True):
            if item.type not in types:
                continue
            ix, iy = item.ix, item.iy
            if self.get(ix+1, iy).type in free:
                item.ix += 1
                self.iboard[iy,ix+1] = item.id
                self.iboard[iy,ix] = -1
        self.fupdate()
        return int(sum(np.abs(i_original.flatten()-self.iboard.flatten())))
        
        
                    
    def print(self) -> None:
        board = self.cboard.copy()
        for item in self.items:
            board[item.iy, item.ix] = item.symb
        print(board)