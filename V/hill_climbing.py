import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, List, Dict, Optional, NamedTuple
from collections import defaultdict

class PuzzleState(NamedTuple):
    board: Tuple[Tuple[int, ...], ...]
    empty_pos: Tuple[int, int]

    @classmethod
    def from_array(cls, array: np.ndarray) -> 'PuzzleState':
        empty_i, empty_j = np.where(array == 0)
        empty_pos = (int(empty_i[0]), int(empty_j[0]))
        return cls(tuple(map(tuple, array)), empty_pos)

    def to_array(self) -> np.ndarray:
        return np.array(self.board)

class TreeNode:
    def __init__(self, state: PuzzleState, parent: Optional[int], heuristic: int):
        self.state = state
        self.parent = parent
        self.heuristic = heuristic
        self.left_child = None
        self.right_child = None

class PuzzleHillClimbing:
    def __init__(self, root_state: np.ndarray, goal_state: np.ndarray):
        self.goal_state = goal_state
        self.goal_state_tuple = tuple(map(tuple, goal_state))
        self.goal_positions = {
            goal_state[i, j]: (i, j) 
            for i in range(3) for j in range(3) if goal_state[i, j] != 0
        }
        root = PuzzleState.from_array(root_state)
        self.nodes: Dict[int, TreeNode] = {
            0: TreeNode(state=root, parent=None, heuristic=self._manhattan_distance(root))
        }
        self.edges: List[Tuple[int, int]] = []
        self.visited = {root}
        self.levels = defaultdict(list)  # Store nodes by level for binary tree layout
        self.levels[0] = [0]  # Root node at level 0

    def _manhattan_distance(self, state: PuzzleState) -> int:
        return sum(
            abs(i - self.goal_positions[val][0]) + abs(j - self.goal_positions[val][1])
            for i in range(3) for j in range(3) if (val := state.board[i][j]) != 0
        )

    def _get_valid_moves(self, state: PuzzleState) -> List[PuzzleState]:
        valid_states = []
        i, j = state.empty_pos
        board = np.array(state.board)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for di, dj in moves:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                board[i, j], board[new_i, new_j] = board[new_i, new_j], board[i, j]
                new_state = PuzzleState.from_array(board)
                if new_state not in self.visited:
                    valid_states.append(new_state)
                board[i, j], board[new_i, new_j] = board[new_i, new_j], board[i, j]
        return valid_states

    def is_goal_state(self, state: PuzzleState) -> bool:
        return state.board == self.goal_state_tuple

    def solve(self) -> str:
        current_idx = 0
        current_level = 0
        
        while True:
            current_node = self.nodes[current_idx]
            if current_node.heuristic == 0:
                return "Goal state reached!"

            valid_moves = self._get_valid_moves(current_node.state)
            if not valid_moves:
                return "Stuck at local minimum!"

            # Organize nodes in binary tree format
            move_count = 0
            for move in valid_moves[:2]:  # Limit to 2 children for binary tree
                move_heuristic = self._manhattan_distance(move)
                new_idx = len(self.nodes)
                new_node = TreeNode(state=move, parent=current_idx, heuristic=move_heuristic)
                self.nodes[new_idx] = new_node
                self.edges.append((current_idx, new_idx))
                self.visited.add(move)
                
                # Assign as left or right child
                if move_count == 0:
                    self.nodes[current_idx].left_child = new_idx
                else:
                    self.nodes[current_idx].right_child = new_idx
                
                self.levels[current_level + 1].append(new_idx)
                move_count += 1

            best_idx = min(
                (idx for idx in self.nodes if self.nodes[idx].parent == current_idx),
                key=lambda idx: self.nodes[idx].heuristic, 
                default=None
            )

            if best_idx is None or self.nodes[best_idx].heuristic >= current_node.heuristic:
                return "Stuck at local minimum!"
            
            current_idx = best_idx
            current_level += 1

    def visualize(self) -> None:
        G = nx.Graph()
        node_labels = {}
        node_colors = []
        pos = {}
    
        # Calculate positions for binary tree layout
        max_level = max(self.levels.keys())
        for level in range(max_level + 1):
            nodes_at_level = self.levels[level]
            level_width = 2 ** level
            x_spacing = 2.0 / (level_width + 1)  # Increase spacing for better visibility
            
            for i, node_idx in enumerate(nodes_at_level):
                x_pos = (i + 1) * x_spacing - 1  # Center the tree
                y_pos = -level  # Lower levels are further down
                pos[node_idx] = (x_pos, y_pos)
                
                G.add_node(node_idx)
                node_labels[node_idx] = "\n".join(" ".join(map(str, row)) 
                                                    for row in self.nodes[node_idx].state.board)
                node_colors.append('#90EE90' if self.is_goal_state(self.nodes[node_idx].state) 
                                   else 'lightblue')

        # Add edges
        for node_idx in self.nodes:
            node = self.nodes[node_idx]
            if node.left_child is not None:
                G.add_edge(node_idx, node.left_child)
            if node.right_child is not None:
                G.add_edge(node_idx, node.right_child)

        plt.figure(figsize=(15, 10))
        nx.draw(G, pos=pos, with_labels=True, labels=node_labels,
                node_size=2500, node_color=node_colors, font_size=8,
                edge_color="gray")
        plt.title("8-Puzzle Binary Tree Search", pad=20)
        
        # Use subplots_adjust for manual adjustments
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  # Adjust these values as needed
        plt.axis('off')  # Turn off the axis
        plt.show()

def main() -> None:
    print("\n=== 8-Puzzle Binary Tree Solver ===")
    try:
        print("\nEnter initial state (9 space-separated integers 0-8)")
        print("Example: 1 2 3 4 0 5 6 7 8\n")
        initial_values = list(map(int, input("Enter initial state: ").strip().split()))

        print("\nEnter goal state (9 space-separated integers 0-8)")
        print("Example: 1 2 3 4 5 6 7 8 0\n")
        goal_values = list(map(int, input("Enter goal state: ").strip().split()))

        for values in [initial_values, goal_values]:
            if len(values) != 9 or set(values) != set(range(9)):
                raise ValueError("Each state must contain numbers 0-8 exactly once")

        initial_state = np.array(initial_values).reshape(3, 3)
        goal_state = np.array(goal_values).reshape(3, 3)
        puzzle = PuzzleHillClimbing(initial_state, goal_state)

        print("\nSolving using Binary Tree Search...")
        message = puzzle.solve()
        print(f"\nStatus: {message}")
        print("\nDisplaying visualization...")
        puzzle.visualize()

    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()