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
    [0, 1],
    [1, 0],
    [-1, 0],
    [0, -1]
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
    plant = garden[field[0][0]][field[0][1]]
    edges = 0
    (rmin, cmin), (rmax, cmax) = get_bounding_box_vertices(field)

    if rmin == rmax:
        return 4
    if cmin == cmax:
        return 4

    # edges down-up
    for row in range(rmin, rmax+1):
        prev_valid = False
        for col in range(cmin, cmax+1):
            print(f'r: {row}, c: {col}, valid: {prev_valid}')
            if not garden[row][col] == plant:
                if prev_valid:
                    print("found edge throug invalid char")
                    prev_valid = False
                    edges += 1
                continue

            if (col == cmax) and prev_valid:
                print("found edge through end")
                edges += 1
                continue

            if not isValidMove(row-1, col, garden):
                prev_valid = True

            if not garden[row - 1][col] == plant:
                prev_valid = True

            if prev_valid:
                print('egde found through invalid')
                edges += 1

    return edges


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
    file = open('./test_inputs.txt', 'r')
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
    # total_cost = 0
    # for field in fields:
    #     print(field)
    #     total_cost += calc_field_cost(field, garden)
    # print(f'part 1: {total_cost}')
    print(fields[0])
    print(get_bounding_box_vertices(fields[0]))
    print(get_edges_field(fields[0], garden))

    pass


if __name__ == "__main__":
    main()
    pass
