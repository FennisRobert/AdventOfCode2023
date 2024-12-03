from aoc import *

data = load(13,2023,False).symbgroup().split()
ca, cb = 0, 0
for sublist in data:
    matrix = sublist.tomatrix()
    #print(matrix.tostring())
    xmirrorid = 0
    ymirrorid = 0

    for ic in range(matrix.width-1):
        ML, MR = matrix.splitx(ic)

        mirroredx = ML.flipx().merge(MR)
        if mirroredx.apply(lambda x: x[0]==x[1]).all():
            xmirrorid = ic+1
            break

    for ic in range(matrix.height-1):
        ML, MR = matrix.splity(ic)
        
        mirroredx = ML.flipy().merge(MR)
        if mirroredx.apply(lambda x: x[0]==x[1]).all():
            ymirrorid = ic+1
            break
    
    ca += xmirrorid
    cb += ymirrorid
print(ca, cb, 100*cb + ca)


data = load(13,2023,False).symbgroup().split()
ca, cb = 0, 0
for sublist in data:
    matrix = sublist.tomatrix()
    
    xmirrorid = 0
    ymirrorid = 0

    for ic in range(matrix.width-1):
        ML, MR = matrix.splitx(ic)

        mirroredx = ML.flipx().merge(MR)
        #print(mirroredx.apply(lambda x: x[0]==x[1]).tostring(), mirroredx.apply(lambda x: x[0]==x[1]).count(False))
        
        if mirroredx.apply(lambda x: x[0]==x[1]).count(False)==1:
            xmirrorid = ic+1
            break

    for ic in range(matrix.height-1):
        ML, MR = matrix.splity(ic)
        
        mirroredx = ML.flipy().merge(MR)
        #print(mirroredx.tostring())
        if mirroredx.apply(lambda x: x[0]==x[1]).count(False)==1:
            ymirrorid = ic+1
            break
    
    ca += xmirrorid
    cb += ymirrorid
    print(xmirrorid, ymirrorid)
print(ca, cb, 100*cb + ca)
