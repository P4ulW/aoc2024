from rich import print
from heapq import heappush, heappop
from math import inf, sqrt

DIRECTIONS = {
    'R': (0, 1),
    'U': (-1, 0),
    'L': (0, -1),
    'D': (1, 0),
}


def add_error_to_memoryspace(
    memory_space,
    coords,
    number_coords,
):
    for i, (x, y) in enumerate(coords):
        if i == number_coords:
            break
        memory_space[y][x] = '#'
    return memory_space


def inMemSpace(y, x, sy, sx):
    if 0 <= x < sx and 0 <= y < sy:
        return True
    return False


def bfs(
    memory_space,
    start_position=(0, 0),
    end_position=(6, 6),
):
    sy = len(memory_space)
    sx = len(memory_space[0])
    depth = 0
    visited = set()
    visited.add(start_position)
    queue = []
    queue.append((*start_position, depth))

    while queue:
        y, x, depth = queue.pop(0)

        for dy, dx in DIRECTIONS.values():
            ny, nx = y+dy, x+dx
            if not inMemSpace(ny, nx, sy, sx):
                continue

            if memory_space[ny][nx] == '#':
                continue

            if (ny, nx) in visited:
                continue

            if (ny, nx) == end_position:
                return depth+1

            queue.append((ny, nx, depth+1))
            visited.add((ny, nx))

    return -1


def manhattan_dist(y1, x1, y2, x2):
    return abs(y1-y2)+abs(x1-x2)


def repr_mmap(memory_space):
    out = ''
    for line in memory_space:
        for char in line:
            out += char
        out += '\n'
    return out


def path_from_path(path):
    y, x = 0, 0
    trajectory = []
    for char in path:
        dy, dx = DIRECTIONS[char]
        y, x = y+dy, x+dx
        trajectory.append((y, x))
    return trajectory


def maze_sol(maze, path):
    out = ''
    path = path_from_path(path)
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if (r, c) in path:
                color = '[red]'
            elif char == '#':
                color = '[blue]'
            elif char == '.':
                color = '[black]'

            out += f'{color}#'
        out += '\n'
    return out


def main():

    filename = './inputs.txt'
    file = open(filename)
    byte_coords = [line.strip().split(',') for line in file.readlines()]
    byte_coords = [(int(x), int(y)) for x, y in byte_coords]
    file.close()
    if 'test' in filename:
        memory_space = [['.']*7 for _ in range(7)]
    else:
        memory_space = [['.']*71 for _ in range(71)]

    memory_space = add_error_to_memoryspace(
        memory_space, byte_coords, 1024)
    steps = bfs(memory_space, end_position=(70, 70))
    print('part1:', steps)

    num = 2024
    while steps != -1:
        num += 1
        filename = './inputs.txt'
        file = open(filename)
        byte_coords = [line.strip().split(',') for line in file.readlines()]
        byte_coords = [(int(x), int(y)) for x, y in byte_coords]
        file.close()
        if 'test' in filename:
            memory_space = [['.']*7 for _ in range(7)]
        else:
            memory_space = [['.']*71 for _ in range(71)]

        memory_space = add_error_to_memoryspace(
            memory_space, byte_coords, num)
        steps = bfs(memory_space, end_position=(70, 70))
        # print(num, steps)
    # print(repr_mmap(memory_space))
    print('part2:', byte_coords[num-1])
    return


if __name__ == "__main__":
    main()
    pass
