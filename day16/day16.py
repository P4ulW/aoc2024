from rich import print
import sys
import heapq as hq
from math import cos, inf
sys.setrecursionlimit(10_000)
EMPTY = '.'
WALL = '#'
EXIT = 'E'
START = 'S'

DIRECTIONS = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0)
]

lowest_cost = 100_000


def rotate_direction(direction: tuple[int, int]) -> tuple[int, int]:
    return -direction[1], direction[0]


def rotation_cost(num_rotations: int) -> int:
    if num_rotations == 0:
        return 0
    elif num_rotations in (1, 3):
        return 1000
    elif num_rotations == 2:
        return 2000
    else:
        raise ValueError


def main():
    # part 1
    with open('./inputs.txt', 'r') as file:
        maze = [line.strip() for line in file.readlines()]
    # print(maze)
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == START:
                start_pos = (r, c)
    lowest_cost, paths = djikstra_maze(maze, start_pos)
    print(lowest_cost)

    # part 1
    tiles = set()
    for path in paths:
        y, x = start_pos
        tiles.add((y, x))
        d_idx = 0
        for char in path:
            if char == 'L':
                d_idx = (d_idx+1) % 4
                continue

            if char == 'R':
                d_idx = (d_idx-1) % 4
                continue

            if char == 'S':
                dy, dx = DIRECTIONS[d_idx]
                y, x = y+dy, x+dx
                tiles.add((y, x))
    print(len(tiles))

    return


def djikstra_maze(
    maze: list[str],
    start_pos: tuple[int, int],

):
    y, x = start_pos
    d_idx = 0
    costs = {(y, x, d_idx): 0}
    unexplored = []
    lowest_cost = inf
    paths = []

    hq.heappush(unexplored, (0, y, x, d_idx, ''))
    while len(unexplored) > 0:
        cost, y, x, d_idx, path = hq.heappop(unexplored)

        if lowest_cost < cost:
            continue

        if maze[y][x] == EXIT:
            lowest_cost = cost
            paths.append(path)
            continue

        if (y, x, d_idx) in costs and costs[(y, x, d_idx)] < cost:
            continue

        costs[(y, x, d_idx)] = cost

        new_y, new_x = y+DIRECTIONS[d_idx][0], x-DIRECTIONS[d_idx][1]
        if maze[new_y][new_x] != WALL:
            hq.heappush(
                unexplored, (cost+1, new_y, new_x, d_idx, path+'S'))

        hq.heappush(
            unexplored, (cost+1000, y, x, (d_idx+1) % 4, path+'L'))
        hq.heappush(
            unexplored, (cost+1000, y, x, (d_idx-1) % 4, path+'R'))

    return lowest_cost, paths


def maze_sol(maze, path):
    out = ''
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if (r, c) in path:
                color = '[red]'
            elif char == WALL:
                color = '[blue]'
            elif char == EXIT:
                color = '[green]'
            elif char == START:
                color = '[cyan]'
            elif char == EMPTY:
                color = '[black]'

            out += f'{color}#'
        out += '\n'
    return out


if __name__ == "__main__":
    main()
