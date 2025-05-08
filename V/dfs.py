from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import math

def is_goal_state(state, z):
    return state[0] == z or state[1] == z

def generate_next_states(state, max_x, max_y):
    x, y = state
    return [
        (max_x, y),  # Fill jug X
        (x, max_y),  # Fill jug Y
        (0, y),      # Empty jug X
        (x, 0),      # Empty jug Y
        (x - min(x, max_y - y), y + min(x, max_y - y)),  # Pour X -> Y
        (x + min(y, max_x - x), y - min(y, max_x - x))   # Pour Y -> X
    ]

def calculate_tree_positions(graph, root, width=1., vert_gap=0.4, vert_loc=0, xcenter=0.5,
                           pos=None, parent=None, visited=None):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    if visited is None:
        visited = set()
        
    visited.add(root)
    children = [n for n in graph.neighbors(root) if n not in visited]
    if len(children) != 0:
        dx = width / len(children)
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = calculate_tree_positions(graph, child, width=dx, vert_gap=vert_gap,
                                        vert_loc=vert_loc-vert_gap, xcenter=nextx,
                                        pos=pos, parent=root, visited=visited)
    return pos

def draw_tree(graph, path=None):
    plt.figure(figsize=(15, 10))
    
    # Calculate positions based on tree structure
    root = (0, 0)  # Starting state
    pos = calculate_tree_positions(graph, root, width=2., vert_gap=0.3)
    
    # Draw edges
    nx.draw_networkx_edges(graph, pos, edge_color='gray', arrows=True,
                          arrowsize=20, arrowstyle='->', connectionstyle='arc3,rad=0.2')
    
    # Color nodes based on their depth
    depths = nx.shortest_path_length(graph, root)
    max_depth = max(depths.values())
    node_colors = [plt.cm.viridis(depths[node]/max_depth) for node in graph.nodes()]
    
    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, 
                          node_size=2000, node_shape='o')
    
    # Draw labels
    labels = {node: f'({node[0]},{node[1]})' for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels, font_size=10)
    
    # Highlight solution path
    if path:
        path_edges = list(zip(path[:-1], path[1:]))
        nx.draw_networkx_edges(graph, pos, edgelist=path_edges, 
                             edge_color='red', width=2,
                             arrows=True, arrowsize=20,
                             arrowstyle='->', connectionstyle='arc3,rad=0.2')
        nx.draw_networkx_nodes(graph, pos, nodelist=path,
                             node_color='lightgreen', 
                             node_size=2200)
    
    plt.title("Water Jug Problem - Tree Visualization", pad=20, size=16)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def dfs_water_jug(x, y, z):
    if z > max(x, y):
        print("Impossible to measure this amount.")
        return
    
    stack = [(0, 0)]
    visited = set()
    parent = {}
    graph = nx.DiGraph()
    
    # Initialize the starting node
    graph.add_node((0, 0))
    
    while stack:
        state = stack.pop()
        
        if state not in visited:
            visited.add(state)
            
            if is_goal_state(state, z):
                path = []
                current = state
                while current is not None:
                    path.append(current)
                    current = parent.get(current)
                path = path[::-1]
                
                print("\nSolution path (DFS):", path)
                print("\nSteps to solve:")
                for i in range(len(path)-1):
                    print(f"Step {i+1}: From {path[i]} to {path[i+1]}")
                
                draw_tree(graph, path)
                return
            
            next_states = generate_next_states(state, x, y)
            for next_state in reversed(next_states):
                if next_state not in visited:
                    stack.append(next_state)
                    if next_state not in parent:  # Only add edge if not already in tree
                        parent[next_state] = state
                        graph.add_node(next_state)
                        graph.add_edge(state, next_state)
    
    print("No solution found (DFS).")
    draw_tree(graph)

def main():
    print("Water Jug Problem Solver using DFS")
    print("----------------------------------")
    
    while True:
        try:
            x = int(input("\nEnter capacity of jug X: "))
            y = int(input("Enter capacity of jug Y: "))
            z = int(input("Enter target amount Z: "))
            
            if x <= 0 or y <= 0 or z < 0:
                print("Please enter positive numbers (target can be 0)")
                continue
                
            print(f"\nSolving for jugs with capacities {x}L and {y}L to measure {z}L...")
            dfs_water_jug(x, y, z)
            
            choice = input("\nWould you like to solve another problem? (yes/no): ").lower()
            if choice not in ['yes', 'y']:
                print("Thank you for using the Water Jug Problem Solver!")
                break
                
        except ValueError:
            print("Please enter valid numbers.")

if __name__ == "__main__":
    main()