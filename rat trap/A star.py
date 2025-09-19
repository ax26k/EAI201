from queue import PriorityQueue as PQ
import math

print("Exploring connections in a network")
print("Using a prioritized approach\n")

def heuristic(node, goal, coordinates):
    """Estimates distance between nodes."""
    x1, y1 = coordinates[node]
    x2, y2 = coordinates[goal]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def a_star_search(graph, start_node, target_node, coordinates):
    """Explores connections to find a route."""
    priority_queue = PQ()
    priority_queue.put((0, start_node))

    came_from = {start_node: None}
    cost_so_far = {start_node: 0}
    nodes_explored_count = 0

    while not priority_queue.empty():
        _, current_node = priority_queue.get()
        nodes_explored_count += 1
        if current_node == target_node: 
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from.get(current_node)
            path.reverse()
            return path, cost_so_far[target_node], nodes_explored_count

        for neighbor, edge_cost in graph.get(current_node, []):
            new_cost = cost_so_far[current_node] + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                
                priority = new_cost + heuristic(neighbor, target_node, coordinates)
                priority_queue.put((priority, neighbor))
                came_from[neighbor] = current_node
    
    return None, float('inf'), nodes_explored_count

if __name__ == "__main__":
    # Sample exercise for exploring connections
    graph = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 10), ('D', 2), ('E', 5)],
        'C': [('A', 4), ('F', 3)],
        'D': [('B', 2)],
        'E': [('B', 5), ('F', 1)],
        'F': [('C', 3), ('E', 1)]
    }
    coordinates = {
        'A': (0, 5),
        'B': (1, 3),
        'C': (4, 2),
        'D': (0, 2),
        'E': (3, 1),
        'F': (5, 0) 
    }
    start_node = 'A'
    target_node = 'F'
    path, cost, junctions_explored = a_star_search(graph, start_node, target_node, coordinates) 
    if path:
        print("Route:", " -> ".join(path))
    else:
        print("No route found.")
