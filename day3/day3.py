from re import findall


def main():
    file = open('./inputs.txt', 'r')
    lines = file.readlines()
    # instructions = []
    # prods = []
    # for line in lines:
    #     valid = findall(r'mul\(\d+,\d+\)', line)
    #     # print(valid)
    #     for instruction in valid:
    #         instructions.append(instruction)
    # for instruction in instructions:
    #     prod = process_instruction(instruction)
    #     prods.append(prod)
    # print(f'result part 1: {sum(prods)}')

    long_line = ''
    for line in lines:
        long_line += line
    print(long_line)
    instructions = findall(
        r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)',
        long_line)
    # print(instructions)
    res = process_instructions_part2(instructions)
    print(res)
    pass


def process_instruction(instruction: str):
    instruction = instruction.strip('mul').strip('(').strip(')').split(',')
    prod = int(instruction[0]) * int(instruction[1])
    return prod


def process_instructions_part2(instructions: list[str]):
    enable = True
    result = 0
    for instruction in instructions:
        print(instruction)
        if instruction == 'do()':
            enable = True
            continue
        if instruction == 'don\'t()':
            enable = False
            continue
        if enable:
            prod = process_instruction(instruction)
            result += prod

    return result


if __name__ == "__main__":
    main()
    pass
