from collections import defaultdict
DIRECTIONS = {
    '<': (0, -1),
    '>': (0, 1),
    '^': (-1, 0),
    'v': (1, 0),
}
WALL = '#'
BOX = 'O'
ROBOT = '@'
EMPTY = '.'
BOX_LEFT = '['
BOX_RIGHT = ']'



def get_warehouse_and_movements(
    filename
) -> tuple[list[list[str]], str]:
    file = open(filename, 'r')
    input = [line.strip() for line in file.readlines()]
    warehouse = []
    movements = ''
    partial = False
    for line in input:
        if partial:
            for char in line:
                movements += char
            continue
        if line == '':
            partial = True
            continue
        warehouse.append([char for char in line])
    return warehouse, movements


def do_movement(
        warehouse: list[list[str]],
        robot_position: tuple[int, int],
        movement: str
):
    new_warehouse = warehouse
    direction = DIRECTIONS[movement]
    new_robot_y = robot_position[0]+direction[0]
    new_robot_x = robot_position[1]+direction[1]

    if new_warehouse[new_robot_y][new_robot_x] == WALL:
        return new_warehouse, robot_position

    if warehouse[new_robot_y][new_robot_x] == BOX:
        new_warehouse = push_box(
            warehouse, (new_robot_y, new_robot_x), movement)

    if new_warehouse[new_robot_y][new_robot_x] == EMPTY:
        new_warehouse[new_robot_y][new_robot_x] = ROBOT
        new_warehouse[robot_position[0]][robot_position[1]] = EMPTY
        robot_position = (new_robot_y, new_robot_x)

    return new_warehouse, robot_position


def push_box(
        warehouse: list[list[str]],
        position: tuple[int, int],
        movement: str
):
    new_warehouse = warehouse
    direction = DIRECTIONS[movement]
    new_y = position[0]+direction[0]
    new_x = position[1]+direction[1]

    if new_warehouse[new_y][new_x] == WALL:
        return new_warehouse

    if warehouse[new_y][new_x] == BOX:
        new_warehouse = push_box(
            new_warehouse, (new_y, new_x), movement)

    if new_warehouse[new_y][new_x] == EMPTY:
        new_warehouse[position[0]][position[1]] = EMPTY
        new_warehouse[new_y][new_x] = BOX

    return new_warehouse


def get_robot_pos(warehouse):
    for r, row in enumerate(warehouse):
        for c, char in enumerate(row):
            if char == ROBOT:
                return (r, c)
    return (0, 0)


def print_warehouse(warehouse):
    full_out = ''
    for row in warehouse:
        out = ''
        for char in row:
            out += char
        out += '\n'
        full_out += out
    return full_out


def calc_checksum(
    warehouse: list[list[str]],
):
    num = 0
    for r, row in enumerate(warehouse):
        for c, char in enumerate(row):
            if char == BOX:
                num += 100*r + c

    return num


def calc_checksum_wide(
    warehouse: list[list[str]],
):
    num = 0
    for r, row in enumerate(warehouse):
        for c, char in enumerate(row):
            if char == BOX_LEFT:
                num += 100*r + c

    return num


def widen(
    warehouse: list[list[str]],
):
    wide_warehouse = []
    for row in warehouse:
        wide_row = []
        for char in row:
            if char == BOX:
                wide_row.append('[')
                wide_row.append(']')
            elif char == EMPTY:
                wide_row.append(EMPTY)
                wide_row.append(EMPTY)
            elif char == WALL:
                wide_row.append(WALL)
                wide_row.append(WALL)
            elif char == ROBOT:
                wide_row.append(ROBOT)
                wide_row.append(EMPTY)
        wide_warehouse.append(wide_row)
    return wide_warehouse


def do_movement_wide(
        warehouse: list[list[str]],
        robot_position: tuple[int, int],
        movement: str
):
    new_warehouse = warehouse
    direction = DIRECTIONS[movement]
    new_robot_y = robot_position[0]+direction[0]
    new_robot_x = robot_position[1]+direction[1]

    if new_warehouse[new_robot_y][new_robot_x] == WALL:
        return new_warehouse, robot_position

    if warehouse[new_robot_y][new_robot_x] in (BOX_LEFT, BOX_RIGHT):
        new_warehouse = push_box_wide(
            warehouse, (new_robot_y, new_robot_x), movement)

    if new_warehouse[new_robot_y][new_robot_x] == EMPTY:
        new_warehouse[new_robot_y][new_robot_x] = ROBOT
        new_warehouse[robot_position[0]][robot_position[1]] = EMPTY
        robot_position = (new_robot_y, new_robot_x)

    return new_warehouse, robot_position


    

def push_box_wide(
        warehouse: list[list[str]],
        position: tuple[int, int],
        movement: str,
):
    current_box = warehouse[position[0]][position[1]]
    new_warehouse = [row.copy() for row in warehouse]
    direction = DIRECTIONS[movement]
    new_y = position[0]+direction[0]
    new_x = position[1]+direction[1]
    if movement in ['<', '>']:
        if new_warehouse[new_y][new_x] == WALL:
            return new_warehouse

        if warehouse[new_y][new_x] in (BOX_LEFT, BOX_RIGHT):
            new_warehouse = push_box_wide(
                new_warehouse, (new_y, new_x), movement)

        if new_warehouse[new_y][new_x] == EMPTY:
            new_warehouse[position[0]][position[1]] = EMPTY
            new_warehouse[new_y][new_x] = current_box

    elif movement in ['^', 'v']:
        boxes = find_all_boxes(movement, position, warehouse)
        if movement == '^':
            boxes = sorted(boxes, reverse=False)
        else:
            boxes = sorted(boxes, reverse=True)
        print(boxes)

        for box in boxes:
            movePossible = check_box_move(box, movement, new_warehouse)
            if not movePossible:
                return warehouse
            else:
                y, x = box
                new_y, new_x = y+direction[0], x+direction[1]
                new_warehouse[new_y][new_x] = new_warehouse[y][x]
                new_warehouse[y][x] = EMPTY
         
    return new_warehouse


def find_all_boxes(
        movement: str,
        position: tuple[int, int],
        warehouse: list[list[str]],
        seen: list[int] = []
) -> list[tuple[int, int]]:
    current_box = warehouse[position[0]][position[1]]
    y, x = position
    direction = DIRECTIONS[movement]
    new_y = y+direction[0]
    new_x = x+direction[1]
    boxes = []

    boxes.append((y, x))

    if warehouse[new_y][new_x] == WALL:
        return boxes
    elif warehouse[new_y][new_x] in (BOX_RIGHT, BOX_LEFT):
        to_add_boxes = find_all_boxes(movement, (new_y, new_x), warehouse, boxes)
        for box in to_add_boxes:
            if box not in boxes:
                boxes.append(box)

    if current_box == BOX_LEFT and (y, x+1) not in seen:
        to_add_boxes = find_all_boxes(movement, (y, x+1), warehouse, boxes)
        for box in to_add_boxes:
            if box not in boxes:
                boxes.append(box)

    elif current_box == BOX_RIGHT and (y, x-1) not in seen:
        to_add_boxes = find_all_boxes(movement, (y, x-1), warehouse, boxes)
        for box in to_add_boxes:
            if box not in boxes:
                boxes.append(box)


    return boxes


def check_box_move(
        box: tuple[int, int],
        movement: str,
        warehouse: list[list[str]]
) -> bool:
    y, x = box
    direction = DIRECTIONS[movement]
    new_y, new_x = y+direction[0], x+direction[1]
    if warehouse[new_y][new_x] == EMPTY:
        return True
    else:
        return False


def main():
    warehouse, movements = get_warehouse_and_movements('./inputs.txt')

    print(movements)
    for row in warehouse:
        print(row)

    robot_position = get_robot_pos(warehouse)
    print(robot_position)

    for movement in movements:
        warehouse, robot_position = do_movement(
            warehouse, robot_position, movement)
        # print('move', movement, ':')
        # print_warehouse(warehouse)
        # print('\n')

    res = calc_checksum(warehouse)
    print('part 1:', res)

    warehouse, movements = get_warehouse_and_movements('./inputs.txt')
    warehouse = widen(warehouse)
    robot_position = get_robot_pos(warehouse)
    print(robot_position)

    # print(print_warehouse(warehouse))
    # boxes = find_all_boxes('^', (5, 6), warehouse)
    # print(boxes)
    print_warehouse(warehouse)
    for movement in movements:
        warehouse, robot_position = do_movement_wide(
            warehouse, robot_position, movement)
        # print('move', movement, ':')
        # print(print_warehouse(warehouse))
        # print('\n')
        # input('enter')
    #
    #     # print(print_warehouse(warehouse))
    #     # with open('out.txt', 'w') as file:
    #     #     file.write(print_warehouse(warehouse))
    #     # input('enter')
    #

    print(print_warehouse(warehouse))
    print('\n')
    res = calc_checksum_wide(warehouse)
    print('part 2:', res)
    return


if __name__ == "__main__":
    main()
    pass
