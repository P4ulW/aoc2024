from rich import print
import sys
import heapq as hq
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
    with open('./inputs.txt', 'r') as file:
        maze = [line.strip() for line in file.readlines()]
    print(maze)
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == START:
                start_pos = (r, c)
    lowest_cost = djikstra_maze(maze, start_pos)
    print(lowest_cost)

    return


def djikstra_maze(
    maze: list[str],
    start_pos: tuple[int, int],

):
    y, x = start_pos
    direction = (0, 1)
    costs = {(y, x): 0}
    unexplored = []

    hq.heappush(unexplored, (0, y, x, direction))
    while len(unexplored) > 0:
        cost, y, x, direction = hq.heappop(unexplored)
        for number_rot90 in range(4):
            direction = rotate_direction(direction)
            new_y, new_x = y+direction[0], x+direction[1]
            added_cost = rotation_cost((number_rot90+1) % 4)+1
            next_cost = costs[(y, x)] + added_cost
            next_tile = maze[new_y][new_x]

            if next_tile == WALL:
                continue
            if next_tile == EXIT:
                print('done')
                return costs[(y, x)] + added_cost
            if next_tile == EMPTY:
                if costs.get((new_y, new_x)) is None:
                    costs[(new_y, new_x)] = next_cost
                    hq.heappush(
                        unexplored, (next_cost, new_y, new_x, direction))
                else:
                    costs[(new_y, new_x)] = min(
                        next_cost, costs[(new_y, new_x)])

    return costs

# def find_cheapest_path(
#         pos: tuple[int, int],
#         maze: list[str],
#         path: list[tuple[int, int]],
#         cost: list[int] = [],
#         visited: list[tuple[int, int]] = [],
#         direction=(0, 1),
#         lowest_cost=1_000_100_000_000,
#         depth=0
# ):
#     y, x = pos
#     visited.append((y, x))
#
#     for number_rot90 in range(4):
#         direction = rotate_direction(direction)
#         new_y, new_x = y+direction[0], x+direction[1]
#
#         if sum(cost) > lowest_cost:
#             return lowest_cost
#         next_tile = maze[new_y][new_x]
#         if next_tile == WALL:
#             continue
#         if (new_y, new_x) in visited:
#             continue
#         if next_tile == EXIT:
#             # print(f'found exit with cost {sum(cost)}')
#             # print(list(zip(path, cost)))
#             sum_cost = sum(cost)
#             sum_cost += rotation_cost((number_rot90+1) % 4)+1
#             if sum_cost < lowest_cost:
#                 lowest_cost = sum_cost
#                 print(maze_sol(maze, path))
#             return lowest_cost
#
#         path.append((new_y, new_x))
#         cost.append(rotation_cost((number_rot90+1) % 4)+1)
#         lowest_cost = find_cheapest_path(
#             (new_y, new_x), maze, path, cost, visited, direction, lowest_cost, depth+1)
#         path.pop()
#         cost.pop()
#         visited.pop()
#
#     return lowest_cost


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
