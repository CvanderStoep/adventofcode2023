import queue
from dataclasses import dataclass

# import re

"""see also day12 (aoc2022) and day24
---> i (x)
|
j(y)   grid[j][i]
\/

data model:
grid[j][i] = "tile symbol"
Node class, individual nodes
nodes, dictionary of nodes; key = (i,j), value = node

"""


@dataclass
class Node:
    i: int  # x coordinate
    j: int  # y coordinate
    tile: str
    neighbours: list
    visited: bool = False
    depth: int = 0


def surrounding(grid, x: int, y: int) -> list:
    """return a list of surrounding neighbours"""
    vals = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    # print(f'{x= }, {y= }, {vals= }, {len(grid[0])= }, {len(grid)= }')
    return [(x_i, y_i) for (x_i, y_i) in vals if 0 <= x_i < len(grid[0]) and 0 <= y_i < len(grid)]


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

    return rows, cols


def grid_to_nodes_dictionary(grid) -> list:
    """" transforms a grid[j][i] into a dictionary of nodes and also fill the neighbours for each node"""

    rows, cols = grid_size(grid)
    # create all nodes from the grid
    nodes = {}
    for i in range(cols):
        for j in range(rows):
            node = Node(i=i, j=j, tile=grid[j][i], neighbours=[])
            nodes.update({(i, j): node})

    # update the neighbours for all nodes.
    for i in range(cols):
        for j in range(rows):
            node = nodes[(i, j)]
            surrounding_nodes = surrounding(grid, i, j)
            for sr in surrounding_nodes:
                x, y = sr[0], sr[1]
                sr_node = nodes[(x, y)]
                if valid_neighbours(node, sr_node):
                    node.neighbours.append(sr_node)

    return nodes


# check if valid neighbours (i, j), (x, y)
def valid_neighbours(node1: Node, node2: Node) -> bool:
    """are two nodes connected by the correct pipe type"""
    if node1.tile == "." or node2.tile == ".":
        return False

    key = (node1.tile, node2.i - node1.i, node2.j - node1.j)
    valid_combinations = {("|", 0, -1): "|7F", ("|", 0, 1): "|LJ",
                          ("-", 1, 0): "-7J", ("-", -1, 0): "-FL",
                          ("F", 1, 0): "-7J", ("F", 0, 1): "|JL",
                          ("7", -1, 0): "-FL", ("7", 0, 1): "|LJ",
                          ("J", 0, -1): "|F7", ("J", -1, 0): "-LF",
                          ("L", 0, -1): "|7F", ("L", 1, 0): "-J7"}

    valid_combination = valid_combinations.get(key)
    if valid_combination is None:
        return False
    if node2.tile in valid_combination:
        return True
    else:
        return False


def print_maze_grid(grid):
    """prints a small porting of the grid around the starting positions"""
    rows, cols = grid_size(grid)
    i_s, j_s = find_start(grid)
    for j in range(j_s - 1, j_s + 2):  # rows
        for i in range(i_s - 3, i_s + 3):  # cols
            print(grid[j][i], end="")
        print()


def print_full_maze_grid(grid):
    """prints the full grid"""
    rows, cols = grid_size(grid)
    i_s, j_s = find_start(grid)
    for j in range(rows):  # rows
        for i in range(cols):  # cols
            print(grid[j][i], end="")
        print()


def print_maze_dict(nodes_dict, grid):
    """prints the full grid (depth of the nodes)"""
    rows, cols = grid_size(grid)

    for j in range(rows):
        for i in range(cols):
            node = nodes_dict[(i, j)]
            print(node.depth, end="")
        print()


def node_inside(nodes_dict, grid, node: Node) -> bool:
    """check whether a nodes is inside or outside a closed loop by counting the number of crossings
     by walking towards the end of the grid; in this case diagonally"""
    rows, cols = grid_size(grid)

    node_i = node.i
    node_j = node.j

    if node_j == rows-1:
        pass
    if node_i == 0 or node_i == cols-1 or node_j == 0 or node_j == rows-1:
        return False

    number_of_crossings = 0
    while node_i < cols and node_j < rows:
        running_node = nodes_dict[(node_i, node_j)]
        # print(node_i, node_j, running_node.depth)
        node_i += 1
        node_j += 1
        if running_node.tile not in ".L7" and running_node.depth != 0:
            number_of_crossings += 1

    # print(f'{number_of_crossings= }')

    if number_of_crossings % 2 == 0:
        return False

    return True


def find_start(grid) -> (int, int):
    rows, cols = grid_size(grid)

    for j in range(rows):
        for i in range(cols):
            if grid[j][i] == "S":
                # print(f'{i= }, {j= }')
                return i, j

    return 0, 0


def compute_part_one(file_name: str) -> int:
    grid = read_input_file(file_name)

    start_i, start_j = find_start(grid)
    grid[start_j][start_i] = "-"

    nodes_dict = grid_to_nodes_dictionary(grid)

    node = nodes_dict[(start_i, start_j)]
    node.visited = True
    node.depth = 0
    node_queue = queue.Queue()
    node_queue.put(node)

    while not node_queue.empty():
        node = node_queue.get()
        for sr in node.neighbours:
            if not sr.visited:
                sr.visited = True
                sr.depth = node.depth + 1
                # print(f'{sr.depth= }')
                node_queue.put(sr)

    max_depth = 0
    for node in nodes_dict.values():
        max_depth = max(max_depth, node.depth)

    return max_depth


def compute_part_two(file_name: str) -> int:
    grid = read_input_file(file_name)

    start_i, start_j = find_start(grid)
    grid[start_j][start_i] = "-"

    nodes_dict = grid_to_nodes_dictionary(grid)

    node = nodes_dict[(start_i, start_j)]
    node.visited = True
    node.depth = 0
    node_queue = queue.Queue()
    node_queue.put(node)

    while not node_queue.empty():
        node = node_queue.get()
        for sr in node.neighbours:
            if not sr.visited:
                sr.visited = True
                sr.depth = node.depth + 1
                node_queue.put(sr)

    max_depth = 0
    for node in nodes_dict.values():
        max_depth = max(max_depth, node.depth)

    node = nodes_dict[(start_i, start_j)]
    node.depth = -1  # set the depth of the starting node = -1 to avoid seeing it as a .

    number_inside_nodes = 0
    rows, cols = grid_size(grid)
    for j in range(rows):
        for i in range(cols):
            node = nodes_dict[(i, j)]
            if node.depth == 0:
                inside = node_inside(nodes_dict, grid, node)
                if inside:
                    grid[j][i] = "I"
                    number_inside_nodes += 1
                else:
                    grid[j][i] = "O"

    return number_inside_nodes


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input10.txt')}")
    print(f"Part II: {compute_part_two('input/input10.txt')}")
