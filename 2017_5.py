from aoc import *
import numba as nb
import time

start = time.time()

######## PART 1 #######
data = load(5,2017,test=False).toint()

arry = np.array(data.tolist()).astype(np.int32)

@nb.njit(nb.i8(nb.i4[:]), cache=True, fastmath=True)
def execprogram(arry):
    N = arry.shape[0]
    pos = 0
    newpos = 0
    i = 0
    while True:
        newpos = pos + arry[pos]
        arry[pos] += 1
        pos = newpos
        i += 1
        if (newpos >= N) or (newpos < 0):
            break
    return i


print(f'Solution to part 1: {execprogram(arry)}')

print(f'Execution time = {(time.time()-start)*1000:.0f}ms')
######## PART 2 #######
data = load(5,2017,test=False).toint()

arry = np.array(data.tolist()).astype(np.int32)

@nb.njit(nb.i8(nb.i4[:]),cache=True, fastmath=True)
def execprogram(arry):
    N = arry.shape[0]
    pos = 0
    newpos = 0
    i = 0
    while True:
        newpos = pos + arry[pos]
        if arry[pos] >= 3:
            arry[pos] -= 1
        else:
            arry[pos] += 1
        pos = newpos
        i += 1
        if (newpos >= N) or (newpos < 0):
            break
    return i



print(f'Solution to part 2: {execprogram(arry)}')
print(f'Execution time = {(time.time()-start)*1000:.0f}ms')
