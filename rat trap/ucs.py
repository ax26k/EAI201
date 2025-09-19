from queue import PriorityQueue as PQ

print("Exploring connections in a network")
print("Using a cost-based approach\n")

def ucs(graph, start_node, target_node):
    """Explores connections to find a route."""
    priority_queue = PQ()
    priority_queue.put((0, start_node))  
    
    came_from = {start_node: None}
    cost_so_far = {start_node: 0}
    visited = set() 

    while not priority_queue.empty():
        current_cost, current_node = priority_queue.get()
        
        visited.add(current_node) 

        if current_node == target_node:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = came_from.get(current_node)
            path.reverse()
            return path, cost_so_far[target_node], visited 

        for neighbor, edge_cost in graph.get(current_node, []):
            new_cost = cost_so_far[current_node] + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority_queue.put((new_cost, neighbor))
                came_from[neighbor] = current_node

    return None, float('inf'), visited 

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
    start_node = 'A'
    target_node = 'F'
    path, cost, junctions_explored = ucs(graph, start_node, target_node)
    if path:
        print("Route:", " -> ".join(path))
    else:
        print("No route found.")
