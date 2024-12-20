from rich import print
from functools import lru_cache
START = 'S'
END = 'E'
TRACK = '.'
WALL = '#'

Grid = list[list[str]]
Point = tuple[int, int]

DIRECTIONS = {
    'L' : (0, 1),
    'R' : (0, -1),
    'U' : (-1, 0),
    'D' : (1, 0),
}


@lru_cache
def manhattan_dist(p1:Point, p2:Point):
    dist = abs(p1[0]-p2[0])
    dist += abs(p1[1]-p2[1])
    return dist


def track_from_path(
        path: str,
        start: Point,
):
    track = [start]
    y, x = start
    for char in path:
        dy, dx = DIRECTIONS[char]
        y, x = y+dy, x+dx
        track.append((y, x))
    return track


def inMaze(maze: Grid,
        point: Point
):
    sy = len(maze)
    sx = len(maze[0])
    y,x = point
    if 0<=x<sx and 0<=y<sy:
        return True
    return False


def maze_sol(maze, path, start):
    out = ''
    color = ''
    path = track_from_path(path, start)
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if (r, c) in path:
                color = '[red]'
            elif char == '#':
                color = '[blue]'
            elif char == '.':
                color = '[black]'

            out += f'{color}{char}'
            # out += char
        out += '\n'
    return out


def get_length_to_end(
        maze: Grid,
        end: Point,
        point: Point,
        visited = [],
        path = '',
        ):

    y, x = point
    while (y,x) != end:
        for key, (dy, dx) in DIRECTIONS.items():
            ny, nx = y+dy, x+dx
            if (ny, nx) in visited:
                continue

            if maze[ny][nx] == WALL:
                continue

            visited.append((y, x))
            path += key
            y, x = ny, nx

    return path


def get_shortcuts(
        track: list[Point],
        cheat_cost: int,
):
    count = 0
    for left, point in enumerate(track):
        y, x = point
        for right, point in enumerate(track):
            if not left < right:
                continue

            if not manhattan_dist(track[left], track[right]) == 2:
                continue

            cost_before = left
            cost_after = right 
            if cost_after >= cost_before + 2 + cheat_cost:
                count += 1
    return count

def get_updated_shortcuts(
        track: list[Point],
        cheat_cost: int,
):
    count = 0
    for left, _ in enumerate(track[slice(None, -cheat_cost)]):
        # counts = [1 for
        #  right, _ in enumerate(track)
        #  if ((left < right)
        #      and (manhattan_dist(track[left], track[right])>20)
        #      and (right >= left + cheat_cost + manhattan_dist(track[left], track[right])))]
        # count += sum(counts)
        for right, _ in enumerate(track[slice(left+cheat_cost, None)]):
            right = right + left + cheat_cost
            if not left < right:
                continue

            mdist = manhattan_dist(track[left], track[right])
            if mdist > 20:
                continue

            cost_before = left
            cost_after = right 
            # print(cost_before, cost_after)
            if cost_after >= cost_before + mdist + cheat_cost:
                count += 1
    return count
    

def main():
    with open('./inputs.txt', 'r') as file:
        data = [line.strip() for line in file.readlines()]
        maze = [[char for char in line ] for line in data]
        pass
    start = (0, 0)
    end = (0, 0)
    for r, row in enumerate(data):
        for  c,char in enumerate(row):
            if char == START:
                start = (r, c)
            if char == END:
                end = (r, c)


    # part 1
    path = get_length_to_end(maze, end, start, [])
    track = track_from_path(path, start)

    # shortcuts = get_shortcuts(track, 100)
    # print(f'part 1: {shortcuts}')

    # part 2
    shortcuts = get_updated_shortcuts(track, 100)
    print(f'part 2: {shortcuts}')

    return

if __name__ == '__main__':
    main()
