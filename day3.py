# from typing import List
import re
from dataclasses import dataclass


@dataclass
class PartNumber:
    number: int
    line: int
    start: int
    end: int


def read_input_file(file_name: str) -> tuple[list, list, list]:
    with open(file_name) as f:
        content = f.read().splitlines()

    # for line in content:
    # items = line.split(":")
    # print(re.findall(r'(\d+)', line))
    # print(re.findall(r'[^0-9\.]', line))

    engine_line = 0
    part_numbers = []
    part_symbols = []
    part2_symbols = []
    for line in content:
        for match in re.finditer(r'(\d+)', line):
            part_numbers.append([int(match.group()), engine_line, match.start(), match.end()])
        for match in re.finditer(r'[^0-9\.]', line):
            part_symbols.append([engine_line, match.start()])
            part2_symbols.append([engine_line, match.start(), match.group()])
        engine_line += 1

    return part_numbers, part_symbols, part2_symbols


def calc_neighbours(pn):
    neighbour_list = []
    nb = [pn[1], pn[2] - 1]
    neighbour_list.append(nb)
    nb = [pn[1], pn[3]]
    neighbour_list.append(nb)
    for j in range(pn[2] - 1, pn[3] + 1):
        nb = [pn[1] - 1, j]
        neighbour_list.append(nb)
        nb = [pn[1] + 1, j]
        neighbour_list.append(nb)

    return neighbour_list


def compute_part_one(file_name: str) -> int:
    part_numbers, part_symbols, dummy = read_input_file(file_name)
    sum_of_part_numbers = 0
    for part_number in part_numbers:
        neighbours = calc_neighbours(part_number)
        has_adjacent_number = False
        for neighbour in neighbours:
            if neighbour in part_symbols:
                has_adjacent_number = True
            if has_adjacent_number:
                sum_of_part_numbers += part_number[0]
                break

    return sum_of_part_numbers


def compute_part_two(file_name: str) -> int:
    part_numbers, dummy, part_symbols = read_input_file(file_name)
    sum_of_gear_counts = 0
    for part_symbol in part_symbols:
        if part_symbol[2] != "*":
            continue
        gear_count = 0
        gear_list = []
        for part_number in part_numbers:
            neighbours = calc_neighbours(part_number)
            if [part_symbol[0], part_symbol[1]] in neighbours:
                gear_count += 1
                gear_list.append(part_number)
                if gear_count > 2:
                    break
        if gear_count == 2:
            sum_of_gear_counts += gear_list[0][0] * gear_list[1][0]

    return sum_of_gear_counts


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input3.txt')}")
    print(f"Part II: {compute_part_two('input/input3.txt')}")
