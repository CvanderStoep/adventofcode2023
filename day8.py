import re
from itertools import cycle
from math import lcm


def read_input_file(file_name: str) -> (str, list):
    pattern = "[A-Z0-9]{3}"
    network = dict()

    with open(file_name) as f:
        content = f.read().splitlines()

    for i, line in enumerate(content):
        if i == 0:
            directions = line
        if i > 1:
            node, left, right = re.findall(pattern, line)
            network[node] = [left, right]

    return directions, network


def starting_positions(network: dict) -> list:
    sp = []  # list of starting positions
    for n in network:
        if n[-1] == "A":
            sp.append(n)
    return sp


def end_positions(network: dict) -> list:
    ep = []  # list of end positions
    for n in network:
        if n[-1] == "Z":
            ep.append(n)
    return ep


def compute_part_one(file_name: str) -> int:
    directions, network = read_input_file(file_name)

    position = "AAA"
    number_of_steps = 0
    for move in cycle(directions):
        number_of_steps += 1
        if move == "L":
            position = network[position][0]
        else:
            position = network[position][1]
        if position == "ZZZ":
            break

    return number_of_steps


def compute_part_two(file_name: str) -> int:
    directions, network = read_input_file(file_name)

    starting_position_list = starting_positions(network)
    end_position_list = end_positions(network)
    individual_cycles = []  # list of individual cycle length of each starting position

    number_of_steps = 0
    for move in cycle(directions):
        # end_position_check_list = []
        number_of_steps += 1
        for i, position in enumerate(starting_position_list):
            if move == "L":
                position = network[position][0]
            else:
                position = network[position][1]
            if position in end_position_list:
                # end_position_check_list.append(True)
                individual_cycles.append(number_of_steps)
            starting_position_list[i] = position  # update starting position list with new element

        if len(individual_cycles) == len(starting_position_list):
            break

        # this is the alternative, but takes way too long ...
        # if all(end_position_check_list) and len(end_position_check_list) == len(starting_position_list):
        #     break

        # the answer is the lowest common denominator of the individual cycle lengths.
    print(f'{individual_cycles= }')
    return lcm(*individual_cycles)


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input8.txt')}")
    print(f"Part II: {compute_part_two('input/input8.txt')}")
