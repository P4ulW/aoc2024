from rich import print
import numpy as np

DIRECTIONS = [
    [0, -1],
    [1, 0],
    [0, 1],
    [-1, 0]
]


def main():
    file = open('./test_inputs.txt', 'r')
    board = [[char for char in line.strip()]
             for line in file.readlines()]
    # [print(line) for line in board]
    x, y, = find_start_position(board)
    print(x, y)
    print(traverse_board(board))
    pass


def find_start_position(board: list[list[str]]) -> list[int]:
    for j, line in enumerate(board):
        for i, char in enumerate(line):
            if not char == '^':
                continue
            return [i, j]
    return []


def traverse_board(board: list[list[str]]) -> int:
    x, y = find_start_position(board)
    dir_index = 0

    size_y = len(board)
    size_x = len(board[0])
    visited_positions_board = [[0,]*size_x]*size_y
    visited_positions_board = np.array(visited_positions_board)
    visited_positions_board[y, x] = 1

    for _ in range(20000):
        # print(visited_positions_board)
        visited_positions_board[y, x] = 1
        next_x = x + DIRECTIONS[dir_index][0]
        next_y = y + DIRECTIONS[dir_index][1]

        # print('x: ', x, 'y: ', y, 'dir: ', dir_index)

        if not inBoard(next_x, next_y, board):
            break
        if board[next_y][next_x] == '#':
            dir_index = get_next_direction_index(dir_index)
            continue

        x = next_x
        y = next_y
    return sum([sum(row) for row in visited_positions_board])


def get_next_direction_index(current_dir: int):
    num_dirs = len(DIRECTIONS)
    if current_dir+1 == num_dirs:
        return 0
    return current_dir + 1


def inBoard(x: int, y: int, board: list[list[str]]) -> bool:
    size_y = len(board)
    size_x = len(board[0])
    if x < 0 or y < 0:
        return False
    if x >= size_x or y >= size_y:
        return False
    return True


if __name__ == "__main__":
    main()
    pass
