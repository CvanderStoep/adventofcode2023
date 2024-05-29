import queue
import copy


def read_input_file(file_name: str) -> list:
    # pattern = r"[+-]?\d+"
    grid = []

    with open(file_name) as f:
        content = f.read().splitlines()

    for line in content:
        grid.append(list(line))

    return grid


def grid_size(grid) -> (int, int):
    rows = len(grid)
    cols = len(grid[0])

    width = len(grid[0])
    height = len(grid)

    return rows, cols


def surrounding(grid, x: int, y: int) -> list:
    """return a list of surrounding neighbours"""
    vals = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    # print(f'{x= }, {y= }, {vals= }, {len(grid[0])= }, {len(grid)= }')
    return [(x_i, y_i) for (x_i, y_i) in vals if 0 <= x_i < len(grid[0]) and 0 <= y_i < len(grid)]


def surrounding_no_limit(grid, x: int, y: int) -> list:
    """return a list of surrounding neighbours"""
    vals = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [(x_i, y_i) for (x_i, y_i) in vals]


def print_grid(grid):
    """prints the full grid"""
    rows, cols = grid_size(grid)
    for j in range(rows):  # rows
        for i in range(cols):  # cols
            print(grid[j][i], end="")
        print()


def find_start(grid) -> (int, int):
    rows, cols = grid_size(grid)

    for j in range(rows):
        for i in range(cols):
            if grid[j][i] == "S":
                return i, j


def count_steps(grid) -> int:
    rows, cols = grid_size(grid)
    number_of_steps = 0
    for j in range(rows):
        for i in range(cols):
            if grid[j][i] == "O":
                number_of_steps += 1

    return number_of_steps


def compute_part_one(file_name: str) -> int:
    grid = read_input_file(file_name)
    print_grid(grid)

    start_i, start_j = find_start(grid)
    node = find_start(grid)

    garden_queue = queue.Queue()
    garden_queue.put((start_i, start_j))
    steps = 64
    for step in range(steps):
        temp_queue = queue.Queue()
        while not garden_queue.empty():
            node = garden_queue.get()
            for neighbours in surrounding(grid, node[0], node[1]):
                x_n, y_n = neighbours[0], neighbours[1]
                if grid[y_n][x_n] in ".S":
                    grid[y_n][x_n] = "O"
                    temp_queue.put((x_n, y_n))
        # print_grid(grid)
        # print()
        if step == steps - 1:
            number_of_steps = count_steps(grid)
            print(f'{number_of_steps= }')
        while not temp_queue.empty():
            node = temp_queue.get()
            x_n, y_n = node[0], node[1]
            grid[y_n][x_n] = "."
            garden_queue.put((x_n, y_n))

    return number_of_steps


def compute_part_two(file_name: str) -> int:
    grid = read_input_file(file_name)
    rows, cols = grid_size(grid)

    # start_i, start_j = find_start(grid)
    start_node = find_start(grid)

    garden_queue = set()
    # garden_queue.add((start_i, start_j))
    garden_queue.add(start_node)
    steps = 500
    for step in range(steps):
        print(f'{step= }')
        temp_queue = set()
        visited = set()

        while garden_queue:
            node = garden_queue.pop()
            if node in visited:
                continue
            visited.add(node)
            for neighbours in surrounding_no_limit(grid, node[0], node[1]):
                x_n, y_n = neighbours[0], neighbours[1]
                if grid[y_n % rows][x_n % cols] in ".S":
                    temp_queue.add((x_n, y_n))
        if step == steps - 1:
            number_of_steps = len(temp_queue)
            print(f'{number_of_steps= }')
        garden_queue = copy.copy(temp_queue)

    return number_of_steps


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input21.txt')}")
    print(f"Part II: {compute_part_two('input/input21.txt')}")
