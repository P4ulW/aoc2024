from collections import defaultdict


def main():
    input = open('./inputs.txt', 'r')
    lines = input.readlines()
    lines = [line.replace('\n', '').split('   ')
             for line in lines]
    list1, list2 = list(zip(*lines))
    list1 = sorted(list1)
    list2 = sorted(list2)
    print(list1, list2)
    distances = distance_elements(list1, list2)
    print(distances)
    print(f'result part 1: {sum(distances)}')

    occurence_dict_list2 = defaultdict(int)
    for entry in list2:
        occurence_dict_list2[entry] += 1

    print(occurence_dict_list2)
    for num in list1:
        print(int(num), occurence_dict_list2[num])
    new_score = [occurence_dict_list2[num]*int(num)
                 for num in list1]
    print(f'result part2: {sum(new_score)}')

    return


def distance_elements(list1: list[str], list2: list[str]) -> list[int]:
    assert len(list1) == len(list2)
    distances = [abs(int(list1[i])-int(list2[i])) for i in range(len(list1))]
    return distances


if __name__ == "__main__":
    main()
    pass
