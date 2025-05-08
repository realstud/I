import heapq
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

class PuzzleSolver:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
    
    def heuristic(self, state):
        """Calculate the heuristic value (number of misplaced tiles)"""
        return sum(1 for i in range(9) if state[i] != self.goal[i] and state[i] != 0)
    
    def get_neighbors(self, state):
        """Generate possible moves by swapping the empty tile (0) with its neighbors"""
        neighbors = []
        idx = state.index(0)
        moves = {
            0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
            3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
            6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
        }
        
        for move in moves[idx]:
            new_state = list(state)
            new_state[idx], new_state[move] = new_state[move], new_state[idx]
            neighbors.append(tuple(new_state))
        
        return neighbors
    
    def a_star_search(self):
        """A* Search Algorithm for 8-puzzle"""
        priority_queue = []
        heapq.heappush(priority_queue, (self.heuristic(self.start), 0, self.start, "Start"))
        visited = set()
        parent = {self.start: (None, "Start")}
        g_scores = {self.start: 0}
        
        solution_path = []
        heuristic_values = []
        graph = nx.DiGraph()
        
        graph.add_node(self.start, heuristic=self.heuristic(self.start))
        
        while priority_queue:
            f_score, g_score, current, direction = heapq.heappop(priority_queue)
            if current in visited:
                continue
                
            visited.add(current)
            h_score = self.heuristic(current)
            heuristic_values.append(h_score)
            
            if current == self.goal:
                path = []
                while current:
                    path.append((current, parent[current][1], self.heuristic(current), g_scores[current]))
                    current = parent[current][0]
                solution_path = path[::-1]
                
                self.plot_tree(graph, solution_path, heuristic_values, g_scores)
                return solution_path, heuristic_values
            
            for neighbor in self.get_neighbors(current):
                if neighbor in visited:
                    continue
                    
                tentative_g_score = g_scores[current] + 1
                
                if neighbor not in g_scores or tentative_g_score < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor)
                    heapq.heappush(priority_queue, (f_score, tentative_g_score, neighbor, direction))
                    parent[neighbor] = (current, direction)
                    
                    if neighbor not in graph.nodes:
                        graph.add_edge(current, neighbor)
                        graph.add_node(neighbor, heuristic=self.heuristic(neighbor))
        
        return None, heuristic_values

    @staticmethod
    def get_input():
        """Get user input for 8-puzzle initial and goal state in matrix form"""
        print("Enter the 8-puzzle initial state row by row (use 0 for blank, space-separated):")
        start = tuple(int(num) for _ in range(3) for num in input().split())
        print("Enter the 8-puzzle goal state row by row (use 0 for blank, space-separated):")
        goal = tuple(int(num) for _ in range(3) for num in input().split())
        return start, goal
    
    def display_state(self, state, direction, heuristic_value, g_score, step_num):
        """Display the puzzle state and info in a boxed structure"""
        print(f"+{'-' * 31}+")
        print(f"| Step {step_num}: {direction:<16} |")
        print(f"+{'-' * 31}+")
        for i in range(0, 9, 3):
            print(f"| {state[i] if state[i] != 0 else ' '} | {state[i+1] if state[i+1] != 0 else ' '} | {state[i+2] if state[i+2] != 0 else ' '} |")
            print(f"+{'-' * 7}+{'-' * 7}+{'-' * 7}+")
        print(f"| Heuristic: {heuristic_value:<3}  Cost (g): {g_score:<3}  f = {heuristic_value + g_score:<3} |")
        print(f"+{'-' * 31}+\n")

    def plot_tree(self, graph, solution_path, heuristic_values, g_scores):
        """Visualize the puzzle search tree with matrix representation in a hierarchical layout"""
        fig, ax = plt.subplots(figsize=(15, 12))
        
        # Calculate positions based on hierarchy (g_score as y-level)
        pos = {}
        level_counts = {}  # Track number of nodes at each level
        
        # Assign initial positions
        for node in graph.nodes:
            level = g_scores[node]  # Use g_score as the vertical level
            if level not in level_counts:
                level_counts[level] = 0
            level_counts[level] += 1
            # Initial x-position based on order of appearance at this level
            x_pos = (level_counts[level] - 1) * 0.5  # Simple spacing
            pos[node] = (x_pos, -level)  # Negative y to grow downward
        
        # Adjust x-positions to avoid overlap
        for level in level_counts:
            nodes_at_level = [n for n in graph.nodes if g_scores[n] == level]
            width = max(1, (level_counts[level] - 1) * 0.5)  # Minimum width of 1
            for i, node in enumerate(nodes_at_level):
                pos[node] = (i * width / max(1, level_counts[level] - 1) - width / 2, -level)

        # Draw edges
        nx.draw_networkx_edges(graph, pos, ax=ax, arrows=True, alpha=0.6)
        
        # Highlight solution path
        solution_nodes = [step[0] for step in solution_path]
        edges = [(solution_nodes[i], solution_nodes[i+1]) for i in range(len(solution_nodes) - 1)]
        nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2, ax=ax)

        # Draw nodes as matrices
        node_size = 0.3
        for node, (x, y) in pos.items():
            matrix = np.array(node).reshape(3, 3)
            matrix_display = np.where(matrix == 0, '', matrix)
            
            rect = Rectangle((x - node_size/2, y - node_size/2), node_size, node_size, 
                           facecolor='skyblue', alpha=0.6)
            ax.add_patch(rect)
            
            for i in range(3):
                for j in range(3):
                    ax.text(x - node_size/2 + j * node_size/3 + node_size/6,
                           y - node_size/2 + (2 - i) * node_size/3 + node_size/6,
                           str(matrix_display[i, j]),
                           ha='center', va='center', fontsize=8)
            
            ax.text(x, y - node_size/2 - 0.05, f'H: {graph.nodes[node]["heuristic"]} g: {g_scores[node]}',
                   ha='center', va='top', fontsize=8, color='black')

        plt.title("8-Puzzle State Space Tree (A* Search) - Hierarchical Layout")
        ax.set_aspect('equal')
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    start, goal = PuzzleSolver.get_input()
    if len(start) != 9 or len(goal) != 9:
        print("Invalid input! Please enter exactly 9 numbers.")
    else:
        solver = PuzzleSolver(start, goal)
        result, heuristic_values = solver.a_star_search()
        if result:
            print("Solution found in steps:")
            for i, (step, move_direction, heuristic_value, g_score) in enumerate(result, 1):
                solver.display_state(step, move_direction, heuristic_value, g_score, i)
            print(f"Total moves: {len(result) - 1}")
        else:
            print("No solution found!")