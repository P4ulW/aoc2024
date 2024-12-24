from typing import Literal
from rich import print
from collections import defaultdict


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
    #
    # for wire in to_calculate.keys():
    #     state = calculate_wire(wire, wire_states, to_calculate)
    #     wire_states[wire] = state
    #
    # num = ''
    # for i in range(99, -1, -1):
    #     key = f'z{str(i).zfill(2)}'
    #     if key not in wire_states:
    #         continue
    #     state = str(wire_states[key])
    #     num += state
    #
    # print(wire_states)
    # print(int(num, 2))

    res = correct_result(10, 0, init_wires, to_calculate)
    print(res)
    return


def set_wires_to_int(num: int, key: Literal['x', 'y'], wire_states):
    num = bin(num).removeprefix('0b').zfill(44)
    for idx in range(43, -1, -1):
        wire = key+str(idx).zfill(2)
        wire_states[wire] = int(num[idx])


def get_wire_diagramm(wire, wire_states, to_calculate):
    out = ''

    left, op, right = to_calculate[wire]
    if not (left.startswith('x') or left.startswith('y')):
        left = get_wire_diagramm(left, wire_states, to_calculate)

    if not (right.startswith('x') or right.startswith('y')):
        right = get_wire_diagramm(right, wire_states, to_calculate)

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

    num = ''
    for i in range(99, -1, -1):
        key = f'z{str(i).zfill(2)}'
        if key not in states:
            continue
        state = str(states[key])
        num += state

    num = int(num)
    print(num)
    if num == x+y:
        return True

    return False


def input_to_zero(wire_states):
    for key in wire_states.keys():
        if 'x' in key:
            wire_states[key] = 0

        if 'y' in key:
            wire_states[key] = 0
    return wire_states


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
