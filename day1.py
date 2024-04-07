"""
advent of code 2023
https://adventofcode.com/2023
"""
import re
from typing import List


def read_calibration_file(file_name: str) -> List[int]:
    with open(file_name) as f:
        content = f.read().splitlines()

    pattern = "[0-9]"
    number_list = []
    for line in content:
        digits = re.findall(pattern, line)
        number = int(digits[0] + digits[-1])
        number_list.append(number)

    return number_list


def read_and_translate_file(file_name: str) -> List[int]:
    with open(file_name) as f:
        content = f.read().splitlines()
    pattern = "[0-9]"
    digit_in_letters = "(one|two|three|four|five|six|seven|eight|nine)"
    translation_dictionary = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
                              "six": "6", "seven": "7", "eight": "8", "nine": "9"}

    number_list = []
    for line in content:
        # print(line)
        while re.findall(digit_in_letters, line):
            digit_found = re.findall(digit_in_letters, line)
            line = re.sub(digit_found[0], translation_dictionary.get(digit_found[0]), line)
            # print(line)
        # print('--')

        digits = re.findall(pattern, line)
        number = int(digits[0] + digits[-1])
        # print(number)
        number_list.append(number)

    return number_list


def read_and_translate_file2(file_name: str) -> List[int]:
    with open(file_name) as f:
        content = f.read().splitlines()
    pattern = "[0-9]"

    number_list = []
    for line in content:
        # print(line)
        line = line.replace("one", "one1one").replace("two", "two2two").replace("three", "three3three")\
            .replace("four", "four4four").replace("five", "five5five").replace("six", "six6six")\
            .replace("seven", "seven7seven").replace("eight", "eight8eight").replace("nine", "nine9nine")

        # print(line)
        digits = re.findall(pattern, line)
        number = int(digits[0] + digits[-1])
        # print(number)
        number_list.append(number)

    return number_list


def compute_part_one(file_name: str) -> int:
    calibration_values = read_calibration_file(file_name)
    return sum(calibration_values)


def compute_part_two(file_name: str) -> int:
    calibration_values = read_and_translate_file(file_name)
    return sum(calibration_values)


def compute_part_twob(file_name: str) -> int:
    calibration_values = read_and_translate_file2(file_name)
    return sum(calibration_values)


if __name__ == '__main__':
    # print(f"Part I: {compute_part_one('input/input1.txt')}")
    print(f"Part II: {compute_part_two('input/input1.txt')}")
    print(f"Part II: {compute_part_twob('input/input1.txt')}")
