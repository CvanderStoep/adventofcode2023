import networkx
import itertools
from math import prod


def read_input_file(file_name: str) -> list:
    # pattern = r"[+-]?\d+"
    components = []

    with open(file_name) as f:
        content = f.read().splitlines()

    for line in content:
        lhs, rhs = line.split(": ")
        rhs = rhs.split()
        components.append((lhs, rhs))

    return components


def compose_edges(components: list) -> list:
    edges = []
    for component in components:
        node1 = component[0]
        for node2 in component[1]:
            # print(node1, node2)
            edges.append((node1, node2))

    return edges


def compute_part_one(file_name: str) -> int:
    components = read_input_file(file_name)
    edges = compose_edges(components)
    for comb in itertools.combinations(edges, len(edges) - 3):
        graph = networkx.Graph()
        graph.add_edges_from(comb)
        cc = networkx.connected_components(graph)
        if networkx.number_connected_components(graph) != 1:
            product = 1
            for c in cc:
                print(len(c), c)
                product *= len(c)
            break
    print(f'{product= }')
    return product


def compute_part_one_alter(file_name: str) -> int:
    components = read_input_file(file_name)
    edges = compose_edges(components)
    graph = networkx.Graph()
    graph.add_edges_from(edges)

    # _, groups = networkx.stoer_wagner(graph)
    # product = len(groups[0] * len(groups[1]))

    # alternative:
    # e = networkx.minimum_edge_cut(graph)
    # print(e)
    graph.remove_edges_from(networkx.minimum_edge_cut(graph))
    print(prod([len(c) for c in networkx.connected_components(graph)]))

    return 0


if __name__ == '__main__':
    print(f"Part I: {compute_part_one_alter('input/input25.txt')}")
    print(f"Part I: {compute_part_one('input/input25.txt')}")
