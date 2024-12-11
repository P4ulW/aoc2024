from rich.progress import track
from functools import cache

STONE_SPLITS_LOOKUP = {}


def main():
    file = open('./test_inputs.txt')
    stones = [int(num) for num in file.readline().strip().split(' ')]
    # print(stones)
    blinks = 25
    for i in track(range(blinks)):
        stones = [stone for s in stones for stone in blink_stone(s)]
    print('part 1:', len(stones))

    file = open('./test_inputs.txt')
    stones = [int(num) for num in file.readline().strip().split(' ')]
    blinks = 75
    res = 0
    for stone in stones:
        res += split_count(stone, blinks)

    print('part 2:', res)
    return


def blink_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1, ]

    lenght_stone = len(str(stone))
    if not lenght_stone % 2:
        stone_left = int(str(stone)[slice(0, lenght_stone//2)])
        stone_right = int(str(stone)[slice(lenght_stone//2, None)])
        return [stone_left, stone_right]

    else:
        return [stone*2024, ]


@cache
def split_count(stone, blinks) -> int:
    if blinks == 0:
        return 1

    num = [split_count(stone, blinks-1) for stone in blink_stone(stone)]
    return sum(num)


if __name__ == "__main__":
    main()
    for key, value in STONE_SPLITS_LOOKUP.items():
        print(key, value)
    pass
