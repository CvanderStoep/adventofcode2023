# https://github.com/jmerle/advent-of-code-2023/blob/master/src/day17/part1.py
import sys


from heapq import *


def compute_part_one(file_name: str) -> int:
    with open(file_name) as f:
        data = f.read().strip()

    grid = tuple(data.split("\n"))

    width = len(grid[0])
    height = len(grid)

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    heap = [(0, 0, 0, 0, 0), (0, 0, 0, 1, 0)]
    seen = set()

    while heap:
        heat, x, y, direction, streak = heappop(heap)

        if (x, y, direction, streak) in seen:
            continue

        seen.add((x, y, direction, streak))
        # print(f'{seen= }')

        if x == width - 1 and y == height - 1:
            print(f'{heat= }')
            return heat

        dx, dy = directions[direction]
        x += dx
        y += dy

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        heat += int(grid[y][x])

        if streak < 2:
            heappush(heap, (heat, x, y, direction, streak + 1))

        heappush(heap, (heat, x, y, (direction + 1) % 4, 0))
        heappush(heap, (heat, x, y, (direction - 1) % 4, 0))


def compute_part_two(file_name: str) -> int:
    with open(file_name) as f:
        data = f.read().strip()

    grid = tuple(data.split("\n"))

    width = len(grid[0])
    height = len(grid)

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    heap = [(0, 0, 0, 0, 0), (0, 0, 0, 1, 0)]
    seen = set()

    while len(heap) > 0:
        heat, x, y, direction, streak = heappop(heap)

        if (x, y, direction, streak) in seen:
            continue

        seen.add((x, y, direction, streak))

        if x == width - 1 and y == height - 1:
            if streak > 3:
                print(f'{heat= }')
                return heat

        dx, dy = directions[direction]
        x += dx
        y += dy

        if x < 0 or x >= width or y < 0 or y >= height:
            continue

        heat += int(grid[y][x])
        streak += 1

        if streak < 10:
            heappush(heap, (heat, x, y, direction, streak))

        if streak > 3:
            heappush(heap, (heat, x, y, (direction + 1) % 4, 0))
            heappush(heap, (heat, x, y, (direction - 1) % 4, 0))


if __name__ == "__main__":
    print(f"Part I: {compute_part_one('input/input17.txt')}")
    print(f"Part II: {compute_part_two('input/input17.txt')}")
