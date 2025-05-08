import matplotlib.pyplot as plt
import numpy as np

def print_grid(ar):
    """Print the Sudoku grid in console (optional, kept for reference)."""
    for i in range(9):
        for j in range(9):
            print(ar[i][j], end=" ")
        print()

def display_grid(grid, title="Sudoku Grid"):
    """Display the Sudoku grid using Matplotlib."""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.matshow(np.zeros((9, 9)), cmap='Greys', alpha=0.3)  # Background
    
    # Add numbers
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                ax.text(j, i, str(grid[i][j]), va='center', ha='center', fontsize=14)
    
    # Draw 3x3 grid lines
    for i in range(10):
        if i % 3 == 0:
            ax.axhline(i - 0.5, color='black', linewidth=2)
            ax.axvline(i - 0.5, color='black', linewidth=2)
        else:
            ax.axhline(i - 0.5, color='gray', linewidth=0.5)
            ax.axvline(i - 0.5, color='gray', linewidth=0.5)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=16, pad=20)
    plt.show()

def find_empty_loc(ar, l):
    """Find an empty location (0) in the grid."""
    for row in range(9):
        for col in range(9):
            if ar[row][col] == 0:
                l[0] = row
                l[1] = col
                return True
    return False

def used_in_row(ar, row, num):
    """Check if number is used in the row."""
    for i in range(9):
        if ar[row][i] == num:
            return True
    return False

def used_in_col(ar, col, num):
    """Check if number is used in the column."""
    for i in range(9):
        if ar[i][col] == num:
            return True
    return False

def used_in_box(ar, row, col, num):
    """Check if number is used in the 3x3 box."""
    for i in range(3):
        for j in range(3):
            if ar[i + row][j + col] == num:
                return True
    return False

def check_loc_is_safe(ar, row, col, num):
    """Check if placing number at location is safe."""
    return (not used_in_row(ar, row, num) and
            not used_in_col(ar, col, num) and
            not used_in_box(ar, row - row % 3, col - col % 3, num))

def solve_sudoku(ar):
    """Solve the Sudoku puzzle using backtracking."""
    l = [0, 0]
    
    if not find_empty_loc(ar, l):
        return True  # Puzzle solved
    
    row, col = l[0], l[1]
    
    for num in range(1, 10):
        if check_loc_is_safe(ar, row, col, num):
            ar[row][col] = num
            
            if solve_sudoku(ar):
                return True
            
            ar[row][col] = 0  # Backtrack
    
    return False

def main():
    print("Enter the Sudoku puzzle (use 0 for empty cells):")
    grid = []
    for i in range(9):
        while True:
            try:
                row = list(map(int, input(f"Row {i+1}: ").strip().split()))
                if len(row) != 9:
                    print("Error: Each row must contain exactly 9 numbers.")
                    continue
                if all(0 <= x <= 9 for x in row):
                    grid.append(row)
                    break
                else:
                    print("Error: Numbers must be between 0 and 9.")
            except ValueError:
                print("Error: Please enter valid integers separated by spaces.")
    
    # Display the initial grid
    display_grid(grid, title="Unsolved Sudoku Puzzle")
    
    # Solve and display the result
    if solve_sudoku(grid):
        print("Solution found!")
        display_grid(grid, title="Solved Sudoku Puzzle")
    else:
        print("No solution exists")

if __name__ == "__main__":
    main()