from util import * 
from dataclasses import dataclass, field
from collections import defaultdict

def split_opcode(num):
    op = num % 100 
    return digits(num // 100, 3) + (op, )

@dataclass
class IntCode:
    data: list 
    inputs: list = field(default_factory=list)
    index: int = 0 
    relbase: int = 0

    @classmethod 
    def from_list(cls, memory):
        return cls(defaultdict(int, enumerate(memory)))

    def deepcopy(self):
        return IntCode(defaultdict(int, self.data), list(self.inputs), self.index, self.relbase)

    def run_to_output(self):
        data = self.data
        while self.index < len(data):
            #print(index, data[index])

            m3, m2, m1, op = split_opcode(data[self.index])
            modes = m1, m2, m3

            def get_pos(num):
                """
                Gets the position referred to by the num-th parameter. 
                """
                m = modes[num-1]
                if m == 1: 
                    return self.index + num # immediate mode
                
                x = data[self.index+num]
                # relative is 2, normal position mode is 0.
                if m == 2: 
                    return x + self.relbase # relative mode
                elif m == 0: 
                    return x # position mode
                assert False

            def get_param(num): 
                """
                Gets the num-th operation parameter, starting from 1, 
                and applying the modes.
                """
                # immediate mode is 1, other modes use indirection.
                return data[get_pos(num)]

            if op == 99: 
                #print('HALT')
                return None
            elif op in (1,2): # 1 or 2
                a, b = get_param(1), get_param(2)
                out_pos = get_pos(3)
                
                #print(out_pos, out_pos % 4)
                if op == 1:
                    data[out_pos] = a + b
                else:
                    data[out_pos] = a * b
            
                self.index += 4
            elif op== 3: # input
                #print('waiting for input')
                data[get_pos(1)] = self.inputs.pop(0)
                #print('got input', data[data[index+1]])
                self.index += 2
            elif op == 4:
                x = get_param(1)
                #print('PROGRAM OUPUT:', x)
                #print('output', x)
                #print('got after output', (yield x))
                self.index += 2
                return x
            elif op == 5: # jump if true
                x = get_param(1)
                if x != 0:
                    self.index = get_param(2)
                else:
                    self.index += 3
            elif op == 6: # jump if false
                x = get_param(1)
                if x == 0:
                    self.index = get_param(2)
                else:
                    self.index += 3
            elif op == 7: # less than
                a, b = get_param(1), get_param(2) 
                out_pos = get_pos(3)

                data[out_pos] = int(a < b)
                self.index += 4
            elif op == 8: # equals
                a, b = get_param(1), get_param(2) 
                out_pos = get_pos(3)

                data[out_pos] = int(a == b)
                self.index += 4
            elif op == 9:
                x = get_param(1)
                self.relbase += x
                self.index += 2
            else: 
                print('UNKNOWN OPCODE:', op)
    
    def run_to_halt(self):
        out = []
        while True: 
            x = self.run_to_output()
            if x is None:
                break 
            out.append(x)
        return out

    def run_to_input(self):
        out = []
        while True: 
            try:
                x = self.run_to_output()
            except IndexError:
                break
            if x is None:
                break 
            out.append(x)
        return out