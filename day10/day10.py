
from rich import print
from rich.progress import track
from functools import lru_cache

DIRECTIONS = [
    [1, 0],
    [0, 1],
    [-1, 0],
    [0, -1]
]


def repr_topo(topo_map):
    out = ''
    out += '\n'
    for row in topo_map:
        for char in row:
            out += str(char)

        out += '\n'
    return out


def print_trail(topo_map, trail):
    out = ''
    for r, row in enumerate(topo_map):
        for c, char in enumerate(topo_map[r]):
            if (r, c) in trail:
                out += f'[red][bold]{char}'
            else:
                out += f'[white]{char}'
        out += '\n'

    return out


def determine_trail_score(
    topo_map: list[list[int]],
    row: int,
    col: int,
    trail: list[tuple[int, int]],
    head_score: dict[tuple[int, int], int],
    visited: set[tuple[int, int]] | None = None,
):
    current_num = topo_map[row][col]
    next_num = current_num + 1

    if current_num == 9:
        # print((row, col), visited, not (row, col) in visited)
        if visited is None or not (row, col) in visited:
            # print('new finish!')
            # print(print_trail(topo_map, trail))
            head_score[trail[0]] = head_score.get(trail[0], 0) + 1
            # print(head_score[trail[0]])

            if not visited is None:
                visited.add((row, col))

        return

    for drow, dcol in DIRECTIONS:
        if not isValidMove(topo_map, row+drow, col+dcol):
            continue

        if topo_map[row+drow][col+dcol] == next_num:
            trail.append((row+drow, col+dcol))
            determine_trail_score(topo_map, row+drow,
                                  col+dcol, trail, head_score,
                                  visited)
            trail.pop()


def isValidMove(topo_map, row, col):
    return (0 <= row < len(topo_map)
            and 0 <= col < len(topo_map[0]))


def main():
    with open('./inputs.txt', 'r') as file:
        topo_map = [[int(char) for char in line.strip()]
                    for line in file.readlines()]
    print(repr_topo(topo_map))

    trailheads = [(row, col)
                  for row in range(len(topo_map))
                  for col in range(len(topo_map[0]))
                  if topo_map[row][col] == 0]

    head_score = {pos: 0 for pos in trailheads}

    for row, col in trailheads:
        visited = set()
        determine_trail_score(topo_map, row, col, [
                              (row, col)], head_score, visited)

    # print(head_score)
    print(sum(head_score.values()))

    head_score = {pos: 0 for pos in trailheads}

    for row, col in trailheads:
        visited = None
        determine_trail_score(topo_map, row, col, [
                              (row, col)], head_score, visited)

    # print(head_score)
    print(sum(head_score.values()))

    return


if __name__ == "__main__":
    main()
