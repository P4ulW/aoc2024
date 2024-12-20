from rich import print
from collections import defaultdict
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
        maze: Grid,
        track: list[Point],
        cheat_cost: int,
):
    count = 0
    for left, point in enumerate(track):
        y, x = point
        for key, (dy,dx) in DIRECTIONS.items():
            cheat_start_pos = (y+dy, x+dx)
            cheat_end_pos = (y+2*dy, x+2*dx)
            if not inMaze(maze, cheat_end_pos):
                continue

            if not maze[cheat_start_pos[0]][cheat_start_pos[1]] == WALL:
                continue

            if maze[cheat_end_pos[0]][cheat_end_pos[1]] == WALL:
                continue

            cost_before = left
            cost_after = track.index(cheat_end_pos) 
            if cost_after >= cost_before + 2 + cheat_cost:
                count += 1
    return count

def get_updated_shortcuts(
        maze: Grid,
        track: list[Point],
        cheat_cost: int,
):

    count = 0
    for left, point in enumerate(track[:-1]):
        y, x = point
        for (dy,dx) in DIRECTIONS.values():
            cheat_start_pos = (y+dy, x+dx)

            if not maze[cheat_start_pos[0]][cheat_start_pos[1]] == WALL:
                continue

            for right, (ey, ex) in enumerate(track): 
                if left > right:
                     continue

                cheat_end_pos = (ey, ex)
                dist = manhattan_dist((y, x), cheat_end_pos)
                if dist > 20:
                    continue



                cost_before = left
                cost_after = right
                if cost_after == cost_before + dist + cheat_cost:
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

    shortcuts = get_shortcuts(maze, track, 100)
    print(f'part 1: {shortcuts}')

    # # part 2
    # shortcuts = get_updated_shortcuts(maze, track, 50)
    # print(f'part 2: {shortcuts}')

    return

if __name__ == '__main__':
    main()
