from math import inf
from rich import progress
from rich.progress import track

def combo(registers, operand):
    if operand in [0, 1, 2, 3]:
        return operand
    if operand == 4:
        return registers['A']
    if operand == 5:
        return registers['B']
    if operand == 6:
        return registers['C']
    else:
        raise ValueError


def literal(registers, operand):
    return operand


def adv(
    registers,
    operand
):
    res = registers['A']/2**combo(registers,operand)
    registers['A'] = int(res)
    return registers


def bxl(
    registers,
    operand
):
    res = registers['B'] ^ literal(registers, operand)
    registers['B'] = res
    return registers


def bst(
    registers,
    operand
):
    res = combo(registers, operand) % 8
    registers['B'] = res
    return registers


def bxc(
    registers,
    operand
):
    res = registers['B'] ^ registers['C']
    registers['B'] = res
    return registers


def out(
    registers,
    operand
):
    res = combo(registers, operand) % 8
    return res



def bdv(
    registers,
    operand
):
    res = registers['A']/2**combo(registers,operand)
    registers['B'] = int(res)
    return registers



def cdv(
    registers,
    operand
):
    res = registers['A']/2**combo(registers,operand)
    registers['C'] = int(res)
    return registers

def run_programm(
    registers,
    programm,
    check_self_output = False,
    reference_output = None,
):
    ip = 0
    outputs=[]
    while ip < len(programm)-1:
        instruction = programm[ip]
        operand = programm[ip+1]
        if instruction == 0:
            registers = adv(registers, operand)

        elif instruction == 1:
            registers = bxl(registers, operand)

        elif instruction == 2:
            registers=bst(registers, operand)

        elif instruction == 3:
            if not registers['A'] == 0:
                ip = literal(registers, operand)
                continue

        elif instruction == 4:
            registers = bxc(registers, operand)

        elif instruction == 5:
            outputs.append(out(registers, operand))
            if check_self_output:
                if not outputs == reference_output[slice(None, len(outputs))]:
                    break

        elif instruction == 6:
            registers = bdv(registers, operand)

        elif instruction == 7:
            registers = cdv(registers, operand)

        ip += 2
    return outputs

def single_step(a):
    # decompiled program from puzzle input
    b = (a%8)
    b = b ^ 5
    c = int(a/2**b)
    b = b ^ 6 
    b = b ^ c
    out = b % 8
    a = int(a/8)
    return out

# reg A is build like this: 
# 8*(8*(8*(8*(3*8 + 0) + 3) + 3) + 0)+0

def find_a(num, col, target, found = []):
    if single_step(num) != target[-(col+1)]:
        return found 
    if col == len(target) -1:
        found.append(num)
    else:
        for next_match_num in range(8):
            found = find_a(num*8 + next_match_num, col+1, target, found)
    return found

    
def main():

    reg = {
        'A': 0,
        'B': 0,
        'C': 0,
    }
    programm = [2,4,1,5,7,5,1,6,4,3,5,5,0,3,3,0]
    out = run_programm(reg, programm)
    print(out)
    A = []
    for init_num in range(8):
        A.append(find_a(init_num, 0, programm))
    print(sorted(A)[0][0])
    # print(out)
    # print(single_step(10))





    # # programm = [0,3,5,4,3,0]
    # for i in track(range(200_000_000), total=200_000_000):
    #     reg = {
    #         'A': i,
    #         'B': 0,
    #         'C': 0,
    #     }
    #     output = run_programm(reg, programm, True, programm)
    #     if output == programm:
    #         print(i)
    #         break
    # output = run_programm(reg, programm)
    # print(output)
    # print(reg)
            
        
    return


if __name__ == "__main__":
    main() 
    pass
