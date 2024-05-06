
def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    reflector = []
    for line in content:
        reflector.append(list(line))
    return reflector


def reflector_size(reflector: list) -> (int, int):
    rows = len(reflector)
    cols = len(reflector[0])

    return rows, cols


def move_up(reflector: list) -> list:
    rows, cols = reflector_size(reflector)
    rolled = True
    while rolled:  # keep moving rounded rocks up until it is not possible anymore
        rolled = False
        for j in range(1, rows):
            for i in range(cols):
                if reflector[j][i] == "O" and reflector[j - 1][i] == ".":
                    reflector[j - 1][i] = "O"
                    reflector[j][i] = "."
                    rolled = True

    return reflector


def move_left(reflector: list) -> list:
    rows, cols = reflector_size(reflector)
    rolled = True
    while rolled:  # keep moving rounded rocks up until it is not possible anymore
        rolled = False
        for i in range(1, cols):
            for j in range(rows):
                if reflector[j][i] == "O" and reflector[j][i - 1] == ".":
                    reflector[j][i - 1] = "O"
                    reflector[j][i] = "."
                    rolled = True

    return reflector


def move_right(reflector: list) -> list:
    rows, cols = reflector_size(reflector)
    rolled = True
    while rolled:  # keep moving rounded rocks up until it is not possible anymore
        rolled = False
        for i in range(cols - 2, -1, -1):
            for j in range(rows):
                if reflector[j][i] == "O" and reflector[j][i + 1] == ".":
                    reflector[j][i + 1] = "O"
                    reflector[j][i] = "."
                    rolled = True

    return reflector


def move_down(reflector: list) -> list:
    rows, cols = reflector_size(reflector)
    rolled = True
    while rolled:  # keep moving rounded rocks up until it is not possible anymore
        rolled = False
        for j in range(rows - 2, -1, -1):
            for i in range(cols):
                if reflector[j][i] == "O" and reflector[j + 1][i] == ".":
                    reflector[j + 1][i] = "O"
                    reflector[j][i] = "."
                    rolled = True

    return reflector


def compute_part_one(file_name: str) -> int:
    reflector = read_input_file(file_name)
    move_up(reflector)
    total_load = calculate_load(reflector)

    return total_load


def compute_part_two(file_name: str) -> int:
    reflector = read_input_file(file_name)
    load_pattern = []
    for i in range(200):
        move_up(reflector)
        move_left(reflector)
        move_down(reflector)
        move_right(reflector)

        total_load = calculate_load(reflector)
        load_pattern.append(total_load)
        print(f'{i+1= }, {total_load= }')

    preamble, repetition = find_pattern(load_pattern)
    print(f'{len(preamble)= }, {preamble= }')
    print(f'{len(repetition)= }, {repetition= }')

    total_load_number = (1_000_000_000 - len(preamble)) % len(repetition)
    print(f'{total_load_number= }')
    total_load = repetition[total_load_number - 1]

    return total_load


def find_pattern(data: list[int]) -> tuple[list[int], list[int]]:
    """"
    find pattern in a list of numbers
    a = [1, 1, 5, 6, 5, 6, 5, 6, 8, 9, 11, 12, 12, 11, 12, 12, 11, 12, 12]
    preamble = [1, 1, 5, 6, 5, 6, 5, 6, 8, 9]
    repetition = [11, 12, 12]
    """
    for p in range(len(data)):
        sd = data[p:]
        for r in range(2, len(sd) // 2):
            if sd[0:r] == sd[r:2 * r]:
                if all([(sd[0:r] == sd[y:y + r]) for y in range(r, len(sd) - r, r)]):
                    return data[:p], data[p:p + r]
    return [], []


def calculate_load(reflector: list) -> int:
    rows, _ = reflector_size(reflector)
    distance = rows
    load = 0
    for row in reflector:
        number_of_rounded_rocks = row.count("O")
        load += number_of_rounded_rocks * distance
        distance -= 1

    return load


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input14.txt')}")
    print(f"Part II: {compute_part_two('input/input14.txt')}")
