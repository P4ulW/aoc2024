from rich import print
from rich.progress import track

DIRECTIONS = [
    [0, -1],
    [1, 0],
    [0, 1],
    [-1, 0]
]


def load_board(filename):
    file = open(filename, 'r')
    board = [[char for char in line.strip()]
             for line in file.readlines()]
    for y, row in enumerate(board):
        for x, col in enumerate(board[y]):
            char = board[y][x]
            if char == '.':
                board[y][x] = 0
            if char == '#':
                board[y][x] = 2
            if char == '^':
                board[y][x] = 1

    return board


def main():
    print('Start')
    board = load_board('./inputs.txt')
    x, y, = find_start_position(board)
    print(x, y)
    res = traverse_board(board, track_pos=True)
    print('res 1:', res['visited_squares'])
    print(res['isLoop'])

    res2 = 0
    pos_ostacles = res['visited_positions'].copy()
    for pos in track(pos_ostacles,
                     total=(len(pos_ostacles))):
        if pos == [x, y]:
            continue
        new_board = place_obstruction(pos[0], pos[1], board)
        _ = traverse_board(new_board)
        if _['isLoop']:
            res2 += 1

    print('res 2:', res2)
    print('done')
    pass
# --------------------------------------------------- #


def find_start_position(board: list[list[str]]) -> list[int]:
    for j, line in enumerate(board):
        for i, char in enumerate(line):
            if not char == 1:
                continue
            return [i, j]
    return []
# --------------------------------------------------- #


def traverse_board(board: list[list[str]], track_pos=False) -> dict:
    x, y = find_start_position(board)
    dir_index = 0
    visited_squares = 0
    visited_positions = []
    isLoop = False

    size_y = len(board)
    size_x = len(board[0])
    visited_positions_board = [[0 for _ in range(size_x)]
                               for _ in range(size_y)]
    visited_positions_board[y][x] = 1

    while True:
        next_x, next_y = get_next_position(x, y, dir_index)
        visited_positions_board[y][x] += 1

        if visited_positions_board[y][x] > 4:
            isLoop = True
            break

        if track_pos:
            if not [x, y] in visited_positions:
                visited_positions.append([x, y])

        if not inBoard(next_x, next_y, size_x, size_y):
            break

        if board[next_y][next_x] == 2:
            dir_index = get_next_direction_index(dir_index)
            continue

        x = next_x
        y = next_y

    visited_positions_board = [[1 for num in row if num > 0]
                               for row in visited_positions_board]
    visited_squares = sum(
        [sum(row) for row in visited_positions_board])

    return_dict = dict(
        visited_squares=visited_squares,
        visited_positions=visited_positions,
        visited_positions_board=visited_positions_board,
        isLoop=isLoop
    )
    return return_dict
# --------------------------------------------------- #


def get_next_position(x, y, dir_index):
    next_x = x + DIRECTIONS[dir_index][0]
    next_y = y + DIRECTIONS[dir_index][1]
    return next_x, next_y
# --------------------------------------------------- #


def place_obstruction(x, y, board):
    new_board = [[char for char in line.copy()] for line in board]
    new_board[y][x] = 2
    return new_board
# --------------------------------------------------- #


def get_next_direction_index(current_dir: int):
    num_dirs = len(DIRECTIONS)
    if current_dir+1 == num_dirs:
        return 0
    return current_dir + 1
# --------------------------------------------------- #


def inBoard(x: int, y: int, size_x, size_y) -> bool:
    if x < 0 or y < 0:
        return False
    if x >= size_x or y >= size_y:
        return False
    return True
# --------------------------------------------------- #


if __name__ == "__main__":
    from timeit import timeit
    # print(timeit(main, number=100))
    main()
    pass
