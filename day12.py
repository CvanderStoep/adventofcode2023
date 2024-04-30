from itertools import product, combinations, permutations
import re
from functools import lru_cache


def read_input_file(file_name: str) -> list:
    # pattern = r"[+-]?\d+"
    pattern = "[0-9]+"
    spring_condition = "[?.#]"
    condition_records = []

    with open(file_name) as f:
        content = f.read().splitlines()

    for line in content:
        springs = re.findall(spring_condition, line)
        digits = [int(digit) for digit in re.findall(pattern, line)]
        condition_records.append([springs, digits])

    return condition_records


# @lru_cache
def is_valid_condition_record(condition_record) -> bool:
    """"
    [#....######..#####.] [1,6,5] -> True
    """

    spring_row = ''.join(condition_record[0])
    spring_sizes_input = condition_record[1]
    # return is_valid(spring_row, tuple(spring_sizes_input))

    pattern = "[#]+"
    damaged = re.finditer(pattern, spring_row)
    spring_sizes_calculated = []
    for d in damaged:
        spring_sizes_calculated.append(d.end() - d.start())

    return spring_sizes_input == spring_sizes_calculated


@lru_cache()
def is_valid(spring_row: str, spring_sizes_input: tuple) -> bool:
    pattern = "[#]+"
    damaged = re.finditer(pattern, spring_row)
    spring_sizes_calculated = []
    for d in damaged:
        spring_sizes_calculated.append(d.end() - d.start())

    return spring_sizes_input == spring_sizes_calculated


def compute_part_one(file_name: str) -> int:
    condition_records = read_input_file(file_name)
    number_of_different_arrangements = 0
    for cr in condition_records:
        spring_row = cr[0]
        item = "?"
        number_of_questionmarks = spring_row.count(item)
        number_of_damaged_springs = spring_row.count('#')
        total_number_of_springs = len(spring_row)
        calculated_number_of_damaged_springs = sum(cr[1])
        print(f'{number_of_questionmarks= }')
        questionmark_to_damaged = calculated_number_of_damaged_springs - number_of_damaged_springs
        questionmark_to_operational = number_of_questionmarks - questionmark_to_damaged

        translate_sequence = "." * questionmark_to_operational + "#" * questionmark_to_damaged

        # generate all possible combinations
        # ?.? can be: (...) or (..#) or (#..) or (#.#)
        # ???.### 1,1,3 -> #.#.### 1, 1, 3 -> True

        for co in product(".#", repeat=number_of_questionmarks):
            if co.count("#") != questionmark_to_damaged:
                continue
            j = 0
            new_row = []
            for i in range(len(spring_row)):
                if spring_row[i] == "?":
                    new_row.append(co[j])
                    j += 1
                else:
                    new_row.append(spring_row[i])
            if is_valid_condition_record([new_row, cr[1]]):
                number_of_different_arrangements += 1

    print(f'{number_of_different_arrangements= }')
    return number_of_different_arrangements


def compute_part_two(file_name: str) -> int:
    # TODO bring back resolution time, solutions works, but way too slow ...
    condition_records = read_input_file(file_name)
    number_of_different_arrangements = 0
    for cr in condition_records:
        spring_row = cr[0] + ["?"] + cr[0] + ["?"] + cr[0] + ["?"] + cr[0] + ["?"] + cr[0]
        item = "?"
        number_of_questionmarks = spring_row.count(item)
        print(f'{number_of_questionmarks= }')
        number_of_damaged_springs = spring_row.count('#')
        calculated_number_of_damaged_springs = sum(cr[1] * 5)
        questionmark_to_damaged = calculated_number_of_damaged_springs - number_of_damaged_springs

        # generate all possible combinations
        # ?.? can be: (...) or (..#) or (#..) or (#.#)
        # ???.### 1,1,3 -> #.#.### 1, 1, 3 -> True

        for co in product(".#", repeat=number_of_questionmarks):
            if co.count("#") != questionmark_to_damaged:
                continue
            # search and replace ? with either . or #
            j = 0
            new_row = []
            for i in range(len(spring_row)):
                if spring_row[i] == "?":
                    new_row.append(co[j])
                    j += 1
                else:
                    new_row.append(spring_row[i])
            cr_times5 = cr[1] * 5
            if is_valid_condition_record([new_row, cr_times5]):
                number_of_different_arrangements += 1

    print(f'{number_of_different_arrangements= }')
    return number_of_different_arrangements


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input12.txt')}")
    print(f"Part II: {compute_part_two('input/input12.txt')}")
    for co in set(permutations("AAB", 3)):
        print(co)
