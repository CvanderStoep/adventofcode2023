import re


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    for line in content:
        sequence = line.split(',')

    return sequence


def hash_algorithm(step: str) -> int:
    current_value = 0
    for c in step:
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256

    return current_value


def compute_part_one(file_name: str) -> int:
    sequence = read_input_file(file_name)

    sum_of_results = 0
    for step in sequence:
        sum_of_results += hash_algorithm(step)

    print(f'{sum_of_results= }')
    return sum_of_results


def remove_lens(box: list, step: str) -> None:
    pattern1 = "[a-z]+"
    step_label = re.findall(pattern1, step)[0]

    for lens in box:
        lens_label = re.findall(pattern1, lens)[0]
        if lens_label == step_label:
            box.remove(lens)


def replace_or_add_lens(box: list, step: str) -> None:
    pattern1 = "[a-z]+"
    step_label = re.findall(pattern1, step)[0]

    for i, lens in enumerate(box):
        lens_label = re.findall(pattern1, lens)[0]
        if lens_label == step_label:
            box[i] = step
            return
    box.append(step)


def compute_part_two(file_name: str) -> int:
    sequence = read_input_file(file_name)
    boxes = [[] for _ in range(256)]
    pattern1 = "[a-z]+"
    pattern2 = "[=-]"

    for step in sequence:
        box_label = re.findall(pattern1, step)[0]
        box_number = hash_algorithm(box_label)
        box = boxes[box_number]
        operation = re.findall(pattern2, step)[0]
        if operation == "=":
            replace_or_add_lens(box, step)
        else:
            remove_lens(box, step)

    total_focusing_power = 0
    for i, box in enumerate(boxes):
        for j, lens in enumerate(box):
            focus_power = (i + 1) * (j + 1) * int(lens[-1])
            total_focusing_power += focus_power

    print(f'{total_focusing_power= }')

    return total_focusing_power


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input15.txt')}")
    print(f"Part II: {compute_part_two('input/input15.txt')}")
