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
    sum_extrapolated_values = 0  # by adding the last values of all intermediate sequence, the prediction is found
    for numbers in oasis:
        sum_extrapolated_values += numbers[-1]
        while len(set(numbers)) > 1:  # quick way to check whether a list contains only 1 number: convert to a set
            temp_copy_numbers = []
            for i in range(0, len(numbers) - 1):
                difference = numbers[i + 1] - numbers[i]
                temp_copy_numbers.append(difference)
            numbers = temp_copy_numbers
            sum_extrapolated_values += temp_copy_numbers[-1]

    return sum_extrapolated_values


def compute_part_two(file_name: str) -> int:
    oasis = read_input_file(file_name)
    sum_extrapolated_values = 0
    # by adding the (-1) ^depth * first values of all intermediate sequence, the prediction is found
    # a0 = a1 - b1 + c1 - d1 ...  (a is original series, b is first differences, c is second ...
    for numbers in oasis:
        extrapolated_value = numbers[0]
        depth = 0
        while len(set(numbers)) > 1:  # quick way to check whether a list contains only 1 number: convert to a set
            temp_copy_numbers = []
            for i in range(0, len(numbers) - 1):
                difference = numbers[i + 1] - numbers[i]
                temp_copy_numbers.append(difference)
            numbers = temp_copy_numbers
            depth += 1
            extrapolated_value = extrapolated_value + (-1) ** depth * temp_copy_numbers[0]
        sum_extrapolated_values += extrapolated_value

    return sum_extrapolated_values


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input9.txt')}")
    print(f"Part II: {compute_part_two('input/input9.txt')}")
