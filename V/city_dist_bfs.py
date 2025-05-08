import heapq
import time
import networkx as nx
import matplotlib.pyplot as plt

def a_star_search(graph, start, goal):
    """
    Find the shortest path from start to goal city using A* Search.
    
    Args:
        graph: Dictionary mapping city names to dictionaries of neighbors and distances
        start: Name of the starting city
        goal: Name of the goal city
    
    Returns:
        path: List of cities in the path from start to goal, or None if no path exists
        total_distance: Total distance of the path
        nodes_expanded: Number of nodes explored during search
    """
    # Priority queue stores (f_score, g_score, current, path)
    open_list = [(straight_line_distances[start][goal], 0, start, [start])]
    closed_set = set()
    g_scores = {start: 0}  # Cost from start to current node
    nodes_expanded = 0
    
    while open_list:
        f_score, g_score, current, path = heapq.heappop(open_list)
        
        if current == goal:
            return path, g_score, nodes_expanded
        
        if current in closed_set:
            continue
        
        closed_set.add(current)
        nodes_expanded += 1
        
        if current in graph:
            for neighbor, edge_distance in graph[current].items():
                if neighbor in closed_set:
                    continue
                
                # Calculate g_score for this neighbor
                tentative_g_score = g_score + edge_distance
                
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g_score
                    h_score = straight_line_distances[neighbor][goal]
                    f_score = tentative_g_score + h_score  # f(n) = g(n) + h(n)
                    new_path = path + [neighbor]
                    heapq.heappush(open_list, (f_score, tentative_g_score, neighbor, new_path))
    
    return None, float('inf'), nodes_expanded  # No path found

def draw_graph(road_network, start, goal, shortest_path=None):
    """Draws a graph representation of the road network, highlighting the shortest path."""
    G = nx.Graph()
    
    for city in road_network:
        G.add_node(city)
    
    for city1 in road_network:
        for city2, distance in road_network[city1].items():
            if not G.has_edge(city2, city1):
                G.add_edge(city1, city2, weight=distance)

    pos = nx.spring_layout(G, seed=42)
    
    # Draw the base graph with light gray edges
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=1500, font_size=10, font_weight="bold", edge_color="lightgray")
    
    # Highlight start and goal nodes
    nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color="green", node_size=1800)
    nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color="red", node_size=1800)

    # Draw the shortest path with a dark blue line if it exists
    if shortest_path:
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="darkblue", width=2.5)

    # Draw edge labels with distances
    edge_labels = {(city1, city2): f"{distance}" for city1 in road_network for city2, distance in road_network[city1].items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, label_pos=0.5)

    plt.title("City Road Network with Shortest Path Highlighted (A* Search)")
    plt.show()

def get_user_input():
    """Get the cities, road connections, and straight-line distances from the user."""
    cities = []
    road_network = {}
    straight_line_distances = {}
    
    print("Enter the names of all cities (one per line). Type 'done' when finished:")
    while True:
        city = input().strip()
        if city.lower() == 'done':
            break
        if city not in cities:
            cities.append(city)
            road_network[city] = {}
            straight_line_distances[city] = {}
    
    if len(cities) < 2:
        print("At least two cities are required.")
        return get_user_input()
    
    print("\nEnter road connections between cities.")
    print("Format: 'City1,City2,Distance'. Type 'done' when finished:")
    
    while True:
        conn = input().strip()
        if conn.lower() == 'done':
            break
        try:
            city1, city2, distance = conn.split(',')
            city1, city2 = city1.strip(), city2.strip()
            distance = float(distance.strip())
            
            if city1 not in cities or city2 not in cities:
                print(f"Error: Both cities must be in the list. Available cities: {', '.join(cities)}")
                continue
                
            if distance <= 0:
                print("Error: Distance must be a positive number.")
                continue
                
            road_network[city1][city2] = distance
            road_network[city2][city1] = distance
            
        except ValueError:
            print("Invalid format. Please use 'City1,City2,Distance'.")
    
    print("\nEnter straight-line distances between each pair of cities.")
    
    for i, city1 in enumerate(cities):
        straight_line_distances[city1] = {}
        for j, city2 in enumerate(cities):
            if i != j:
                if city2 in straight_line_distances and city1 in straight_line_distances[city2]:
                    straight_line_distances[city1][city2] = straight_line_distances[city2][city1]
                else:
                    while True:
                        try:
                            dist = float(input(f"Straight-line distance from {city1} to {city2}: "))
                            if dist <= 0:
                                print("Error: Distance must be a positive number.")
                                continue
                            straight_line_distances[city1][city2] = dist
                            break
                        except ValueError:
                            print("Invalid input. Please enter a positive number.")
            else:
                straight_line_distances[city1][city2] = 0
    
    while True:
        start = input("\nEnter the starting city: ").strip()
        if start in cities:
            break
        print(f"City not found. Available cities: {', '.join(cities)}")
    
    while True:
        goal = input("Enter the goal city: ").strip()
        if goal in cities:
            if goal != start:
                break
            print("Goal city cannot be the same as starting city.")
        else:
            print(f"City not found. Available cities: {', '.join(cities)}")
    
    return cities, road_network, straight_line_distances, start, goal

def main():
    global straight_line_distances
    print("A* Search for Cities Shortest Path Problem")
    print("==========================================")
    
    cities, road_network, straight_line_distances, start, goal = get_user_input()
    
    print("\nGenerating road network graph...")
    draw_graph(road_network, start, goal)  # Draw initial graph without the path
    
    print("\nSearching for shortest path using A*...")
    start_time = time.time()
    path, total_distance, nodes_expanded = a_star_search(road_network, start, goal)
    end_time = time.time()
    
    if path:
        print(f"\nPath found! {' -> '.join(path)}")
        print(f"Total distance: {total_distance:.2f} units")
        print(f"Total nodes expanded: {nodes_expanded}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")
        print("\nStep-by-step path:")
        for i in range(len(path) - 1):
            dist = road_network[path[i]][path[i+1]]
            print(f"{path[i]} to {path[i+1]}: {dist:.2f} units")
        print("\nGenerating graph with shortest path...")
        draw_graph(road_network, start, goal, path)  # Draw graph with path highlighted
    else:
        print("\nNo path found! The goal city is unreachable from the start city.")

if __name__ == "__main__":
    main()