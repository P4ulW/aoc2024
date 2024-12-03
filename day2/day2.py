from rich import print
import timeit


def main():
    with open('./inputs.txt', 'r') as file:
        score_part_1 = 0
        score_part_2 = 0
        for report in file.readlines():
            report = report.strip('\n').split(' ')
            report = [int(num) for num in report]
            # print(report)
            # valid = is_report_valid(report)
            # print(valid)
            # if valid:
            #     score_part_1 += 1

            valid = is_report_valid_damped(report)
            # print(valid)
            if valid:
                score_part_2 += 1
    # print(f'part 1: {score_part_1}')
    # print(f'part 2: {score_part_2}')
    return


def is_report_valid(report: list[int]):
    # report = [report[i] - report[i+1] for i in range(len(report)-1)]
    first = report[1] - report[0]
    if first == 0:
        return False

    ascending = ((first / abs(first))+1) / 2
    # print(ascending)
    for i in range(len(report)-1):
        current = report[i+1] - report[i]

        if current == 0:
            return False
        if abs(current) > 3:
            return False
        if ascending and current < 1:
            return False
        if not ascending and current > -1:
            return False

    return True


def is_report_valid_damped(report: list[int]):
    if is_report_valid(report):
        return True
    for i in range(len(report)):
        skipped_report = report.copy()
        skipped_report.pop(i)
        if is_report_valid(skipped_report):
            return True

    return False


if __name__ == "__main__":
    # time = timeit.timeit(main, number=1000)
    # print(time)
    reports = [[int(x)
                for x in report.split()]
               for report in open('./test_inputs.txt')]
    for report in reports:
        print(report)

    # main()
    pass
