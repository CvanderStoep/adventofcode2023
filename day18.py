from shapely.geometry.polygon import *


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    plan = []
    for line in content:
        items = line.split()
        items[1] = int(items[1])
        items[2] = items[2][1:-1]  # remove first & last element
        plan.append(items)

    # print(plan)

    return plan


def read_input_file2(file_name: str) -> list:
    directions = {0: "R", 1: "D", 2: "L", 3: "U"}

    with open(file_name) as f:
        content = f.read().splitlines()

    plan = []
    for line in content:
        items = line.split()
        items[1] = int(items[1])
        items[2] = items[2][1:-1]  # remove first & last element
        direction = int(items[2][-1])
        distance = int(items[2][1:-1], 16)
        # print(direction, distance, items[2][1:-1])
        items[0] = directions[direction]
        items[1] = distance
        # print(items)
        plan.append(items)

    # print(plan)

    return plan


def dig_trench(lagoon: set, dig: list, position: tuple) -> set:
    directions = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}
    direction, steps = dig[0], dig[1]
    dx, dy = position[0], position[1]
    for step in range(steps):
        dx += directions[direction][0]
        dy += directions[direction][1]
        lagoon.add((dx, dy))
    position = (dx, dy)

    return position


def covert_dig_list_to_coordinates(dig_plan: list, position: tuple) -> list:
    """convert input/dig-plan to set of coordinates"""
    coordinates = []
    directions = {"R": (1, 0), "L": (-1, 0), "U": (0, -1), "D": (0, 1)}
    dx, dy = position[0], position[1]
    coordinates.append([dx, dy])

    for dig in dig_plan:
        direction, steps = dig[0], dig[1]
        dx += directions[direction][0] * steps
        dy += directions[direction][1] * steps
        coordinates.append([dx, dy])

    return coordinates


def print_lagoon(lagoon):
    x_min = min([x[0] for x in lagoon])
    x_max = max([x[0] for x in lagoon])
    y_min = min([x[1] for x in lagoon])
    y_max = max([x[1] for x in lagoon])
    for y in range(y_min, y_max + 1):
        for x in range(x_min, x_max + 1):
            if (x, y) in lagoon:
                print("#", end='')
            else:
                print(".", end='')
        print()


def fill(lagoon: set, visited: set, x, y):
    x_min = min([x[0] for x in lagoon])
    x_max = max([x[0] for x in lagoon])
    y_min = min([x[1] for x in lagoon])
    y_max = max([x[1] for x in lagoon])

    seen = set()
    is_lava = True

    queue = [(x, y)]
    while queue:
        x, y = queue.pop()
        if (x, y) in seen:
            continue
        if (x, y) in lagoon:
            continue
        if x == x_min or x == x_max or y == y_min or y == y_max:
            is_lava = False
            continue
        seen.add((x, y))

        if x > x_min:
            queue.append((x - 1, y))
        if x < x_max:
            queue.append((x + 1, y))
        if y > y_min:
            queue.append((x, y - 1))
        if y < y_max:
            queue.append((x, y + 1))

    for (x, y) in seen:
        if is_lava:
            lagoon.add((x, y))
        visited.add((x, y))


def size_lagoon(lagoon: set):
    x_min = min([x[0] for x in lagoon])
    x_max = max([x[0] for x in lagoon])
    y_min = min([x[1] for x in lagoon])
    y_max = max([x[1] for x in lagoon])

    return x_min, x_max, y_min, y_max


def compute_part_one(file_name: str) -> int:
    dig_plan = read_input_file(file_name)
    start = (0, 0)
    lagoon = set()
    lagoon.add(start)

    for dig in dig_plan:
        start = dig_trench(lagoon, dig, position=start)

    print(lagoon)
    print_lagoon(lagoon)
    print()

    visited = set()
    for item in lagoon:
        visited.add(item)

    x_min, x_max, y_min, y_max = size_lagoon(lagoon)

    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            if (x, y) not in visited:
                fill(lagoon, visited, x, y)

    print_lagoon(lagoon)
    print(f'{len(lagoon)= }')

    return len(lagoon)


def calculate_area(coordinates: list) -> int:
    """calculate the area using surveyor's method"""
    area = 0
    length = 0
    for i in range(len(coordinates) - 1):
        x1 = coordinates[i][0]
        y1 = coordinates[i][1]
        x2 = coordinates[i + 1][0]
        y2 = coordinates[i + 1][1]
        area = area + (x1 * y2) - (x2 * y1)
        length = length + abs(x2 - x1) + abs(y2 - y1)

    area = abs(area) / 2
    print(f'{area= }')
    print(f'{length= }')
    poly = Polygon(coordinates)
    print(f'{poly.area= }, {poly.length= }')
    area = poly.area + poly.length // 2 + 1

    return int(area)


def compute_part_two(file_name: str) -> int:
    dig_plan = read_input_file2(file_name)
    start = (0, 0)
    coordinates = covert_dig_list_to_coordinates(dig_plan, start)
    area = calculate_area(coordinates)


    return area


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input18.txt')}")
    print(f"Part II: {compute_part_two('input/input18.txt')}")
