import re
from dataclasses import dataclass


@dataclass
class Race:
    time: int
    distance: int


def read_input_file(file_name: str) -> list[Race]:
    races = []
    with open(file_name) as f:
        content = f.read().splitlines()
    for line in content:
        if "Time" in line:
            times = [int(digit) for digit in re.findall(r'(\d+)', line)]
        else:
            distances = [int(digit) for digit in re.findall(r'(\d+)', line)]

    for t, d in zip(times, distances):
        race = Race(time=t, distance=d)
        races.append(race)

    return races


def compute_part_one(file_name: str) -> int:
    races = read_input_file(file_name)
    overall_product = 1
    for race in races:
        total_time = race.time
        record_distance = race.distance
        record_broken = 0
        for button in range(total_time + 1):
            distance = (total_time - button) * button
            if distance > record_distance:
                record_broken += 1
        overall_product *= record_broken

    return overall_product


def compute_part_two(file_name: str) -> int:
    races = read_input_file(file_name)
    overall_product = 1
    total_time = ""
    record_distance = ""
    for race in races:
        total_time += str(race.time)
        record_distance += str(race.distance)
    total_time = int(total_time)
    record_distance = int(record_distance)
    record_broken = 0
    print(f'{total_time= }')
    for button in range(total_time + 1):
        distance = (total_time - button) * button
        if distance > record_distance:
            record_broken += 1
    overall_product *= record_broken

    return overall_product


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input6.txt')}")
    print(f"Part II: {compute_part_two('input/input6.txt')}")
