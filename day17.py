from dataclasses import dataclass
import heapq


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    blocks = []
    for line in content:
        line = [int(element) for element in line]
        blocks.append(list(line))

    rows, cols = block_size(blocks)
    for i in range(cols):
        for j in range(rows):
            heat = blocks[j][i]
            blocks[j][i] = Block(i, j, heat, route=[])

    return blocks


def block_size(blocks: list) -> (int, int):
    rows = len(blocks)
    cols = len(blocks[0])

    return rows, cols


@dataclass
class Block:
    i: int
    j: int
    heat: int
    route: list
    total_heat: float = float('inf')
    visited: bool = False


def dijkstra(blocks: list, start: tuple):
    # TODO modify function to exclude a path with more than 3 consecutive steps in the same direction.

    i, j = start[0], start[1]
    start_block: Block = blocks[j][i]
    start_block.total_heat = 0
    priority_queue = [(i, start)]

    while priority_queue:
        current_total, current_block_index = heapq.heappop(priority_queue)
        i, j = current_block_index[0], current_block_index[1]
        current_block: Block = blocks[j][i]
        current_block.visited = True

        for neighbor in surrounding(blocks, i, j):
            i_n, j_n = neighbor[0], neighbor[1]
            neighbor_block: Block = blocks[j_n][i_n]
            if neighbor_block.visited:
                continue
            total_heat = current_total + neighbor_block.heat

            if total_heat < neighbor_block.total_heat:
                neighbor_block.total_heat = total_heat
                neighbor_block.route.append((i, j))
                heapq.heappush(priority_queue, (total_heat, neighbor))

    return 0


def surrounding(blocks, x: int, y: int) -> list:
    """return a list of surrounding neighbours"""
    vals = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [(x_i, y_i) for (x_i, y_i) in vals if 0 <= x_i < len(blocks[0]) and 0 <= y_i < len(blocks)]


def compute_part_one(file_name: str) -> int:
    blocks = read_input_file(file_name)
    rows, cols = block_size(blocks)
    start = (0, 0)
    finish = (cols-1, rows-1)
    dijkstra(blocks, start)
    for line in blocks:
        for block in line:
            print(block)

    i, j = finish[0], finish[1]
    current_block: Block = blocks[j][i]
    print(f'{current_block.total_heat= }')
    while True:
        i_previous, j_previous = current_block.route[0][0], current_block.route[0][1]
        current_block = blocks[j_previous][i_previous]
        print(f'{current_block= }')
        if i_previous == 0 and j_previous == 0:
            break

    return 0


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input17.txt')}")
    # print(f"Part II: {compute_part_two('input/input17.txt')}")
