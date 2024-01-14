"""
advent of code 2023
https://adventofcode.com/2023
"""
import re
from typing import List


def read_input_file(file_name: str) -> List[int]:
    with open(file_name) as f:
        content = f.read().splitlines()

    # bag = {'r': 0, 'g': 0, 'b': 0}
    all_games = []
    for line in content:
        # for num, col in re.findall(r'(\d+) (\w)', line):
        #     print(f"{num= }, {col= }")
        # print(re.findall(r'(\d+) (\w+)', line))
        items = line.split(":")[1].split(";")
        cube_draw_list = []
        for item in items:
            draws = item.split(",")
            cube_draw_dict = {}
            for draw in draws:
                cube_draw = draw.split(" ")
                cube_draw_dict[cube_draw[2]] = int(cube_draw[1])
            cube_draw_list.append(cube_draw_dict)
        all_games.append(cube_draw_list)
    return all_games


def compute_part_one(file_name: str, maximum_in_bag: dict) -> int:
    all_games = read_input_file(file_name)
    sum_of_valid_IDs = 0
    for ID, game in enumerate(all_games, 1):
        # print(game)
        possible = True
        for draw in game:
            if draw.get("blue", 0) > maximum_in_bag["blue"] or \
                    draw.get("green", 0) > maximum_in_bag["green"] or \
                    draw.get("red", 0) > maximum_in_bag["red"]:
                possible = False
                # print(ID)
                break
        if possible:
            sum_of_valid_IDs += ID
    return sum_of_valid_IDs


def compute_part_two(file_name: str) -> int:
    all_games = read_input_file(file_name)
    sum_of_cube_powers = 0
    for ID, game in enumerate(all_games, 1):
        max_red, max_green, max_blue = 0, 0, 0
        for draw in game:
            if draw.get("blue", 0) > max_blue:
                max_blue = draw.get("blue", 0)
            if draw.get("red", 0) > max_red:
                max_red = draw.get("red", 0)
            if draw.get("green", 0) > max_green:
                max_green = draw.get("green", 0)
        cube_power = max_blue * max_red * max_green
        sum_of_cube_powers += cube_power
        # print(ID, cube_power, sum_of_cube_powers)
    return sum_of_cube_powers


if __name__ == '__main__':
    max_grab = {"red": 12,
                "green": 13,
                "blue": 14}
    print(f"Part I: {compute_part_one('input/input2.txt', max_grab)}")
    print(f"Part II: {compute_part_two('input/input2.txt')}")
