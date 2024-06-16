def read_input_file(file_name: str) -> list:
    # pattern = r"[+-]?\d+"
    bricks = []

    with open(file_name) as f:
        content = f.read().splitlines()

    for line in content:
        begin, end = line.split('~')
        x, y, z = begin.split(',')
        x, y, z = int(x), int(y), int(z)
        a, b, c = begin.split(',')
        a, b, c = int(a), int(b), int(c)
        bricks.append(((x, y, z), (a, b, c)))

    return bricks


def compute_part_one(file_name: str) -> int:
    bricks = read_input_file(file_name)
    for brick in bricks:
        print(brick)

    return 0


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input22.txt')}")
    # print(f"Part II: {compute_part_two('input/input22.txt')}")
