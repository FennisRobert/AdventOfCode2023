from aoc import *

######## PART 1 #######
data = load(9,2024,test=True)[0]

data_blocks, empty_blocks = [int(x) for x in data[::2]],[int(x) for x in data[1::2]]

empty_blocks.append(0)
Ntot = sum([int(c) for c in data])

mem_fill_data = []
i_range_filled = []
i_range_empty = []

mem_index = 0
for i, (n_free, n_empty) in enumerate(list(zip(data_blocks,empty_blocks))):
    mem_fill_data += [(i,ii) for ii in list(range(mem_index, mem_index+n_free))]
    i_range_filled += [ii for ii in list(range(mem_index, mem_index+n_free))]
    i_range_empty += list(range(mem_index+n_free, mem_index+n_free+n_empty))
    mem_index += n_free+n_empty


# Generate the memory
memory = [0 for _ in range(Ntot)]
for index, i in mem_fill_data:
    memory[i]=index

# Optimize the memory

while True:
    if i_range_filled[-1] < i_range_empty[0]:
        break
    index = i_range_filled.pop()
    c = memory.pop(index)
    index_empty = i_range_empty.pop(0)
    memory[index_empty] = c
 

print(f'Solution to part 1: {sum([i*n for i,n in enumerate(memory)])}, right answer = 1928')

######## PART 2 #######
data = load(9,2024,test=False)[0]

data_blocks, empty_blocks = [int(x) for x in data[::2]],[int(x) for x in data[1::2]]

empty_blocks.append(0)
Ntot = sum([int(c) for c in data])

mem_fill_data = []
i_range_filled = []
i_range_empty = []

mem_index = 0
for i, (n_free, n_empty) in enumerate(list(zip(data_blocks,empty_blocks))):
    mem_fill_data += [(i,ii) for ii in list(range(mem_index,mem_index+n_free))]
    i_range_filled.append((mem_index,mem_index+n_free))
    i_range_empty.append((mem_index+n_free,mem_index+n_free+n_empty))
    mem_index += n_free+n_empty

memory = [0 for x in range(Ntot)]
for index, i in mem_fill_data:
    memory[i]=index

memory = np.array(memory)
# For easier overwriting of data

for ipointer in range(len(i_range_filled)-1,-1,-1):
    i_start,i_end = i_range_filled[ipointer]
    data_blocks = i_end-i_start
    index_available = -1
    for i, (i_avail_start,i_avail_end) in enumerate(i_range_empty):
        if i_avail_end-i_avail_start >= data_blocks and (i_avail_start < i_start):
            index_available = i
            break
    if index_available >= 0:
        i_avail_start, i_avail_end = i_range_empty[index_available]
        memory[i_avail_start:(i_avail_start+data_blocks)] = memory[i_start:(i_start+data_blocks)]
        if i_avail_start+data_blocks != i_avail_end:
            i_range_empty[index_available] = (i_avail_start+data_blocks,i_avail_end)
        else:
            i_range_empty.pop(index_available)
        memory[i_start:i_end] = 0 

print(f'Solution to part 2: {sum([i*n for i,n in enumerate(memory)])}. Right answer = 6448168620520')

    