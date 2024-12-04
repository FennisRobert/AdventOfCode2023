import numba as nb
import numpy as np
from collections import defaultdict

@nb.njit(nb.i1[:,:](nb.i1[:,:],nb.i8, nb.i8), parallel=True, cache=True)
def up(matrix, free, fixed):
    
    nx, ny = matrix.shape
    
    for iy in range(1,ny):
        for ix in nb.prange(nx):
            if matrix[iy,ix] == free:
                if matrix[iy-1,ix] == 0:
                    matrix[iy-1,ix] = free
                    matrix[iy,ix] = 0
    
    return matrix

@nb.njit(nb.i1[:,:](nb.i1[:,:],nb.i8, nb.i8), parallel=True, cache=True)
def down(matrix, free, fixed):
    
    nx, ny = matrix.shape
    
    for iy in range(ny-2,-1,-1):
        for ix in nb.prange(nx):
            if matrix[iy,ix] == free:
                if matrix[iy+1,ix] == 0:
                    matrix[iy+1,ix] = free
                    matrix[iy,ix] = 0
    
    return matrix

@nb.njit(nb.i1[:,:](nb.i1[:,:],nb.i8, nb.i8), parallel=True, cache=True)
def left(matrix, free, fixed):
    
    nx, ny = matrix.shape
    
    for ix in range(1,nx):
        for iy in nb.prange(ny):
            if matrix[iy,ix] == free:
                if matrix[iy,ix-1] == 0:
                    matrix[iy,ix-1] = free
                    matrix[iy,ix] = 0
    
    return matrix

@nb.njit(nb.i1[:,:](nb.i1[:,:],nb.i8, nb.i8), parallel=True, cache=True)
def right(matrix, free, fixed):
    
    nx, ny = matrix.shape
    
    for ix in range(nx-2,-1,-1):
        for iy in nb.prange(ny):
            if matrix[iy,ix] == free:
                if matrix[iy,ix+1] == 0:
                    matrix[iy,ix+1] = free
                    matrix[iy,ix] = 0
    
    return matrix
                
    
    
class Sandbox:
    
    def __init__(self, data: list[list[str]], free: str, fixed: str):
        self.data = data
        self.free = free
        self.fixed = fixed
        self.matrix = None
        
        self.compile()
        
    def compile(self):
        w = len(self.data[0])
        h = len(self.data)
        
        translate = defaultdict(int)
        translate[self.fixed] = 1
        translate[self.free] = 2
        self.matrix = np.zeros((w,h), dtype=np.int8)
        
        for iy, row in enumerate(self.data):
            for ix, char in enumerate(row):
                self.matrix[iy,ix] = translate[char]
        
        
                
        