from collections import defaultdict
from itertools import combinations
from rich import print

MAX_ORDER = 100


def load_map(filename):
    file = open(filename, 'r')
    data = [[char for char in line.strip()] for line in file.readlines()]
    return data


def print_map(data):
    for line in data:
        print(line)


def get_antenna_locations(antenna_map: list[list[str]]):
    antenna_dict = defaultdict(list)
    for y, row in enumerate(antenna_map):
        for x, char in enumerate(row):
            if not char == '.':
                antenna_dict[char].append([x, y])

    return antenna_dict


def get_antinode_positions(
        antenna1: list[int],
        antenna2: list[int],
    order: int = 1,
) -> list[list[int]]:
    vec_x = antenna1[0] - antenna2[0]
    vec_y = antenna1[1] - antenna2[1]
    center_x = (antenna1[0] + antenna2[0]) / 2
    center_y = (antenna1[1] + antenna2[1]) / 2
    node1_x = int(center_x + (1/2+order)*vec_x)
    node1_y = int(center_y + (1/2+order)*vec_y)
    node2_x = int(center_x - (1/2+order)*vec_x)
    node2_y = int(center_y - (1/2+order)*vec_y)
    node_positions = [
        [node1_x, node1_y],
        [node2_x, node2_y],
    ]

    return node_positions


def get_empty_antinode_grid(antenna_map):
    antinode_grid = [[0 for i in row] for row in antenna_map]
    return antinode_grid


def place_node_in_grid(node, antinode_grid):
    x, y = node
    sy = len(antinode_grid)
    sx = len(antinode_grid[0])

    if x < 0 or x > sx-1:
        return antinode_grid
    if y < 0 or y > sy-1:
        return antinode_grid
    antinode_grid[y][x] = 1
    return antinode_grid


def main():
    data = load_map('./inputs.txt')
    # print_map(data)
    antennas = get_antenna_locations(data)

    # part 1
    antinode_grid = get_empty_antinode_grid(data)
    for positions in antennas.values():
        for comb in combinations(positions, 2):
            nodes = get_antinode_positions(*comb)
            for node in nodes:
                antinode_grid = place_node_in_grid(node, antinode_grid)

    result = sum([sum(line) for line in antinode_grid])
    print('part1: ', result)

    # part 2
    antinode_grid = get_empty_antinode_grid(data)
    for positions in antennas.values():
        for comb in combinations(positions, 2):
            for order in range(MAX_ORDER):
                nodes = get_antinode_positions(*comb, order)
                for node in nodes:
                    antinode_grid = place_node_in_grid(
                        node, antinode_grid)

    result = sum([sum(line) for line in antinode_grid])
    print('part2: ', result)
    pass


if __name__ == "__main__":
    main()
    # from timeit import timeit
    # print(timeit(main, number=100))
