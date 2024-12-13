from decimal import DivisionByZero
import itertools
from math import gcd
from re import findall
from rich import print

costs = {
    'A': 3,
    'B': 1
}

def game_to_instructions(game: list[str], corrected=False) -> dict:
    instructions = {}
    for line in game:
        if 'Button A' in line:
            x = int(findall(r'X\+\d+', line)[0].replace('X+', ''))
            y = int(findall(r'Y\+\d+', line)[0].replace('Y+', ''))
            instructions['A'] = (x, y)

        elif 'Button B' in line:
            x = int(findall(r'X\+\d+', line)[0].replace('X+', ''))
            y = int(findall(r'Y\+\d+', line)[0].replace('Y+', ''))
            instructions['B'] = (x, y)

        elif 'Prize' in line:
            x = int(findall(r'X=\d+', line)[0].replace('X=', ''))
            y = int(findall(r'Y=\d+', line)[0].replace('Y=', ''))
            instructions['Prize'] = (x, y)
            if corrected:
                instructions['Prize'] = (x+10000000000000, y+10000000000000)

    return instructions


def brute_force_cheapest_instruction(
    instructions: dict
):
    lowest_cost = 30000
    reachable = False
    for comb in itertools.combinations_with_replacement(['A', 'B'], r=200):
        x, y = 0, 0
        cost = 0
        for step in comb:
            dx, dy = instructions[step]
            x, y = x+dx, y+dy
            cost += costs[step]

            if x > instructions['Prize'][0] or y > instructions['Prize'][1]:
                continue
            if (x, y) == instructions['Prize']:
                reachable = True
                lowest_cost = min(lowest_cost, cost)

    return reachable, lowest_cost


def calc_cost(
        instructions: dict
):
    possible = False
    cost = 0
    Tx, Ty = instructions['Prize']
    Ax, Ay = instructions['A']
    Bx, By = instructions['B']

    n = (-Bx*Ty + By*Tx) / (Ax*By - Ay*Bx)
    m = (+Ax*Ty - Ay*Tx) / (Ax*By - Ay*Bx)
    if n == int(n) and m == int(m):
        return True, n*costs['A']+m*costs['B']

    return possible, cost

def main():
    file = open('./inputs.txt')
    data = [line.strip() for line in file.readlines()]
    print(data)
    games = []
    game = []
    for line in data:
        if line == '':
            games.append(game)
            game = []
        else:
            game.append(line)
    games.append(game)
    print(games)

    # part 1 
    res = 0
    for game in games:
        instr = game_to_instructions(game)
        # print(instr)
        pos, cost = calc_cost(instr)
        # print(pos, cost)
        if pos:
            res += cost

    print(f'part 1: {res}')

    # part 2 
    res = 0
    for game in games:
        instr = game_to_instructions(game, True)
        # print(instr)
        pos, cost = calc_cost(instr)
        # print(pos, cost)
        if pos:
            res += cost
    print(f'part 1: {res}')

    return

    

if __name__ == "__main__":
    main()
    pass
