from rich import print
import sys
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
    elif num_rotations in (1,3): 
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
    lowest_cost = find_cheapest_path(start_pos, maze, [])
    print(lowest_cost)

    return

def find_cheapest_path(
        pos: tuple[int, int],
        maze: list[str],
        cost: list[int] = [],
        visited: list[tuple[int, int]] = [],
        direction = (0, 1),
        lowest_cost = 1_000_100_000_000,
        depth = 0
):
    y, x = pos
    visited.append((y, x))

    for number_rot90 in range(4):
        direction = rotate_direction(direction)
        new_y, new_x = y+direction[0], x+direction[1]

        if depth >= 100:
            continue
        next_tile = maze[new_y][new_x]
        if next_tile == WALL:
            continue
        if (new_y, new_x) in visited:
            continue
        if next_tile == EXIT:
            sum_cost = sum(cost)
            sum_cost += rotation_cost((number_rot90+1)%4)+1
            if sum_cost < lowest_cost:
                lowest_cost = sum_cost
            return lowest_cost

        # path.append((new_y, new_x))
        cost.append(rotation_cost((number_rot90+1)%4)+1)
        lowest_cost = find_cheapest_path(
            (new_y, new_x), maze, cost, visited, direction, lowest_cost, depth+1)
        # path.pop()
        cost.pop()
        visited.pop()

    return lowest_cost

def inMaze(y, x, maze):
    sy = len(maze)
    sx = len(maze[0])
    if 0<=x<sx and 0<=y<sy:
        return True
    return False
    
def maze_sol(maze, path):
    out = ''
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if (r, c) in path:
                color = '[red]'
            elif char == WALL:
                color='[blue]'
            elif char == EXIT:
                color='[green]'
            elif char == START:
                color='[cyan]'
            elif char == EMPTY:
                color = '[black]'

            out+=f'{color}#'
        out+='\n'
    return out


if __name__ == "__main__":
    main()