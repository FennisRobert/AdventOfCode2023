from aoc import *
from itertools import product
from tqdm import tqdm
######## PART 1 #######
data = load(7,2024,test=True).findgroups('\d+')

operators = {'0':'+',
             '1':'*'}
operators = ('+','*',)
def gen_eq(eq, numbers):
    N = len(numbers)
    op_list = list(product(operators,repeat=N-1))
    #print(op_list)
    for ops in op_list:
        right = '('*(N) + ''.join([a+')'+b for a,b in zip(numbers,list(ops)+['',])])
        truth = eval(f'{eq}=={right}')
        #print(f'{eq}=={right} evals to {truth}')
        if truth:
            return True
    return False
        
tot = 0
for numbers in tqdm(data):
    ans, nums = numbers[0], numbers[1:].tolist()
    if gen_eq(ans,nums):
        tot += int(ans)
        
print(f'Solution to part 1: {tot}')

######## PART 2 #######
data = load(7,2024,test=False).findgroups('\d+')

operators = {'0':'+',
             '1':'*'}
operators = ('add(','mul(','comb(')
add = lambda a,b: a+b
mul = lambda a,b: a*b
comb = lambda a,b: int(str(b)+str(a))

# This takes forever :(
def gen_eq(eq, numbers):
    N = len(numbers)
    op_list = list(product(operators,repeat=N-1))
    #print(op_list)
    for ops in op_list:
        right = ''.join([a+b+',' for a,b in zip(list(ops)+['',],numbers[::-1])])[:-1]+')'*(N-1)
        #print(right)
        truth = eval(f'{eq}=={right}')
        #print(f'{eq}=={right} evals to {truth}')
        if truth:
            return True
    return False
        
tot = 0
for numbers in tqdm(data):
    ans, nums = numbers[0], numbers[1:].tolist()
    if gen_eq(ans,nums):
        tot += int(ans)
        

print(f'Solution to part 2: {tot}')

    