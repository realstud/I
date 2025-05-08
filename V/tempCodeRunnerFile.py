import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple, List, Dict, Optional, NamedTuple


class PuzzleState(NamedTuple):
    """Immutable representation of a puzzle state"""
    board: Tuple[Tuple[int, ...], ...]
    empty_pos: Tuple[int, int]

    @classmethod
    def from_array(cls, array: np.ndarray) -> 'PuzzleState':
        """Create PuzzleState from numpy array"""
        empty_i, empty_j = np.where(array == 0)
        empty_pos = (int(empty_i[0]), int(empty_j[0]))
        return cls(tuple(map(tuple, array)), empty_pos)

    def to_array(self) -> np.ndarray:
        """Convert to numpy array"""
        return np.array(self.board)


class TreeNode:
    """Represents a node in the puzzle search tree"""
    def __init__(self, state: PuzzleState, parent: Optional[int], depth: int, heuristic: int):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.heuristic = heuristic


class PuzzleHillClimbing:
    """8-Puzzle Solver using an expanded Hill Climbing approach"""

    def __init__(self, root_state: np.ndarray, goal_state: np.ndarray):
        """Initialize with the start and goal states"""
        self.goal_state = goal_state
        self.goal_state_tuple = tuple(map(tuple, goal_state))

        # Create goal position lookup for Manhattan heuristic
        self.goal_positions = {goal_state[i, j]: (i, j) for i in range(3) for j in range(3) if goal_state[i, j] != 0}

        # Initialize root node
        root = PuzzleState.from_array(root_state)
        self.nodes: Dict[int, TreeNode] = {
            0: TreeNode(state=root, parent=None, depth=0, heuristic=self._manhattan_distance(root))
        }
        self.edges: List[Tuple[int, int]] = []
        self.visited = {root}

    def _manhattan_distance(self, state: PuzzleState) -> int:
        """Calculate Manhattan distance heuristic"""
        return sum(
            abs(i - self.goal_positions[val][0]) + abs(j - self.goal_positions[val][1])
            for i in range(3) for j in range(3)
            if (val := state.board[i][j]) != 0
        )

    def _get_valid_moves(self, state: PuzzleState) -> List[PuzzleState]:
        """Get all valid moves from the current state"""
        valid_states = []
        i, j = state.empty_pos
        board = np.array(state.board)

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

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
        """Check if the given state is the goal state"""
        return state.board == self.goal_state_tuple

    def solve(self) -> str:
        """Solve the puzzle using Hill Climbing (expanding all heuristics)"""
        current_idx = 0

        while True:
            current_node = self.nodes[current_idx]
            if current_node.heuristic == 0:
                return "Goal state reached!"

            valid_moves = self._get_valid_moves(current_node.state)
            if not valid_moves:
                return "Stuck at local minimum!"

            # Expand all valid moves and add them to the tree
            for move in valid_moves:
                move_heuristic = self._manhattan_distance(move)
                new_idx = len(self.nodes)
                self.nodes[new_idx] = TreeNode(
                    state=move, parent=current_idx, depth=current_node.depth + 1, heuristic=move_heuristic
                )
                self.edges.append((current_idx, new_idx))
                self.visited.add(move)

            # Move to the best available state
            best_idx = min(
                (idx for idx in self.nodes if self.nodes[idx].parent == current_idx),
                key=lambda idx: self.nodes[idx].heuristic,
                default=None
            )

            if best_idx is None or self.nodes[best_idx].heuristic >= current_node.heuristic:
                return "Stuck at local minimum!"

            current_idx = best_idx  # Move to the best state

    def visualize(self) -> None:
        """Visualize the expanded search tree"""
        G = nx.DiGraph()
        node_labels = {}
        node_colors = []

        # Add nodes to the graph
        for idx, node in self.nodes.items():
            G.add_node(idx)
            node_labels[idx] = "\n".join(" ".join(map(str, row)) 
                                         for row in node.state.board)
            node_colors.append('#90EE90' if self.is_goal_state(node.state) else 'lightblue')

        # Add edges
        G.add_edges_from(self.edges)

        # Generate positions AFTER adding nodes
        positions = nx.spring_layout(G)

        plt.figure(figsize=(12, 8))
        nx.draw(G, positions, with_labels=True, labels=node_labels, 
                node_size=2500, node_color=node_colors, font_size=8)

        plt.title("8-Puzzle Hill Climbing Search (Expanded Heuristics)")
        plt.show()


def main() -> None:
    """Main function"""
    print("\n=== 8-Puzzle Hill Climbing Solver (Expanded Tree) ===")

    try:
        # Get initial state
        print("\nEnter initial state (9 space-separated integers 0-8)")
        print("Example: 1 2 3 4 0 5 6 7 8\n")
        initial_values = list(map(int, input("Enter initial state: ").strip().split()))

        # Get goal state
        print("\nEnter goal state (9 space-separated integers 0-8)")
        print("Example: 1 2 3 4 5 6 7 8 0\n")
        goal_values = list(map(int, input("Enter goal state: ").strip().split()))

        # Validate inputs
        for values in [initial_values, goal_values]:
            if len(values) != 9 or set(values) != set(range(9)):
                raise ValueError("Each state must contain numbers 0-8 exactly once")

        initial_state = np.array(initial_values).reshape(3, 3)
        goal_state = np.array(goal_values).reshape(3, 3)

        # Create and solve puzzle
        puzzle = PuzzleHillClimbing(initial_state, goal_state)

        print("\nSolving using Hill Climbing (Expanding All Moves)...")
        message = puzzle.solve()
        print(f"\nStatus: {message}")

        print("\nDisplaying visualization...")
        puzzle.visualize()

    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()
