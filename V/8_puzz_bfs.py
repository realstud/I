import heapq
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.colors import LinearSegmentedColormap
import copy

class PuzzleNode:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
        
    def __lt__(self, other):
        return self.path_cost < other.path_cost
        
    def __eq__(self, other):
        return np.array_equal(self.state, other.state)
    
    def __hash__(self):
        return hash(str(self.state.flatten()))

def manhattan_distance(state, goal):
    """Calculate the Manhattan distance heuristic."""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:  # Skip the empty tile
                # Find where this number is in the goal state
                goal_pos = np.where(goal == state[i][j])
                goal_i, goal_j = goal_pos[0][0], goal_pos[1][0]
                # Calculate Manhattan distance
                distance += abs(i - goal_i) + abs(j - goal_j)
    return distance

def get_blank_position(state):
    """Find the position of the blank (0) in the puzzle."""
    pos = np.where(state == 0)
    return pos[0][0], pos[1][0]

def get_neighbors(node):
    """Generate all possible next states by moving the blank tile."""
    i, j = get_blank_position(node.state)
    neighbors = []
    moves = [('UP', -1, 0), ('DOWN', 1, 0), ('LEFT', 0, -1), ('RIGHT', 0, 1)]
    
    for move, di, dj in moves:
        new_i, new_j = i + di, j + dj
        if 0 <= new_i < 3 and 0 <= new_j < 3:  # Check if the move is valid
            new_state = node.state.copy()
            # Swap blank with the adjacent tile
            new_state[i, j], new_state[new_i, new_j] = new_state[new_i, new_j], new_state[i, j]
            neighbors.append(PuzzleNode(new_state, node, move, 0))
    
    return neighbors

def best_first_search(initial_state, goal_state):
    """Solve 8-puzzle using Best First Search with Manhattan distance heuristic."""
    initial_node = PuzzleNode(initial_state)
    if np.array_equal(initial_state, goal_state):
        return [initial_node], {}, []
    
    frontier = []
    # Priority is the heuristic value (Manhattan distance)
    heapq.heappush(frontier, (manhattan_distance(initial_state, goal_state), initial_node))
    
    explored = set()
    graph = {}  # For visualization
    
    while frontier:
        _, current_node = heapq.heappop(frontier)
        
        # Skip if we've already explored this state
        if hash(current_node) in explored:
            continue
        
        # Add to explored set
        explored.add(hash(current_node))
        
        # Generate all possible next states
        for neighbor in get_neighbors(current_node):
            if hash(neighbor) not in explored:
                # Calculate heuristic for this neighbor
                h = manhattan_distance(neighbor.state, goal_state)
                neighbor.path_cost = h
                
                # Add to frontier with priority = heuristic
                heapq.heappush(frontier, (h, neighbor))
                
                # Add to graph for visualization
                if hash(current_node) not in graph:
                    graph[hash(current_node)] = []
                graph[hash(current_node)].append(hash(neighbor))
                
                # Check if we've found the goal
                if np.array_equal(neighbor.state, goal_state):
                    # Reconstruct path
                    path = [neighbor]
                    parent = neighbor.parent
                    while parent:
                        path.append(parent)
                        parent = parent.parent
                    path.reverse()
                    
                    return path, graph, list(explored)
    
    return [], graph, list(explored)  # No solution found

def visualize_search_tree(path, graph, explored, initial_state, goal_state):
    """Visualize the search tree using NetworkX and Matplotlib."""
    G = nx.DiGraph()
    
    # Create node labels
    node_labels = {}
    
    # Add nodes and edges to the graph
    for parent, children in graph.items():
        if parent not in G:
            G.add_node(parent)
            
        for child in children:
            if child not in G:
                G.add_node(child)
            G.add_edge(parent, child)
    
    # Set up colors for nodes
    node_colors = []
    goal_hash = None
    
    # Find path node hashes
    path_hashes = set()
    for node in path:
        path_hashes.add(hash(node))
        if np.array_equal(node.state, goal_state):
            goal_hash = hash(node)
    
    # Setup positioning using hierarchical layout
    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    
    # Color the nodes
    for node in G.nodes:
        if node == hash(PuzzleNode(initial_state)):
            node_colors.append('green')  # Initial state
        elif node == goal_hash:
            node_colors.append('red')    # Goal state
        elif node in path_hashes:
            node_colors.append('yellow') # Path to goal
        else:
            node_colors.append('skyblue')   # Other explored nodes
    
    plt.figure(figsize=(15, 10))
    nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=500, arrows=True)
    plt.title("8-Puzzle Best First Search Tree")
    
    # Add legend
    legend_labels = {
        'green': 'Initial State',
        'red': 'Goal State',
        'yellow': 'Path to Goal',
        'skyblue': 'Explored Nodes'
    }
    
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', 
                               markerfacecolor=color, markersize=10) 
                    for color in legend_labels.keys()]
    
    plt.legend(legend_handles, legend_labels.values(), loc='upper right')
    
    plt.savefig('8puzzle_search_tree.png')
    plt.close()
    
    # Now create a second visualization that shows the actual puzzle states
    # for nodes along the solution path
    plt.figure(figsize=(15, 5))
    
    for i, node in enumerate(path):
        plt.subplot(1, len(path), i+1)
        plt.imshow(node.state, cmap='Pastel1')
        
        # Add the numbers on the grid
        for i in range(3):
            for j in range(3):
                if node.state[i, j] != 0:  # Skip the blank (0)
                    plt.text(j, i, str(int(node.state[i, j])),
                             ha="center", va="center", fontsize=20)
                else:
                    plt.text(j, i, " ", ha="center", va="center", fontsize=20)
        
        if i == 0:
            plt.title("Initial")
        elif i == len(path) - 1:
            plt.title("Goal")
        else:
            plt.title(f"Step {i}")
        
        plt.xticks([])
        plt.yticks([])
    
    plt.tight_layout()
    plt.savefig('8puzzle_solution_steps.png')
    plt.close()

def main():
    # Define the initial and goal states for the 8-puzzle
    initial_state = np.array([
        [2, 8, 3],
        [1, 6, 4],
        [7, 0, 5]
    ])
    
    goal_state = np.array([
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ])
    
    print("Solving 8-puzzle problem...")
    print("Initial state:")
    print(initial_state)
    print("Goal state:")
    print(goal_state)
    
    # Solve using Best First Search
    path, graph, explored = best_first_search(initial_state, goal_state)
    
    if path:
        print(f"Solution found in {len(path)-1} steps!")
        print(f"Nodes explored: {len(explored)}")
        
        # Visualize the search tree
        visualize_search_tree(path, graph, explored, initial_state, goal_state)
        
        # Print the solution path
        print("\nSolution path:")
        for i, node in enumerate(path):
            print(f"Step {i}:")
            print(node.state)
            if i < len(path) - 1:
                print(f"Action: {path[i+1].action}")
                print()
    else:
        print("No solution found!")

if __name__ == "__main__":
    main()