from aoc import *

######## PART 1 #######
data = load(9,2024,test=False)[0]

data_size, empty_blocks = [int(x) for x in data[::2]],[int(x) for x in data[1::2]]

empty_blocks.append(0)
Ntot = sum([int(c) for c in data])

# Manage a list of memory slots that are filled and free. 
indices_filled = []
indices_empty = []

# For Part 2
i_range_filled = []
i_range_empty = []

mem_index = 0

# Prefill the required data
original_memory = np.zeros((Ntot,),dtype=np.int32)

for file_index, (n_free, n_empty) in enumerate(list(zip(data_size,empty_blocks))):
    original_memory[mem_index:mem_index+n_free] = file_index
    indices_filled += list(range(mem_index, mem_index+n_free))
    indices_empty += list(range(mem_index+n_free, mem_index+n_free+n_empty))
    
    i_range_filled.append((mem_index,mem_index+n_free))
    i_range_empty.append((mem_index+n_free,mem_index+n_free+n_empty))
    
    mem_index += n_free+n_empty
    
    

# Optimize the memory

memory_efficient = 1*original_memory

## Efficient method

nEmpty = len(indices_empty)
nFilled = len(indices_filled)
iempty = np.array(indices_empty)
ifilled = np.array(indices_filled)
merge_limit = np.argwhere(iempty >= ifilled[nFilled-nEmpty:][::-1])[0][0]
memory_efficient[iempty[:merge_limit]] = memory_efficient[ifilled[nFilled-merge_limit:][::-1]]
memory_efficient[ifilled[nFilled-merge_limit:][::-1]] = 0


## Original step by step method
memory = original_memory
while True:
    if indices_filled[-1] < indices_empty[0]:
        break
    index = indices_filled.pop()
    c = memory[index]
    memory[index] = 0
    index_empty = indices_empty.pop(0)
    memory[index_empty] = c
    
##

print(f'Solution to part 1: {sum([i*n for i,n in enumerate(memory)])}, right answer = 6421128769094')
print(f'Solution to part 1: {sum([i*n for i,n in enumerate(memory_efficient)])}, right answer = 6421128769094')

######## PART 2 #######

memory = 1*original_memory

# Start the memory optimization loop starting with the last range

for ipointer in range(len(i_range_filled)-1,-1,-1):
    
    # Get the start and end of the last file
    i_start, i_end = i_range_filled[ipointer]
    data_size = i_end - i_start
    
    index_available = -1
    
    #find an empty slot of sufficient size that sits before the block to move!
    for file_index, (i_avail_start,i_avail_end) in enumerate(i_range_empty):
        if i_avail_end-i_avail_start >= data_size and (i_avail_start < i_start):
            index_available = file_index
            break
    
    #If such an index exists
    if index_available != -1:
        # Shift the parts in the memory
        i_avail_start, i_avail_end = i_range_empty[index_available]
        memory[i_avail_start:(i_avail_start+data_size)] = memory[i_start:(i_start+data_size)]
        
        # If the emtpy slot is not used up completely
        if i_avail_start+data_size != i_avail_end:
            # Replace the indices of the empty slot with the new shorter section
            i_range_empty[index_available] = (i_avail_start+data_size, i_avail_end)
        else:
            # Else, remove it completely from the set of available slots
            i_range_empty.pop(index_available)
        # Overwrite the old memory with zeros
        memory[i_start:i_end] = 0 

print(f'Solution to part 2: {sum([i*n for i,n in enumerate(memory)])}. Right answer = 6448168620520')

    