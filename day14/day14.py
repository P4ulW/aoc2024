# from rich import print
from re import findall
from PIL import Image
import numpy as np


def robot_from_raw_input(input: str) -> dict[str, tuple[int, ...]]:
    robot = {}
    start_pos = tuple([int(pos) for pos in
                       (findall(r'p=\d+,\d+', input)[0]
                        .strip('p=')
                        .split(','))
                       ])
    velocity = tuple([int(pos) for pos in
                      (findall(r'v=-?\d+,-?\d+', input)[0]
                       .strip('v=')
                       .split(','))
                      ])
    robot['start_pos'] = start_pos
    robot['velocity'] = velocity
    return robot


def robot_position_after_time(
        robot: dict[str, tuple[int, ...]],
        time: int,
        max_x: int,
        max_y: int) -> tuple[int, int]:
    x0, y0 = robot['start_pos']
    vx, vy = robot['velocity']
    x = x0 + time*vx
    y = y0 + time*vy
    x %= max_x
    y %= max_y

    return x, y


def calc_result(
        end_positions: list[tuple[int, int]],
        room_size: tuple[int, int]
):
    rx, ry = room_size
    robots_in_quad = [0, 0, 0, 0]
    for pos in end_positions:
        x, y = pos
        if x < rx // 2:
            if y < ry // 2:
                robots_in_quad[0] += 1
            elif y > ry // 2:
                robots_in_quad[2] += 1

        if x > rx // 2:
            if y < ry // 2:
                robots_in_quad[1] += 1
            elif y > ry // 2:
                robots_in_quad[3] += 1

    result = 1
    for num in robots_in_quad:
        result *= num
    return result


def main():
    filename = './inputs.txt'
    file = open(filename, 'r')
    raw_inputs = [line.strip() for line in file.readlines()]
    if 'test' in filename:
        room_size = (11, 7)
    else:
        room_size = (101, 103)
    print(room_size)

    robots = [robot_from_raw_input(input) for input in raw_inputs]
    # print(robots)
    end_positions = [robot_position_after_time(robot, 100, *room_size)
                     for robot in robots]
    # print(end_positions)
    room = [[0
            for _ in range(room_size[0])]
            for _ in range(room_size[1])
            ]
    # for pos in end_positions:
    #     room[pos[1]][pos[0]] += 1
    # for row in room:
    #     print(row)

    print('res part 1:', calc_result(end_positions, room_size))

    for i in range(0, 10000):
        end_positions = [robot_position_after_time(robot, i, *room_size)
                         for robot in robots]

        room = [[0
                for _ in range(room_size[0])]
                for _ in range(room_size[1])
                ]
        for pos in end_positions:
            room[pos[1]][pos[0]] = 1
        room = np.array(room, dtype=np.uint8)
        room = (room * 255).astype(np.uint8)
        img = Image.fromarray(room)
        img.save(f'img_{str(i).zfill(5)}.png')
        # for row in room:
        #     out = ''
        #     for num in row:
        #         if num == 0:
        #             out += ' '
        #         else:
        #             out += str(num)
        #
        #     out += '\n'
        #     file.write(out)
    return


if __name__ == "__main__":
    main()
    pass
