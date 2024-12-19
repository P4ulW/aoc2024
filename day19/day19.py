from rich import print
from rich.progress import track
from functools import cache
from collections import defaultdict

makeable: dict[str, int] = dict()


def max_towel_len(towels):
    lens = [len(towel) for towel in towels]
    return max(lens)


def main():
    filename = './inputs.txt'
    with open(filename) as file:
        input = [line.strip() for line in file.readlines()]
    towels = tuple(input[0].replace(',', '').split(' '))
    designs = input[slice(2, None)]
    print(towels)
    print(designs)
    num_makeable_designs = 0
    for design in designs:
        makeable = is_design_makeable(design, towels)
        # print(f'd: {design}, m?: {makeable}')
        if makeable:
            num_makeable_designs += 1
    print(f'res part 1: {num_makeable_designs}')

    num_makeable_designs = 0
    for design in designs:
        makeable = is_design_makeable(design, towels)
        # print(f'd: {design}, m?: {makeable}')

        num_makeable_designs += makeable
    print(f'res part 2: {num_makeable_designs}')
    return


# @cache
def is_design_makeable(design, towels):
    if design in makeable:
        return makeable[design]
    if design == '':
        return 1
    ways = 0
    for towel in towels:
        if not design.startswith(towel):
            continue
        subdesign = design.removeprefix(towel)
        m = is_design_makeable(subdesign, towels)
        ways += m
        if subdesign not in makeable:
            makeable[subdesign] = m

    return ways


if __name__ == "__main__":
    main()
