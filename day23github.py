# https://gist.github.com/Voltara/ae028b17ba5cd69fa9b8b912e41e853b

import fileinput
from collections import defaultdict


class Graph:
    def __init__(self, base_cost, down_cost, right_cost):
        self.base_cost = base_cost
        self.down_cost = down_cost
        self.right_cost = right_cost
        self.dim = max(down_cost)[0]


def solve_part1(graph):
    from_above = [0] * graph.dim
    for r in range(graph.dim):
        from_left = 0
        for c in range(graph.dim):
            cost = max(from_left, from_above[c])
            from_above[c] = cost + graph.down_cost[r, c]
            from_left = cost + graph.right_cost[r, c]
    return graph.base_cost + from_above[-1]


def solve_part2(graph):
    dots = '.' * (graph.dim - 1)

    def matching_paren(key, col, step):
        nest = step
        while nest != 0:
            col += step
            if key[col] == '(':
                nest += 1
            if key[col] == ')':
                nest -= 1
        return col

    def transition(key, cost, col=0, left='.'):
        if col == graph.dim:
            if left == '.':
                key = ''.join(key)
                next_dp[key] = max(next_dp[key], cost)
            return

        key = list(key)

        def next_col(down, right):
            cost_delta = 0
            if down != '.':
                cost_delta += graph.down_cost[row, col]
            if right != '.':
                cost_delta += graph.right_cost[row, col]
            key[col] = down
            transition(key, cost + cost_delta, col + 1, right)

        up = key[col]
        match left + up:
            case '.(' | '.)' | '(.' | ').':
                next_col(up, left)
                next_col(left, up)
            case '..':
                next_col(*'()')
                next_col(*'..')
            case '((':
                key[matching_paren(key, col, +1)] = '('
                next_col(*'..')
            case '))':
                key[matching_paren(key, col, -1)] = ')'
                next_col(*'..')
            case ')(':
                next_col(*'..')

    dp, next_dp = defaultdict(int), defaultdict(int)
    dp['(' + dots + ')'] = graph.base_cost

    for row in range(graph.dim):
        for key, cost in dp.items():
            transition(list(key), cost)
        dp, next_dp = next_dp, dp

    return dp[dots + '()']


def maze_to_graph(maze):
    dim = len(maze)
    assert dim == len(maze[0])

    DOWN, RIGHT = (1, 0), (0, 1)
    down_cost, right_cost = defaultdict(int), defaultdict(int)

    def coord_add(lhs, rhs):
        return (lhs[0] + rhs[0], lhs[1] + rhs[1])

    def coord_max(lhs, rhs):
        return (max(lhs[0], rhs[0]), max(lhs[1], rhs[1]))

    def get(coord):
        return maze[coord[0]][coord[1]] if coord[0] < dim else '#'

    def pathfind(coord, direction, node):
        step, coord = direction, coord_add(coord, direction)
        if get(coord) == '#':
            return 0

        length, markers_seen = 1, 0
        while markers_seen < 2:
            length += 1
            if get(coord) != '.':
                markers_seen += 1
            for next_step in [step, (-step[1], step[0]), (step[1], -step[0])]:
                next_coord = coord_add(coord, next_step)
                if get(next_coord) != '#':
                    break
            coord, step = next_coord, next_step

        node = coord_add(node, coord_max(direction, step))
        for costs, step in [(down_cost, DOWN), (right_cost, RIGHT)]:
            if node not in costs:
                costs[node] = pathfind(coord, step, node)

        return length

    maze[1][1], maze[-2][-2] = 'v', 'v'
    base_cost = pathfind((0, 1), DOWN, (-1, 0))

    return Graph(base_cost, down_cost, right_cost)


filename = 'input/input23.txt'
graph = maze_to_graph([list(line.rstrip()) for line in fileinput.input(files=filename)])

print('Part 1:', solve_part1(graph))
print('Part 2:', solve_part2(graph))
