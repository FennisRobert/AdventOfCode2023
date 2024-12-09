from aoc import *

######## PART 1 #######
data = load(9,2024,test=True)[0]

size, empty = [int(x) for x in data[::2]],[int(x) for x in data[1::2]]

empty.append(0)
Ntot = sum([int(c) for c in data])

dbfiller = []
ifilled = []
irefilled = []
iempty = []

fcount = 0
for i, (f, e) in enumerate(list(zip(size,empty))):
    dbfiller += [(i,ii) for ii in list(range(fcount,fcount+f))]
    ifilled += [ii for ii in list(range(fcount,fcount+f))]
    iempty += list(range(fcount+f,fcount+f+e))
    fcount += f+e


database = [None for x in range(Ntot)]
for index, i in dbfiller:
    database[i]=index

while True:
    if ifilled[-1] < iempty[0]:
        break
    index = ifilled.pop()
    c = database.pop(index)
    index_empty = iempty.pop(0)
    
    database[index_empty] = c
    irefilled.append(index_empty)
    
database = [x for x in database if x is not None]
    

print(f'Solution to part 1: {sum([i*n for i,n in enumerate(database)])}')

######## PART 2 #######
data = load(9,2024,test=False)[0]

size, empty = [int(x) for x in data[::2]],[int(x) for x in data[1::2]]

empty.append(0)
Ntot = sum([int(c) for c in data])

dbfiller = []
ifilled = []
iempty = []

fcount = 0
for i, (f, e) in enumerate(list(zip(size,empty))):
    dbfiller += [(i,ii) for ii in list(range(fcount,fcount+f))]
    ifilled.append((fcount,fcount+f))
    iempty.append((fcount+f,fcount+f+e))
    fcount += f+e

database = [0 for x in range(Ntot)]
for index, i in dbfiller:
    database[i]=index

database = np.array(database)

for ipointer in range(len(ifilled)-1,-1,-1):
    start,fin = ifilled[ipointer]
    size = fin-start
    iavail = -1
    for i, (es,ef) in enumerate(iempty):
        if ef-es >= size and (es < start):
            iavail = i
            break
    if iavail>=0:
        es, ef = iempty[iavail]
        
        database[es:(es+size)] = database[start:(start+size)]
        if es+size != ef:
            iempty[iavail] = (es+size,ef)
        else:
            iempty.pop(iavail)
        database[start:fin] = 0 
print(database)
print(f'Solution to part 2: {sum([i*n for i,n in enumerate(database)])}')

    