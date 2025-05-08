import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from copy import deepcopy

class MapColoringVisualizer:
    def __init__(self, regions, neighbors, colors):
        self.regions = regions
        self.neighbors = neighbors
        self.colors = colors
        self.assignments = {}
        self.steps = []
        self.current_step = 0
        
        # Generate positions for regions (for visualization)
        self.positions = self._generate_positions()
        
    def _generate_positions(self):
        """Generate positions for regions in a circle layout"""
        G = nx.Graph()
        for region in self.regions:
            G.add_node(region)
        for region, neighbors in self.neighbors.items():
            for neighbor in neighbors:
                G.add_edge(region, neighbor)
        
        # Use a spring layout for more natural-looking graph
        return nx.spring_layout(G, seed=42)
    
    def is_consistent(self, region, color):
        """Check if assigning color to region is consistent with current assignments"""
        for neighbor in self.neighbors.get(region, []):
            if neighbor in self.assignments and self.assignments[neighbor] == color:
                return False
        return True
    
    def select_unassigned_variable(self):
        """Select an unassigned region with most constraints"""
        unassigned = [r for r in self.regions if r not in self.assignments]
        if not unassigned:
            return None
        
        # Apply degree heuristic: choose the region with the most unassigned neighbors
        return max(unassigned, 
                   key=lambda r: sum(1 for n in self.neighbors.get(r, []) if n not in self.assignments))
    
    def order_domain_values(self, region):
        """Order colors by least constraining value heuristic"""
        # Simplified version - just return colors in original order
        return self.colors
    
    def backtrack(self):
        """Solve the map coloring problem with backtracking"""
        # Save current state for visualization
        self.steps.append(deepcopy(self.assignments))
        
        if len(self.assignments) == len(self.regions):
            return self.assignments
        
        region = self.select_unassigned_variable()
        if region is None:
            return self.assignments
        
        for color in self.order_domain_values(region):
            if self.is_consistent(region, color):
                self.assignments[region] = color
                
                # Save current state for visualization
                self.steps.append(deepcopy(self.assignments))
                
                result = self.backtrack()
                if result:
                    return result
                
                del self.assignments[region]
                
                # Save current state for visualization
                self.steps.append(deepcopy(self.assignments))
        
        return None
    
    def solve(self):
        """Solve the map coloring problem and save steps for visualization"""
        self.assignments = {}
        self.steps = [{}]  # Start with empty assignments
        result = self.backtrack()
        return result
    
    def draw_map(self, step=None):
        """Draw the map with current coloring at given step"""
        if step is not None:
            current_assignments = self.steps[step]
        else:
            current_assignments = self.assignments
            
        plt.figure(figsize=(12, 10))
        
        # Create a graph for visualization
        G = nx.Graph()
        for region in self.regions:
            G.add_node(region)
        for region, neighbors in self.neighbors.items():
            for neighbor in neighbors:
                G.add_edge(region, neighbor)
        
        # Draw edges (borders between regions)
        nx.draw_networkx_edges(G, self.positions, alpha=0.3, width=2)
        
        # Define color map
        color_map = {
            'red': '#FF6B6B', 
            'green': '#4ECDC4', 
            'blue': '#45B7D1', 
            'yellow': '#FED766',
            'purple': '#A65EEA',
            'orange': '#FF9A5A',
            'pink': '#FF7EB6'
        }
        
        # Create colors for nodes
        node_colors = []
        for region in self.regions:
            if region in current_assignments:
                color_name = current_assignments[region]
                node_colors.append(color_map.get(color_name.lower(), '#CCCCCC'))
            else:
                node_colors.append('#EEEEEE')  # Unassigned regions
        
        # Draw regions as nodes
        nx.draw_networkx_nodes(G, self.positions, node_size=3000, node_color=node_colors, 
                              edgecolors='black', linewidths=2)
        
        # Add labels to regions
        nx.draw_networkx_labels(G, self.positions, font_size=12, font_weight='bold')
        
        # Add a title showing current step
        if step is not None:
            plt.title(f"Map Coloring - Step {step}/{len(self.steps)-1}", fontsize=16)
        else:
            plt.title("Final Map Coloring Solution", fontsize=16)
            
        # Add a legend for colors
        handles = []
        labels = []
        for color_name, color_hex in color_map.items():
            if color_name in [c.lower() for c in self.colors]:
                handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color_hex, 
                                         markersize=15, label=color_name.capitalize()))
                labels.append(color_name.capitalize())
        
        plt.legend(handles=handles, labels=labels, loc='upper right')
        
        plt.axis('off')
        plt.tight_layout()
        return plt

    def animate_solution(self, show_steps=True):
        """Animate the solution steps"""
        if not self.steps:
            print("No solution steps to animate. Run solve() first.")
            return
        
        total_steps = len(self.steps)
        
        if show_steps:
            # Show just a few key steps if there are too many
            if total_steps > 10:
                step_indices = np.linspace(0, total_steps-1, 10, dtype=int)
            else:
                step_indices = range(total_steps)
            
            for i in step_indices:
                plt = self.draw_map(i)
                plt.show()
        
        # Show final solution
        plt = self.draw_map()
        plt.show()


def get_regions_input():
    print("Enter the names of all regions, one per line.")
    print("Enter an empty line when done.")
    
    regions = []
    while True:
        region = input("Region name (or empty line to finish): ").strip()
        if not region:
            if not regions:
                print("Error: At least one region is required.")
                continue
            break
        
        if region in regions:
            print("Error: Region names must be unique.")
            continue
        
        regions.append(region)
    
    return regions

def get_neighbors_input(regions):
    neighbors = {region: [] for region in regions}
    
    print("\nFor each region, enter its neighboring regions.")
    print("Enter multiple neighbors separated by commas, or leave empty if none.")
    
    for region in regions:
        while True:
            neighbor_input = input(f"Neighbors for {region}: ").strip()
            
            if not neighbor_input:
                break
            
            neighbor_list = [n.strip() for n in neighbor_input.split(',')]
            
            # Validate neighbors
            valid = True
            for n in neighbor_list:
                if n not in regions:
                    print(f"Error: {n} is not a valid region.")
                    valid = False
                elif n == region:
                    print(f"Error: {region} cannot be a neighbor of itself.")
                    valid = False
            
            if valid:
                neighbors[region] = neighbor_list
                break
    
    # Ensure symmetry in neighbor relationships
    for region, region_neighbors in list(neighbors.items()):
        for neighbor in region_neighbors:
            if region not in neighbors[neighbor]:
                print(f"Adding {region} as a neighbor of {neighbor} for consistency.")
                neighbors[neighbor].append(region)
    
    return neighbors

def get_colors_input():
    print("\nEnter the available colors, one per line.")
    print("Enter an empty line when done.")
    
    colors = []
    while True:
        color = input("Color (or empty line to finish): ").strip()
        if not color:
            if len(colors) < 2:
                print("Error: At least two colors are required.")
                continue
            break
        
        if color in colors:
            print("Error: Color names must be unique.")
            continue
        
        colors.append(color)
    
    return colors

def main():
    print("Map Coloring Problem Visualizer")
    print("-" * 30)
    
    print("\nFirst, let's set up the map:")
    regions = get_regions_input()
    neighbors = get_neighbors_input(regions)
    colors = get_colors_input()
    
    # Create visualizer
    visualizer = MapColoringVisualizer(regions, neighbors, colors)
    
    print("\nSolving the map coloring problem...")
    solution = visualizer.solve()
    
    if solution:
        print("\nSolution found:")
        for region, color in solution.items():
            print(f"{region}: {color}")
        
        print(f"\nMinimum colors needed: {len(set(solution.values()))}")
        
        # Ask if user wants to visualize
        show_viz = input("\nShow visualization? (y/n): ").strip().lower()
        if show_viz == 'y':
            print("\nShowing the final colored map...")
            visualizer.draw_map().show()
            
            show_steps = input("\nShow solution steps? (y/n): ").strip().lower()
            if show_steps == 'y':
                print("\nAnimating solution steps...")
                visualizer.animate_solution(show_steps=True)
    else:
        print("No solution found for the given map with these colors.")

if __name__ == "__main__":
    main()