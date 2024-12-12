from os import walk
from typing import Literal


colors = [
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'magenta',
    'cyan',
    'white',
    'bright_black',
    'bright_red',
    'bright_green',
    'bright_yellow',
    'bright_blue',
    'bright_magenta',
    'bright_cyan',
    'bright_white',
    'grey0',
    'navy_blue',
    'dark_blue',
    'blue3',
    'blue1',
    'dark_green',
    'deep_sky_blue4',
    'dodger_blue3',
    'dodger_blue2',
    'green4',
]

DIRECTIONS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
]


def perpendicular_direction(dy: int, dx: int) -> tuple[int, int]:
    return dx, -dy


def isValidMove(row, col, garden) -> bool:
    size_y = len(garden)
    size_x = len(garden[0])
    if 0 <= row < size_y and 0 <= col < size_x:
        return True
    else:
        return False


def get_plant_field_coords(
    row: int,
    col: int,
    plant: str,
    garden: list[list[str]],
    visited: list[list[int]],
    plant_field: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    plant_field.append((row, col))
    visited[row][col] = 1
    for dr, dc in DIRECTIONS:
        new_row, new_col = row+dr, col+dc

        if not isValidMove(new_row, new_col, garden):
            continue

        if visited[new_row][new_col]:
            continue

        if (garden[new_row][new_col] == plant):
            visited[new_row][new_col] = 1
            plant_field = get_plant_field_coords(
                new_row, new_col, plant, garden, visited, plant_field)

    return plant_field


def calc_field_fence_number(
    field: list[tuple[int, int]],
    garden: list[list[str]],
) -> int:
    plant = garden[field[0][0]][field[0][1]]
    fences = 0
    for row, col in field:
        for dr, dc in DIRECTIONS:
            new_row, new_col = row+dr, col+dc
            if not isValidMove(new_row, new_col, garden):
                fences += 1

            elif not garden[new_row][new_col] == plant:
                fences += 1

    return fences


def calc_field_area(field: list[tuple[int, int]]) -> int:
    return len(field)


def calc_cost(fences: int, area: int) -> int:
    return fences * area


def calc_field_cost(
    field: list[tuple[int, int]],
    garden: list[list[str]]
) -> int:

    fences = calc_field_fence_number(field, garden)
    area = calc_field_area(field)
    return calc_cost(fences, area)


def get_edges_field(
    field: list[tuple[int, int]],
    garden: list[list[str]],
) -> int:
    local_garden = [[char for char in line]
                    for line in garden]
    plant = local_garden[field[0][0]][field[0][1]]
    edges = 0
    (rmin, cmin), (rmax, cmax) = get_bounding_box_vertices(field)
    for row in range(rmin, rmax+1):
        for col in range(cmin, cmax+1):
            if (row, col) not in field:
                local_garden[row][col] = '_'

    if rmin == rmax:
        return 4
    if cmin == cmax:
        return 4

    for direction in DIRECTIONS:
        edgemap = [[stepIsEdge(row, col, direction, plant, local_garden)
                    for col in range(cmin, cmax+1)]
                   for row in range(rmin, rmax+1)]
        if direction[0] == 0:
            edges += edges_from_edgemap(edgemap, 'y')

        else:
            edges += edges_from_edgemap(edgemap, 'x')
        # for edge in edgemap:
        #     print(edge)
        # print(edges)
        # print('\n')

    return edges


def edges_from_edgemap(
        emap: list[list[int]],
        direction: str) -> int:
    edges = 0
    if direction == 'x':
        for r in range(len(emap)):
            prev = 0
            for num in emap[r]:
                if prev == 0 and num == 1:
                    edges += 1
                prev = num
        return edges

    elif direction == 'y':
        for c in range(len(emap[0])):
            prev = 0
            for r in range(len(emap)):
                num = emap[r][c]
                # print(f'r: {r} c: {c} num: {num} prev: {prev}')
                if prev == 0 and num == 1:
                    edges += 1
                prev = num
        return edges

    else:
        raise ValueError


def stepIsEdge(
        row: int,
        col: int,
        dir: tuple[int, int],
        plant: str,
        garden: list[list[str]]) -> int:
    isEdge = 0
    dr, dc = dir
    char_before = garden[row][col]
    if not isValidMove(row+dr, col+dc, garden):
        if char_before == plant:
            return 1
        return 0
    char_after = garden[row+dr][col+dc]
    if char_before != char_after and char_before == plant:
        return 1
    return isEdge


def get_bounding_box_vertices(
    field: list[tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    rmin, rmax = 1000, 0
    cmin, cmax = 1000, 0
    for row, col in field:
        rmin = min(rmin, row)
        rmax = max(rmax, row)
        cmin = min(cmin, col)
        cmax = max(cmax, col)
    return (rmin, cmin), (rmax, cmax)


def main():
    file = open('./inputs.txt', 'r')
    garden = [[char
               for char in line.strip()]
              for line in file.readlines()]
    for row in garden:
        print(row)
    visited = [[0 for _ in line]
               for line in garden]

    fields = []
    for row in range(len(garden)):
        for col in range(len(garden[0])):
            if visited[row][col] == 1:
                continue
            plant = garden[row][col]
            fields.append(
                get_plant_field_coords(row, col, plant, garden, visited, []))

    total_cost = 0
    for field in fields:
        edges = get_edges_field(field, garden)
        plant = garden[field[0][0]][field[0][1]]
        cost = calc_cost(edges, calc_field_area(field))
        total_cost += cost
        print(
            f'Field {plant} egdes: {edges}, cost: {cost}')

    print(f'part 2: {total_cost}')
    pass


if __name__ == "__main__":
    main()
    pass
