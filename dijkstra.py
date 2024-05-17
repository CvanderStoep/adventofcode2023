# Converting our graph to an edge list
edge_list = [('A', 'B', 3), ('A', 'C', 8), ('B', 'C', 2), ('B', 'E', 5), ('C', 'D', 1), ('C', 'E', 6), ('D', 'E', 2),
             ('D', 'F', 3), ('E', 'F', 5)]


# Converting our graph to an adjacency list
def edge_list_to_adjacency_list(edge_list):
    adj_list = {}
    for (src, dest, weight) in edge_list:
        if src not in adj_list:
            adj_list[src] = {}
        if dest not in adj_list:
            adj_list[dest] = {}

        adj_list[src][dest] = weight
        adj_list[dest][src] = weight

    return adj_list


adj_list = edge_list_to_adjacency_list(edge_list)
print(adj_list)

# Implementing Dijkstra's Algorithm in Python
import heapq


def dijkstra(adj_list, start):
    distances = {node: float('inf') for node in adj_list}
    distances[start] = 0
    visited = set()

    # Priority queue to track nodes and current shortest distance
    priority_queue = [(0, start)]

    while priority_queue:
        # Pop the node with the smallest distance from the priority queue
        print(f'{priority_queue= }')
        current_distance, current_node = heapq.heappop(priority_queue)
        visited.add(current_node)
        print(f'{distances= }')
        print(f'{visited= }')
        print()


        # Skip if a shorter distance to current_node is already found
        # if current_distance > distances[current_node]:
        #     continue

        # Explore neighbors and update distances if a shorter path is found
        for neighbor, weight in adj_list[current_node].items():
            print(f'{current_node= }, {adj_list[current_node]= }, {neighbor= }')
            if neighbor in visited:
                continue
            distance = current_distance + weight

            # If shorter path to neighbor is found, update distance and push to queue
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


print(dijkstra(adj_list, 'A'))
