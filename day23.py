import networkx


def compute_part_one(file_name: str) -> int:
    with open(file_name) as f:
        data = f.read().strip()

    grid = data.split("\n")

    width = len(grid[0])
    height = len(grid)

    source = (1, 0)
    queue = [(source, set([source]))]

    max_length = 0

    directions = {
        ">": [(1, 0)],
        "<": [(-1, 0)],
        "v": [(0, 1)],
        "^": [(0, -1)],
        ".": [(-1, 0), (1, 0), (0, -1), (0, 1)]
    }

    while len(queue) > 0:
        (x, y), visited = queue.pop()

        if x == width - 2 and y == height - 1:
            max_length = max(max_length, len(visited) - 1)
            continue

        for dx, dy in directions[grid[y][x]]:
            nx, ny = x + dx, y + dy

            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            if grid[ny][nx] == "#":
                continue

            if (nx, ny) in visited:
                continue

            queue.append(((nx, ny), visited | set([(nx, ny)])))

    print(max_length)
    return max_length


def compute_part_two(file_name: str) -> int:
    with open(file_name) as f:
        data = f.read().strip()

    grid = data.split("\n")

    width = len(grid[0])
    height = len(grid)

    source = (1, 0)
    queue = [(source, set([source]))]

    max_length = 0

    directions = {
        ">": [(-1, 0), (1, 0), (0, -1), (0, 1)],
        "<": [(-1, 0), (1, 0), (0, -1), (0, 1)],
        "v": [(-1, 0), (1, 0), (0, -1), (0, 1)],
        "^": [(-1, 0), (1, 0), (0, -1), (0, 1)],
        ".": [(-1, 0), (1, 0), (0, -1), (0, 1)]
    }

    while len(queue) > 0:
        (x, y), visited = queue.pop()

        if x == width - 2 and y == height - 1:
            max_length = max(max_length, len(visited) - 1)
            continue

        for dx, dy in directions[grid[y][x]]:
            nx, ny = x + dx, y + dy

            if nx < 0 or nx >= width or ny < 0 or ny >= height:
                continue

            if grid[ny][nx] == "#":
                continue

            if (nx, ny) in visited:
                continue

            queue.append(((nx, ny), visited | set([(nx, ny)])))

    print(max_length)
    return max_length


def compute_part_two_alter(file_name: str) -> int:
    with open(file_name) as f:
        data = f.read().strip()

    grid = data.split("\n")

    width = len(grid[0])
    height = len(grid)
    graph = networkx.Graph()

    edges = []
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "#":
                continue
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy

                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    continue

                if grid[ny][nx] == "#":
                    continue

                edges.append((y * height + x, ny * height + nx))

    # print(edges)
    graph.add_edges_from(edges)
    max_length = 0
    x, y = 1, 0
    source = y * height + x
    x, y = width - 2, height - 1
    target = y * height + x
    shortest_path = networkx.shortest_path(graph, source=source, target=target)
    # print(shortest_path)
    # print(f'{len(shortest_path)= }')
    # for path in all_paths(graph, 1, (height - 1) * height + (width - 2)):
    #     max_length = max(max_length, len(path) - 1)

    all_paths = networkx.all_simple_paths(graph, source, target)
    i = 1
    for path in all_paths:
        # print(path)
        max_length = max(max_length, len(path) - 1)
        print(f'{i= }, {max_length= }')
        i += 1

    print(max_length)
    return max_length


if __name__ == "__main__":
    print(f"Part I: {compute_part_one('input/input23.txt')}")
    print(f"Part II: {compute_part_two_alter('input/input23.txt')}")
