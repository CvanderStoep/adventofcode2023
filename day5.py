import re
import sys
from dataclasses import dataclass


def read_input_file(file_name: str) -> tuple[list, list, list]:
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


def convert(seed: int, local_map: Map) -> int:
    destination = seed
    for category in local_map.categories:
        if category.source <= seed <= category.source + category.range:
            destination = category.destination + seed - category.source
            break
    return destination


def compute_part_one(file_name: str) -> int:
    seeds, almanac = read_input_file(file_name)
    minimum_location = sys.maxsize
    for seed in seeds:
        seed_map = seed
        for m in almanac:
            seed_map = convert(seed_map, m)
        minimum_location = min(minimum_location, seed_map)
    return minimum_location


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input5.txt')}")
