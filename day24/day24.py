from typing import Literal
from re import findall
from random import randint
from rich import print
from collections import defaultdict
from itertools import combinations


def AND(left, right):
    return left and right


def OR(left, right):
    return left or right


def XOR(left, right):
    return left ^ right


operators = {
    'AND': AND,
    'OR': OR,
    'XOR': XOR,
}


def main():
    filename = './in.txt'
    with open(filename) as file:
        data = file.read()
        init_wires, gates = data.split('\n\n')
        init_wires = init_wires.split('\n')
        gates = gates.split('\n')[:-1]

    wire_states = dict()
    for wire in init_wires:
        label, state = wire.split(': ')
        wire_states[label] = int(state)

    to_calculate = {}
    for gate in gates:
        expr, res = gate.split(' -> ')
        expr = tuple(expr.split(' '))
        to_calculate[res] = expr

    # print(wire_states)
    # print(to_calculate)

    for wire in to_calculate.keys():
        state = calculate_wire(wire, wire_states, to_calculate)
        wire_states[wire] = state

    num = ''
    for i in range(99, -1, -1):
        key = f'z{str(i).zfill(2)}'
        if key not in wire_states:
            continue
        state = str(wire_states[key])
        num += state

    # print(wire_states)
    print("res part 1:", int(num, 2))


    to_calculate = swap_nodes('thm','z08',to_calculate)
    to_calculate = swap_nodes('wss','wrm',to_calculate)
    to_calculate = swap_nodes('z22','hwq',to_calculate)
    to_calculate = swap_nodes('z29','gbs',to_calculate)

    # tree = get_wire_diagramm(f'z29', to_calculate, 2)
    # print(tree)
    #
    # for i in range(45):
    #     tree = get_wire_diagramm(f'z{str(i).zfill(2)}', to_calculate, 2)
    #     print(tree)

    # for i in range(45):
    #     res = run_random_tests(i, 100, init_wires, to_calculate)
    #     print(i, res)

    swaps = sorted(['thm', 'z08', 'wss', 'wrm', 'z22', 'hwq', 'z29', 'gbs'])
    res2 = ",".join(list(swaps))
    print('res part 2:', res2)

                


    return

def swap_nodes(left, right, to_calculate):
    temp = to_calculate[left]
    to_calculate[left] = to_calculate[right]
    to_calculate[right] = temp
    return to_calculate


def run_random_tests(max_bit, num_test, init_wires, to_calculate):
    for i in range(num_test):
        x = randint(0, 2**max_bit-1)
        y = randint(0, 2**max_bit-1)
        success = correct_result(x, y, init_wires, to_calculate)
        if not success:
            return False
    return True


def set_wires_to_int(num: int, key: Literal['x', 'y'], wire_states):
    num = bin(num).removeprefix('0b').zfill(45)
    for idx, gnum in enumerate(range(44, -1, -1)):
        wire = key+str(gnum).zfill(2)
        wire_states[wire] = int(num[idx])


def get_wire_diagramm(wire, to_calculate, depth):
    out = ''

    left, op, right = to_calculate[wire]
    if depth>0 and not (left.startswith('x') or left.startswith('y')):
        left = get_wire_diagramm(left, to_calculate, depth-1)

    if depth>0 and not (right.startswith('x') or right.startswith('y')):
        right = get_wire_diagramm(right, to_calculate, depth-1)

    out += f'{wire} = ({left}) {op} ({right})'

    return out


def correct_result(x, y, init_wires, to_calculate):
    states = dict()
    for wire in init_wires:
        label, state = wire.split(': ')
        states[label] = int(state)
    set_wires_to_int(x, 'x', states)
    set_wires_to_int(y, 'y', states)

    for wire in to_calculate.keys():
        state = calculate_wire(wire, states, to_calculate)
        states[wire] = state

    num = '0b'
    for i in range(99, -1, -1):
        key = f'z{str(i).zfill(2)}'
        if key not in states:
            continue
        state = str(states[key])
        num += state

    num = int(num, 2)
    if num == x+y:
        return True

    return False

def calculate_wire(wire, wire_states, to_calculate):
    state = 0
    if wire in wire_states:
        return wire_states[wire]

    left, op, right = to_calculate[wire]
    if not left in wire_states:
        s = calculate_wire(left, wire_states, to_calculate)
        wire_states[left] = s

    if not right in wire_states:
        s = calculate_wire(right, wire_states, to_calculate)
        wire_states[right] = s

    left = wire_states[left]
    right = wire_states[right]

    state = operators[op](left, right)

    return state


if __name__ == "__main__":
    main()
    pass
