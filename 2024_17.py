from aoc import *

######## PART 1 #######


class Computer:
    
    def __init__(self, A,B,C):
        self.A = A
        self.B = B
        self.C = C
        self.IP = 0
        self.output: list = []
        self.dojump = True
        self.op: dict = {
            0: lambda: 0,
            1: lambda: 1,
            2: lambda: 2,
            3: lambda: 3,
            4: self.getA,
            5: self.getB,
            6: self.getC,
            7: None,
        }
        self.instr: dict = {
            0: lambda op: self.setA(self.getA()//(2**self.op[op]())),
            1: lambda op: self.setB(self.getB() ^ op),
            2: lambda op: self.setB((self.op[op]() % 8)  & 0b111 ),
            3: lambda op: self.jzn(op),
            4: lambda op: self.setB(self.getB() ^ self.getC()),
            5: lambda op: self.output.append(self.op[op]() % 8),
            6: lambda op: self.setB(self.getA()//(2**self.op[op]())),
            7: lambda op: self.setC(self.getA()//(2**self.op[op]())),
        }
    
      
    def jzn(self, op: int) -> None:
        if self.getA()==0:
            return
        else:
            if self.IP != op:
                self.IP = op
                self.dojump = False
                
    def setA(self, val) -> None:
        self.A = val
    
    def setB(self, val) -> None:
        self.B = val
        
    def setC(self, val) -> None:
        self.C = val
        
    def getA(self) -> int:
        return self.A
    
    def getB(self) -> int:
        return self.B
    
    def getC(self) -> int:
        return self.C
    
    def run_program(self, program: tuple[int]) -> str:
        N = len(program)
        while True:
            #print(self.A,self.B,self.C,self.IP)
            if self.IP > N-1:
                break
            n1 = program[self.IP]
            n2 = program[self.IP+1]
            self.instr[n1](n2)
            if self.dojump:
                self.IP += 2
            else:
                self.dojump = True
        return self.output


reg, prog = load(17,2024,test=False).symbgroup()

A,B,C = reg
A = int(A.split(':')[1].strip())
B = int(B.split(':')[1].strip())
C = int(C.split(':')[1].strip())

prog = eval('(' + prog[0].split(':')[1].strip() + ')')


# Program Test
comp = Computer(0,29,0)

comp = Computer(A,B,C)
output = comp.run_program(prog)

print(f'Solution to part 1: {",".join([str(x) for x in output])}')

######## PART 2 #######

program = prog

solution = 8**15

pointer = -1

solved = False

while True:
    
    icounter = 0
    
    if pointer < -15:
        step = 1
    else: 
        step = 8**(15+pointer) + 1
    
    value = solution
    while True:
        output = tuple(Computer(value,0,0).run_program(program))
        
        if output==program:
            solved = True
            break
        
        if (program[pointer:] == output[pointer:]):
            break
        value += step
        icounter += 1
    solution = solution + step*icounter
    
    if solved:
        break
    
    pointer -= 1

print(f'Solution to part 2: {solution}')