from rich import print
from collections import deque


def main():
    char_matrix = get_char_matrix_file('./test_inputs.txt')
    for line in char_matrix:
        print(line)
    res = find_xmas_in_matrix(char_matrix)
    print(res)
    pass


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
    matches = 0
    for y in range(size_y):
        for x in range(size_x):
            matched = search_word_in_matrix(
                char_matrix, 'XMAS', x, y)
            mask[y][x] = matched
            matches += matched
        print('\n')
    print(mask)
    return matches


def search_word_in_matrix(matrix, word, x, y):
    size_y = len(matrix)
    size_x = len(matrix[0])
    length = len(word)
    # word = [char for char in word]
    word_reverse = word[::-1]
    matches = 0

    # forward
    if x+length <= size_x:
        to_test = ''.join([matrix[y][i] for i in range(x, x+length)])
        print(f'fore: \t{to_test}')
        if to_test == word or to_test == word_reverse:
            matches += 1

    # # backwards
    # # minus one because range(0, length) = [0 ... length - 1]
    # print(x-length)
    # if x-length >= -1:
    #     to_test = ''.join([matrix[y][x-i] for i in range(length)])
    #     print(f'back: \t{to_test}')
    #     if to_test == word or to_test == word_reverse:
    #         matches += 1

    # down
    if y+length <= size_y:
        to_test = ''.join([matrix[i][x] for i in range(y, y+length)])
        print(f'down: \t{to_test}')
        if to_test == word or to_test == word_reverse:
            matches += 1

    # # up
    # if y-length >= -1:
    #     to_test = ''.join([matrix[y-i][x] for i in range(length)])
    #     print(f'up: \t{to_test}')
    #     if to_test == word or to_test == word_reverse:
    #         matches += 1

    # diagonal for
    if y+length <= size_y and x+length <= size_x:
        to_test = ''.join([matrix[y+i][x+i] for i in range(length)])
        print(f'diag: \t\t{to_test}')
        if to_test == word or to_test == word_reverse:
            matches += 1

    # # diagonal back
    # if y-length >= -1 and x-length >= -1:
    #     to_test = ''.join([matrix[y-i][x-i] for i in range(length)])
    #     print(f'diag: \t\t{to_test}')
    #     if to_test == word or to_test == word_reverse:
    #         matches += 1

    # other diag
    if y+length < length and x-length >= -1:
        to_test = ''.join([matrix[y+i][x-i] for i in range(length)])
        print(f'diag2: \t\t{to_test}')
        if to_test == word or to_test == word_reverse:
            matches += 1

    return matches


if __name__ == "__main__":
    main()
