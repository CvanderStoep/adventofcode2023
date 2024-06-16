from dataclasses import dataclass
import itertools


def read_input_file(file_name: str) -> list:
    # pattern = r"[+-]?\d+"
    stones = []

    with open(file_name) as f:
        content = f.read().splitlines()

    for line in content:
        position, velocity = line.split("@")
        position = position.split(',')
        velocity = velocity.split(',')
        x, y, z = int(position[0]), int(position[1]), int(position[2])
        vx, vy, vz = int(velocity[0]), int(velocity[1]), int(velocity[2])
        hailstone = Hailstone(x, y, z, vx, vy, vz)
        stones.append(hailstone)

    return stones


@dataclass
class Hailstone:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int


def intersection(hs1: Hailstone, hs2: Hailstone, area_min, area_max):
    # x1 + lambda v1, x2 + mu v2
    x1, y1, u1, v1 = hs1.x, hs1.y, hs1.vx, hs1.vy
    x2, y2, u2, v2 = hs2.x, hs2.y, hs2.vx, hs2.vy

    if (u2 * v1 - u1 * v2) == 0:
        # print("parallel")
        return False

    mu = ((x1 - x2) * v1 + (y2 - y1) * u1) / (u2 * v1 - u1 * v2)
    lamb = (x2 - x1 + mu * u2) / u1

    if mu < 0 or lamb < 0:
        # print("in the past")
        return False

    x_intersection = x1 + lamb * u1
    y_intersection = y1 + lamb * v1

    if x_intersection < area_min or x_intersection > area_max:
        # print("outside area")
        return False
    if y_intersection < area_min or y_intersection > area_max:
        # print("outside area")
        return False

    # print("inside area and in the future")
    return True


def collision(hs1: Hailstone, hs2: Hailstone):
    # x1 + lambda v1, x2 + mu v2
    x1, y1, z1, u1, v1, w1 = hs1.x, hs1.y, hs1.z, hs1.vx, hs1.vy, hs1.vz
    x2, y2, z2, u2, v2, w2 = hs2.x, hs2.y, hs2.z, hs2.vx, hs2.vy, hs2.vz

    if (u2 * v1 - u1 * v2) == 0:
        # print("parallel")
        return False

    mu = ((x1 - x2) * v1 + (y2 - y1) * u1) / (u2 * v1 - u1 * v2)
    lamb = (x2 - x1 + mu * u2) / u1

    x_intersection = x1 + lamb * u1
    y_intersection = y1 + lamb * v1
    z_intersection = z1 + lamb * w1 == z2 + lamb * w2
    # print(x_intersection, y_intersection, z_intersection)

    if mu == lamb and z_intersection:
        # print("collision", mu)
        return True

    # print("inside area and in the future")
    return False


def compute_part_one(file_name: str) -> int:
    stones = read_input_file(file_name)
    # area_min = 200000000000000
    # area_max = 400000000000000
    area_min = 7
    area_max = 27
    combs = list(itertools.combinations(stones, 2))
    number_of_intersections = 0
    for comb in combs:
        hs1, hs2 = comb[0], comb[1]
        intersects = intersection(hs1, hs2, area_min, area_max)
        if intersects:
            number_of_intersections += 1

    print(f'{number_of_intersections= }')
    return number_of_intersections


def compute_part_two(file_name: str) -> int:
    stones = read_input_file(file_name)

    for x in range(20, 30):
        hs1 = Hailstone(x, 13, 10, -3, 1, 2)
        # print(hs1)
        stone_collision = True
        for stone in stones:
            collides = collision(hs1, stone)
            if not collides:
                # print("no collision")
                stone_collision = False
                break
        if stone_collision:
            print("found", hs1)



    return 0


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input24.txt')}")
    print(f"Part II: {compute_part_two('input/input24.txt')}")
