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


def find_shortest_keystrokes(pad: Pad,
                             position: Point,
                             target_key: str):
    path = ''
    y, x = position
    padkey = pad[y][x]
    if padkey == target_key:
        return y, x, ['A',]
    visited = [(y, x)]
    next = []
    next.append((y, x, path))
    paths = []
    ty, tx = 0, 0
    while next:
        y, x, path = next.pop(0)
        for key, (dy, dx) in DIRECTIONS.items():
            ny, nx = y+dy, x+dx

            if not inKeypad(pad, (ny, nx)):
                continue
            padkey = pad[ny][nx]

            if (ny, nx) in visited:
                continue

            if padkey == ' ':
                continue

            # print('checking', ny, nx, path+key, visited)

            if padkey == target_key:
                paths.append(path+key+'A')
                ty, tx = ny, nx
                continue
                # return ny, nx, path+key+'A'

            visited.append((ny, nx))
            next.append((ny, nx, path+key))

    shortest_path = len(paths[0])
    paths = [path for path in paths if len(path) == shortest_path]
    return ty, tx, paths


def get_keypad_inputs(passcode):
    pos = (3, 2)
    total_paths = []
    for code in passcode:
        y, x, paths = find_shortest_keystrokes(keypad, pos, code)
        pos = (y, x)
        # total_paths.append(paths)
        total_paths.append(paths)

    allpaths = []
    for seg in total_paths:
        path = ''
        for sseg in seg:

    return total_paths


def get_controller_inputs(inputs):
    pos = (0, 2)
    totalpath = ''
    for code in inputs:
        y, x, paths = find_shortest_keystrokes(controller, pos, code)
        pos = (y, x)
        totalpath += paths[0]
    return totalpath


def main():
    filename = './test_inputs.txt'
    with open(filename) as file:
        data = [line.strip() for line in file.readlines()]

    passcode = data[0]
    path = get_keypad_inputs(passcode)
    print(path)
    # path = get_controller_inputs(path)
    # print(path)
    # path = get_controller_inputs(path)
    # print(path)
    # print()
    # print('<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A')
    # print("<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A ")
    # print('<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A')

    return


if __name__ == "__main__":
    main()
    pass
