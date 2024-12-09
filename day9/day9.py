# from rich import print
from rich.progress import track
from functools import lru_cache
from numba import njit


def decompress_file(file: list[int]):
    disk = []
    fileID = 0
    isFile = True
    for num in file:
        if isFile:
            [disk.append(fileID) for _ in range(num)]
            fileID += 1

        else:
            [disk.append(-1) for _ in range(num)]
        isFile = not isFile

    return disk


@njit
def compress_disk(disk: list[int]):
    start = 0
    end = len(disk)-1
    while not start >= end:
        if disk[end] == -1:
            end -= 1
            continue
        if disk[start] == -1:
            disk[start] = disk[end]
            disk[end] = -1
            start += 1
            end -= 1
        else:
            start += 1

    return disk


@njit
def compress_disk_blocks(disk: list[int]):
    start = 0
    end = len(disk)-1
    block_id = disk[end]
    while disk[end] == -1:
        disk[end-1]
        end -= 1

    while not start >= end:
        if disk[end] == -1:
            end -= 1
            continue
        block_id = disk[end]

        if disk[start] == block_id:
            # print(f'reached block {block_id}, skipping')
            start = 0
            end -= get_current_blocksize(end, disk)
            continue

        if not disk[start] == -1:
            start += 1
            continue

        hole_size = get_current_holezise(start, disk)
        blocksize = get_current_blocksize(end, disk)
        # print(f'hole at {start} with size {hole_size}')
        if not blocksize <= hole_size:
            start += hole_size
            continue

        # move block
        # print(f'copy block {block_id} to {start}')
        for i in range(blocksize):
            disk[start] = disk[end]
            disk[end] = -1
            start += 1
            end -= 1
        start = 0
        # print_disk(disk)

    return disk


def print_disk(disk):
    stringified = map(lambda x: '.' if x == -1 else str(x), disk)
    out = ''
    for char in stringified:
        out += char
    print(out)


@njit
def get_current_blocksize(idx, disk):
    block_size = 0
    block_id = disk[idx]
    while disk[idx] == block_id:
        block_size += 1
        idx -= 1

    return block_size


@njit
def get_current_holezise(idx, disk):
    hole_size = 0
    while disk[idx] == -1:
        hole_size += 1
        idx += 1
    return hole_size


def calc_disk_checksum(disk: list[int]):
    disk = map(lambda x: 0 if x == -1 else x, disk)
    checksum = sum([x*num for x, num in enumerate(disk)])
    return checksum


def main():
    with open('./inputs.txt', 'r') as file:
        data = file.readline().strip()
    data = list(map(int, data))
    disk = decompress_file(data)
    # print_disk(disk)
    disk = compress_disk(disk)
    # print_disk(disk)
    print('part 1: ', calc_disk_checksum(disk))

    disk = decompress_file(data)
    print('starting:')
    # print_disk(disk)
    disk = compress_disk_blocks(disk)
    # print_disk(disk)
    print('part 2: ', calc_disk_checksum(disk))

    return


if __name__ == "__main__":
    main()
