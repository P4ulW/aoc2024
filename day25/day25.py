from rich import print
from itertools import product

Lock = list[list[str]]
Key = list[list[str]]


def get_lock_colheight(lock: Lock, col: int) -> int:
    column_data = [lock[i][col] for i in range(len(lock))]
    return sum(1 for c in column_data if c == '#')


def get_key_colheigth(key: Key, col: int) -> int:
    column_data = [key[i][col] for i in range(len(key))]
    return sum(1 for c in column_data if c == '#')


def key_fits_lock(key: Key, lock: Lock) -> bool:
    height = len(key)
    length = len(key[0])
    if height != len(lock):
        raise ValueError

    if length != len(lock[0]):
        raise ValueError

    for col in range(length):
        h_lock = get_lock_colheight(lock, col)
        h_key = get_key_colheigth(key, col)
        if not (h_lock + h_key <= height):
            return False

    return True


def main():
    filename = './in.txt'
    with open(filename) as file:
        data = file.read().strip().split('\n\n')
        data = [line.split('\n') for line in data]
    keys = []
    locks = []
    for item in data:
        if item[0][0] == '.':
            keys.append([[char for char in line] for line in item])

        if item[0][0] == '#':
            locks.append([[char for char in line] for line in item])

    res = [1 for key, lock in
           product(keys, locks)
           if key_fits_lock(key, lock)]
    print('res part 1:', sum(res))

    return


if __name__ == "__main__":
    main()
    pass
