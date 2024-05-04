"""
create list of patterns
pattern = [#.##..##.] as list
patterns = [pattern1, pattern2] as list of lists
"""
from copy import deepcopy


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    patterns = []
    pattern = []
    for line in content:
        if len(line) == 0:
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(list(line))
    patterns.append(pattern)
    return patterns


def pattern_size(pattern: list) -> (int, int):
    rows = len(pattern)
    cols = len(pattern[0])

    return rows, cols


def horizontal_mirror(pattern: list) -> int:
    """"returns the mirror row number or 0 if none exists; return row + 1 because the puzzle starts counting at 1"""
    rows, cols = pattern_size(pattern)

    for row_number in range(rows - 1):
        top, bottom = row_number, row_number + 1
        mirror = True
        while top >= 0 and bottom < rows:
            if pattern[top] != pattern[bottom]:
                mirror = False
                break
            top -= 1
            bottom += 1
        if mirror:
            return row_number + 1
    return 0


def horizontal_mirror2(pattern: list) -> list:
    """"returns the mirror row number or 0 if none exists; return row + 1 because the puzzle starts counting at 1"""
    rows, cols = pattern_size(pattern)

    mirror_rows = []
    for row_number in range(rows - 1):
        top, bottom = row_number, row_number + 1
        mirror = True
        while top >= 0 and bottom < rows:
            if pattern[top] != pattern[bottom]:
                mirror = False
                break
            top -= 1
            bottom += 1
        if mirror:
            mirror_rows.append(row_number + 1)
    return mirror_rows


def vertical_mirror(pattern: list) -> int:
    """"mirrors the pattern and check for horizontal mirror using horizontal_mirror function
    list(zip(*pattern)) does the same thing:
    transpose = list(zip(*pattern)), list of tuples
    transpose = [list(p) for p in transpose], list of lists
    """

    rows, cols = pattern_size(pattern)
    pattern_transpose = []
    for i in range(cols):
        row = []
        for j in range(rows):
            row.append(pattern[j][i])
        pattern_transpose.append(row)

    return horizontal_mirror(pattern_transpose)


def pattern_variations(pattern: list) -> list:
    rows, cols = pattern_size(pattern)
    pattern_variation_list = []

    for i in range(cols):
        for j in range(rows):
            element = pattern[j][i]
            new_pattern = deepcopy(pattern)
            if element == "#":
                new_pattern[j][i] = "."
            else:
                new_pattern[j][i] = "#"

            pattern_variation_list.append(new_pattern)

    return pattern_variation_list


def compute_part_one(file_name: str) -> int:
    patterns = read_input_file(file_name)
    note_summarize = 0
    for pattern in patterns:
        row_number = horizontal_mirror(pattern)
        note_summarize += 100 * row_number
        col_number = vertical_mirror(pattern)
        note_summarize += col_number

        # alternative
        # pattern = [list(p) for p in list(zip(*pattern))]
        # col_number = horizontal_mirror(pattern)

    return note_summarize


def compute_part_two(file_name: str) -> int:
    """
    repair the smudge; replace exactly one ./# with #/.
    find original mirror line
    find new mirror line(s)
    compare
    """
    patterns = read_input_file(file_name)
    note_summarize = 0
    for pattern in patterns:
        row_number1 = horizontal_mirror2(pattern)
        pattern_variations_list = pattern_variations(pattern)
        for p in pattern_variations_list:
            row_number2 = horizontal_mirror2(p)
            difference = list(set(row_number2) - set(row_number1))
            if difference:
                note_summarize += 100 * difference[0]
                break

        pattern = [list(p) for p in list(zip(*pattern))]
        col_number1 = horizontal_mirror2(pattern)
        pattern_variations_list = pattern_variations(pattern)
        for p in pattern_variations_list:
            col_number2 = horizontal_mirror2(p)
            difference = list(set(col_number2) - set(col_number1))
            if difference:
                note_summarize += difference[0]
                break

    return note_summarize


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input13.txt')}")
    print(f"Part II: {compute_part_two('input/input13.txt')}")
