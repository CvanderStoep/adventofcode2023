import re
"""see also day12 (aoc2022) and day24"""
def surrounding(input, x, y):
    vals = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [(x_i, y_i) for (x_i, y_i) in vals if 0 <= x_i < len(input) and 0 <= y_i < len(input[x])]


def read_input_file(file_name: str) -> list:
    pattern = r"[+-]?\d+"
    grid = []

    with open(file_name) as f:
        content = f.read().splitlines()

    for line in content:
        grid.append(list(line))

    return grid


def compute_part_one(file_name: str) -> int:
    grid = read_input_file(file_name)

    for line in grid:
        print(line)

    return 0


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input10.txt')}")
    # print(f"Part II: {compute_part_two('input/input10.txt')}")
