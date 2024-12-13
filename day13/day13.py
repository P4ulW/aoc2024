import itertools
from re import findall
# from rich import print

costs = {
    'A': 3,
    'B': 1
}
def main():
    file = open('./test_inputs.txt')
    data = [line.strip() for line in file.readlines()]
    games = []
    game = []
    for line in data:
        if line == '':
            games.append(game)
            game = []
        else:
            game.append(line)
    print(games)

    for game in games:
        instr = game_to_instructions(game)
        print(instr)
        pos, cost = brute_force_cheapest_instruction(instr)
        print(pos, cost)

    return

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


def game_to_instructions(game: list[str]):
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
    return instructions

if __name__ == "__main__":
    main()
    pass
