from os import walk
from posixpath import expanduser
from rich import print
from operator import add, mul
import itertools as it
from multiprocessing import Pool
from functools import partial


def concat(lhs: int, rhs: int) -> int:
    lhs = str(lhs)
    rhs = str(rhs)
    res = int(lhs+rhs)
    return res


def load_inputs(filename):
    file = open(filename, 'r')
    data = [line.strip().split(': ') for line in file.readlines()]
    for i, entry in enumerate(data):
        data[i][0] = int(entry[0])
        data[i][1] = [int(num) for num in entry[1].split(' ')]
    return data


def main():
    data = load_inputs('./inputs.txt')
    # print(data)

    # part 1
    operators = [add, mul]
    res1 = 0
    for equation in data:
        res, expr = equation
        # print(f'{res}={expr}')
        number_ops = len(expr) - 1
        op_sets = all_operator_variations(number_ops, operators)
        all_results = [evaluate_expression(expr, ops)for ops in op_sets]
        if res in all_results:
            res1 += res
    print(f'res1: {res1}')

    # part 2
    operators = [add, mul, concat]
    res2 = 0
    _find_equation_res = partial(equation_result, operators=operators)
    pool = Pool(16)
    results = pool.map(_find_equation_res, data)
    pool.close()
    pool.join()
    res2 = sum(results)
    # for equation in data:
    #     res, expr = equation
    #     print(f'{res}={expr}')
    #     number_ops = len(expr) - 1
    #     op_sets = all_operator_variations(number_ops, operators)
    #     all_results = [evaluate_expression(expr, ops)for ops in op_sets]
    #     if res in all_results:
    #         res2 += res
    print(f'res2: {res2}')

    return


def equation_result(equation, operators):
    res, expr = equation
    print(f'{res}={expr}')
    number_ops = len(expr) - 1
    op_sets = all_operator_variations(number_ops, operators)
    all_results = [evaluate_expression(expr, ops)for ops in op_sets]
    if res in all_results:
        return res
    else:
        return 0


def all_operator_variations(number_ops, operators):
    return it.product(operators, repeat=number_ops)


def evaluate_expression(expr, ops):
    lhs = expr[0]
    for i in range(len(ops)):
        rhs = expr[i+1]
        lhs = ops[i](lhs, rhs)

    return lhs


if __name__ == "__main__":
    main()
    pass
