from collections import deque 

print("Exploring connections in a network")
print("Using a queue-based approach\n")

def bfs_find_path(graph, start_junction, target_junction):
    """Explores connections to find a route."""
    queue = deque([[start_junction]])
    visited = {start_junction}
    while queue:
        path = queue.popleft()
        node = path[-1]
        
        if node == target_junction:
            return path, visited 
    
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
    
    return None, visited

if __name__ == "__main__":
    # Sample exercise for exploring connections
    graph = {
        'A' : ['B', 'C'],
        'B' : ['A', 'D', 'E'],
        'C' : ['A', 'F'],
        'D' : ['B'],
        'E' : ['B', 'F'],
        'F' : ['C', 'E']
    }

    start_junction = 'A'
    target_junction = 'F'
    final_path, junctions_visited_during_search = bfs_find_path(graph, start_junction, target_junction)
    if final_path:
        print("Route:", " -> ".join(final_path))
    else:
        print("No route found.")
