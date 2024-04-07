import re
from itertools import cycle
from math import lcm


def read_input_file(file_name: str) -> list:
    pattern = "[+-]?\d+"
    oasis = []

    with open(file_name) as f:
        content = f.read().splitlines()

    for line in content:
        numbers = [int(digit) for digit in re.findall(pattern, line)]
        oasis.append(numbers)

    return oasis


def compute_part_one(file_name: str) -> int:
    oasis = read_input_file(file_name)
    sum_extrapolated_values = 0
    for numbers in oasis:
        last_numbers = [numbers[-1]]
        print(f'{numbers= }')
        numbers_copy = numbers
        while len(set(numbers_copy)) > 1:
            new_copy = []
            for i in range(0, len(numbers_copy) - 1):
                difference = numbers_copy[i + 1] - numbers_copy[i]
                new_copy.append(difference)
            numbers_copy = new_copy
            last_numbers.append(new_copy[-1])
            print(f'{numbers_copy= }')
        print(f'{last_numbers= }')
        print(f'{sum(last_numbers)= }')
        sum_extrapolated_values += sum(last_numbers)

    return sum_extrapolated_values


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input9.txt')}")
    # print(f"Part II: {compute_part_two('input/input8.txt')}")
