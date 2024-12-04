from rich import print
from collections import deque


masses: list[list[list[str]]] = [
    [
        ['M', '.', 'M'],
        ['.', 'A', '.'],
        ['S', '.', 'S'],
    ],
    [
        ['M', '.', 'S'],
        ['.', 'A', '.'],
        ['M', '.', 'S'],
    ],
    [
        ['S', '.', 'M'],
        ['.', 'A', '.'],
        ['S', '.', 'M'],
    ],
    [
        ['S', '.', 'S'],
        ['.', 'A', '.'],
        ['M', '.', 'M'],
    ],
]


def main():
    print('Start')
    char_matrix = get_char_matrix_file('./inputs.txt')
    # part1
    res = find_xmas_in_matrix(char_matrix)
    print(f'part1: {res}')

    # part2
    res = find_mas_in_matrix(char_matrix)
    print(f'part2: {res}')
    pass


def current_is_mas(matrix, x, y):
    size_y = len(matrix)
    size_x = len(matrix[0])
    match = 0
    if not matrix[y][x] in ['M', 'S']:
        return match
    if x+3 <= size_x and y+3 <= size_y:
        to_test = [[matrix[y+j][x+i] if not (((i == 0 or i == 2) and j == 1) or (i == 1 and (j == 0 or j == 2))) else '.'
                    for i in range(3)]
                   for j in range(3)]
        if to_test in masses:
            match = 1
        # for line in to_test:
        #     print(line)
        # if match:
        #     print('matches')
        # print('\n')
        pass

    return match


def find_mas_in_matrix(char_matrix: list[list[str]]):
    size_y = len(char_matrix)
    size_x = len(char_matrix[0])
    mask = [[0 for i in range(size_x)] for j in range(size_y)]
    # matches = 0
    matches = [[current_is_mas(char_matrix, x, y)
                for x in range(size_x)]
               for y in range(size_y)]
    matches = sum([num for line in matches for num in line])
    return matches


def get_char_matrix_file(filename: str) -> list[list[str]]:
    file = open(filename, 'r')
    data = [[char
             for char in list(line.strip())]
            for line in file.readlines()]
    return data


def find_xmas_in_matrix(char_matrix: list[list[str]]):
    size_y = len(char_matrix)
    size_x = len(char_matrix[0])
    mask = [[0 for i in range(size_x)] for j in range(size_y)]
    # matches = 0
    matches = [[search_word_in_matrix(char_matrix, 'XMAS', x, y)
                for x in range(size_x)]
               for y in range(size_y)]
    matches = sum([num for line in matches for num in line])
    return matches


def search_word_in_matrix(matrix, word, x, y):
    size_y = len(matrix)
    size_x = len(matrix[0])
    length = len(word)
    word_reverse = word[::-1]
    matches = 0

    if matrix[y][x] not in ["X", 'S']:
        return 0

    # forward
    if x+length <= size_x:
        to_test = ''.join([matrix[y][x+i] for i in range(length)])
        if to_test == word or to_test == word_reverse:
            matches += 1

    # down
    if y+length <= size_y:
        to_test = ''.join([matrix[y+i][x] for i in range(length)])
        if to_test == word or to_test == word_reverse:
            matches += 1

    # diag
    if y+length <= size_y and x+length <= size_x:
        to_test = ''.join([matrix[y+i][x+i] for i in range(length)])
        if to_test == word or to_test == word_reverse:
            matches += 1

    # other diag
    if y+length <= size_y and x-length >= -1:
        to_test = ''.join([matrix[y+i][x-i] for i in range(length)])
        if to_test == word or to_test == word_reverse:
            matches += 1

    return matches


if __name__ == "__main__":
    from timeit import timeit
    print(timeit(main, number=100))
