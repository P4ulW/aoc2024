from rich import print
from functools import cache
import itertools as it


Pad = tuple[str]
Point = tuple[int, int]

keypad = (
    '789',
    '456',
    '123',
    ' 0A',
)

controller = (
    ' ^A',
    '<v>',
)

DIRECTIONS = {
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
    '^': (-1, 0),
}


@cache
def inKeypad(pad: Pad, pos: Point):
    sy = len(pad)
    sx = len(pad[0])
    y, x = pos
    if 0 <= x < sx and 0 <= y < sy:
        return True
    return False


@cache
def find_key_index(
    pad: Pad,
    key: str,
):
    for y, x in it.product(range(len(pad)), range(len(pad[0]))):
        if pad[y][x] == key:
            return (y, x)
    raise ValueError(f'k {key} not in pad')


def find_keypath(
        pad: Pad,
        start_key: str,
        target_key: str,
):
    sy, sx = find_key_index(pad, start_key)
    ey, ex = find_key_index(pad, target_key)

    if (sy, sx) == (ey, ex):
        return ['']

    dy = ey - sy
    dx = ex - sx
    y_moves = 'v'*dy if dy > 0 else '^'*-dy
    x_moves = '>'*dx if dx > 0 else '<'*-dx

    if dy == 0:
        return [x_moves]
    if dx == 0:
        return [y_moves]

    if pad[sy][ex] == ' ':
        return [y_moves+x_moves]

    if pad[ey][sx] == ' ':
        return [x_moves+y_moves]

    return [x_moves+y_moves, y_moves+x_moves]


@cache
def get_inputs(code, depth):
    if depth == 1:
        return len(code)

    if any(char in code for char in '0123456789'):
        pad = keypad
    else:
        pad = controller

    res = 0
    for start, end in zip('A'+code, code):
        paths = find_keypath(pad, start, end)
        res += min(get_inputs(path+'A', depth-1) for path in paths)
    return res


def complexity(code, num_levels):
    return get_inputs(code, num_levels) * int(code.strip('A'))


def main():
    filename = './inputs.txt'
    with open(filename) as file:
        data = [line.strip() for line in file.readlines()]

    res1 = sum(complexity(code, 4) for code in data)
    print(f'res 1: {res1}')

    res2 = sum(complexity(code, 1+25+1) for code in data)
    print(f'res 2: {res2}')
    return


if __name__ == "__main__":
    main()
    pass
