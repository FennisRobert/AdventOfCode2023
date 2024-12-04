from aoc import *

######## PART 1 #######
data = load(14,2023,test=False).split().tolist()


sb = Sandbox(data, 'O', '#')

def diff(Ma,Mb):
    value = np.sum(np.abs(Ma.flatten()-Mb.flatten()))
    return value

original = 1*sb.matrix
new = 1*original
while True:
    new = up(1*original, 2, 1)
    if diff(original, new)==0:
        break
    original = new

iix = np.arange(new.shape[0])
iiy = np.arange(new.shape[1])
IX, IY = np.meshgrid(iix,iiy)

IY = new.shape[1]-IY
print(IY)
print(new==2)

print(np.sum(((new==2)*IY).flatten()))
######## PART 2 #######

data = load(14,2023,test=False).split().tolist()


sb = Sandbox(data, 'O', '#')

def diff(Ma,Mb):
    value = np.sum(np.abs(Ma.flatten()-Mb.flatten()))
    return value

def repeated(matrix, function):
    original = 1*matrix
    while True:
        new = function(1*original, 2, 1)
        if diff(original, new)==0:
            original = new
            break
        original = new
    return original

original = 1*sb.matrix
new = 1*original

series = [1*original for _ in range(100)]
iseries = 0

while True:
    original = repeated(original, up)
    original = repeated(original, left)
    original = repeated(original, down)
    original = repeated(original, right)
    
    diffs = [diff(original, s) for s in series]
    
    series = [original] + series[0:-1]
    print(diffs[:10])
    iseries += 1
    if 0 in diffs:
        break
    
print(iseries)
    

iix = np.arange(new.shape[0])
iiy = np.arange(new.shape[1])
IX, IY = np.meshgrid(iix,iiy)

IY = new.shape[1]-IY
print(IY)
print(new==2)

print(np.sum(((new==2)*IY).flatten()))
