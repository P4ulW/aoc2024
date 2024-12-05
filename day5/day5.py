from rich import print
from collections import defaultdict


def main():
    file = open('inputs.txt', 'r')
    lines = [line.strip() for line in file.readlines()]
    ordering = [line.split('|') for line in lines if '|' in line]
    updates = [line for line in lines if ',' in line]

    rules = defaultdict(list)
    for pair in ordering:
        rules[int(pair[0])].append(int(pair[1]))

    updates = [[int(num) for num in line.split(',')] for line in updates]

    valid_updates = [update
                     for update in updates
                     if is_ordered(update, rules)[0]]
    res = sum([update[len(update)//2]
               for update in valid_updates])
    print(f'part 1: {res}')

    invalid_updates = [update
                       for update in updates
                       if not is_ordered(update, rules)[0]]
    reordered_updates = [reorder_update(update, rules)
                         for update in invalid_updates]
    res = sum([update[len(update)//2]
               for update in reordered_updates])
    print(f'part 2: {res}')

    return


def is_ordered(update: list[int],
               rules: defaultdict[int, list]) -> tuple[bool, list]:
    prev_nums: list[int] = []
    for num in update:
        rule_num = rules[num]
        violations = [int(prev_num in rule_num) for prev_num in prev_nums]
        prev_nums.append(num)
        if not sum(violations) == 0:
            return False, violations
    return True, []


def reorder_update(update: list[int],
                   rules: defaultdict[int, list],
                   iteration: int = 0) -> list:
    valid, violations = is_ordered(update, rules)
    if valid:
        return update
    violation_ind = len(violations)
    swap_index = violations.index(1)
    update_new = update.copy()
    update_new[violation_ind] = update[swap_index]
    update_new[swap_index] = update[violation_ind]
    return reorder_update(update_new, rules, iteration + 1)


if __name__ == "__main__":
    from timeit import timeit
    main()

    # print(timeit(main, number=1000))
    pass
