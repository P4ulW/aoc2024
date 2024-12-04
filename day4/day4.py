from rich import print
from collections import deque


def main():
    char_matrix = get_char_matrix_file('./inputs.txt')
    # part1
    res = find_xmas_in_matrix(char_matrix)
    print(f'part1: {res}')

    # part2
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
    return matches


def search_word_in_matrix(matrix, word, x, y):
    size_y = len(matrix)
    size_x = len(matrix[0])
    length = len(word)
    word_reverse = word[::-1]
    matches = 0

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
    main()
