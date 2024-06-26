import re
import sys
from dataclasses import dataclass

"""
https://adventofcode.com/2023/day/5
"""


def read_input_file(file_name: str) -> tuple:
    with open(file_name) as f:
        content = f.read().split("\n\n")
    almanac = []
    for c in content:
        line = c.splitlines()
        if 'seeds' in line[0]:
            seeds = [int(digit) for digit in re.findall(r'(\d+)', line[0])]
            continue
        categories = line[1:]
        map1 = Map(name=line[0], categories=[])
        for category in categories:
            translation_table = [int(digit) for digit in re.findall(r'(\d+)', category)]
            map1.categories.append(Category(translation_table[0], translation_table[1], translation_table[2]))
        almanac.append(map1)

    return seeds, almanac


@dataclass
class Category:
    destination: int
    source: int
    range: int


@dataclass
class Map:
    name: str
    categories: list[Category]


def intervals(local_map: Map) -> list[int]:
    ranges = []
    for category in local_map.categories:
        ranges.append([category.source, category.source + category.range - 1])
    return ranges


def intersects(seed_range: list, interval: list) -> bool:
    if seed_range[1] < interval[0]:
        return False
    if seed_range[0] > interval[1]:
        return False
    if seed_range[0] > interval[0] and seed_range[1] < interval[1]:
        return False
    return True


def split_range(seed_range: list, interval: list) -> list:
    """"not used yet, future improvement"""
    if seed_range[0] <= interval[1] <= seed_range[1]:
        return [seed_range[0], interval[1]], [interval[1], seed_range[1]]
    else:
        return [seed_range[0], interval[0]], [interval[0], seed_range[1]]


def convert(seed: int, local_map: Map) -> int:
    destination = seed
    for category in local_map.categories:
        if category.source <= seed < category.source + category.range:
            destination = category.destination + seed - category.source
            break
    return destination


def compute_part_one(file_name: str) -> int:
    seeds, almanac = read_input_file(file_name)
    minimum_location = sys.maxsize
    for seed in seeds:
        seed_map = seed
        # print(f'{seed_map= }')
        for m in almanac:
            seed_map = convert(seed_map, m)
            # print(f'{seed= }, {seed_map= }')
        minimum_location = min(minimum_location, seed_map)

    # for seed in range(100):
    #     print(f'{seed= }, {convert(seed, almanac[0])}')
    return minimum_location


def compute_part_two(file_name: str) -> int:
    seeds, almanac = read_input_file(file_name)
    start_seeds = seeds[::2]
    total_seeds = seeds[1::2]
    seeds = []
    print('...running...')
    for index, s in enumerate(start_seeds):
        for j in range(total_seeds[index]):
            seeds.append(s + j)
    print('...running...')
    # DONE takes way too long and runs out of memory; if only it was so easy
    # see compute_part_two_c

    minimum_location = sys.maxsize
    for seed in seeds:
        seed_map = seed
        for m in almanac:
            seed_map = convert(seed_map, m)
        minimum_location = min(minimum_location, seed_map)
    return minimum_location


def compute_part_two_b(file_name: str) -> int:
    """"
    determine the starting ranges [a, b]
    determine transformed ranges [c, d]
        when linear, move to next mapping (c-a == d-b)
        when not linear, split the existing range in two parts [a, m] & [m, b] and repeat
        #DONE I found 137516821 iso 137516820, not been able to find bug so far; bug fixed.
    """
    seeds, almanac = read_input_file(file_name)
    seed_ranges = []

    for i in range(0, len(seeds), 2):
        seed_ranges.append([seeds[i], seeds[i] + seeds[i + 1] - 1])
    # print(f"{seed_ranges= }")

    # for m in almanac:
    #     print(f'{intervals(m)= }')

    minimum_location = sys.maxsize
    while seed_ranges:
        # print(f"{seed_ranges= }")
        seed_range = seed_ranges.pop()
        seed0_org = seed0 = seed_range[0]
        seed1_org = seed1 = seed_range[1]
        seedm = (seed0 + seed1) // 2
        break_found = False
        for m in almanac:
            seed0_prev, seed1_prev, seedm_prev = seed0, seed1, seedm
            seed0 = convert(seed0, m)
            seed1 = convert(seed1, m)
            seedm = convert(seedm, m)

            if not ((seed0_prev - seed0) == (seed1_prev - seed1) == (
                    seedm_prev - seedm)):  # split the original range in 2 parts
                mid = (seed0_org + seed1_org) // 2
                seed_ranges.append([seed0_org, mid])
                seed_ranges.append([mid + 1, seed1_org])
                break_found = True
                break
        if not break_found:
            minimum_location = min(minimum_location, seed0, seed1)
    return minimum_location


def compute_part_two_c(file_name: str) -> int:
    seeds, almanac = read_input_file(file_name)
    seed_ranges = []

    for i in range(0, len(seeds), 2):
        seed_ranges.append([seeds[i], seeds[i] + seeds[i + 1] - 1])

    minimum_location = sys.maxsize
    while seed_ranges:
        # print(f"{seed_ranges= }")
        seed_range = seed_ranges.pop()
        seed0_org = seed0 = seed_range[0]
        seed1_org = seed1 = seed_range[1]
        break_found = False
        # temp_seed_stack = [[seed0, seed1]]
        for m in almanac:
            for interval in intervals(m):
                if intersects([seed0, seed1], interval) and seed0 != seed1:
                    mid = (seed0_org + seed1_org) // 2
                    seed_ranges.append([seed0_org, mid])
                    seed_ranges.append([mid + 1, seed1_org])
                    break_found = True
                    break  # break out of interval loop
            if break_found:
                break  # also break out of almanac loop
            seed0 = convert(seed0, m)
            seed1 = convert(seed1, m)
            # temp_seed_stack.append([seed0, seed1])
        if not break_found:
            # if seed0 < minimum_location or seed1 < minimum_location:
            #     seed_stack = temp_seed_stack.copy()
            minimum_location = min(minimum_location, seed0, seed1)
    pass
    return minimum_location


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input5.txt')}")
    # print(f"Part II: {compute_part_two('input/input5.txt')}")  # only works for small test-sets; brute force
    print(f"Part IIb: {compute_part_two_b('input/input5.txt')}")
    print(f"Part IIc: {compute_part_two_c('input/input5.txt')}")
