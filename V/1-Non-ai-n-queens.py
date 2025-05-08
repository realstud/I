def is_safe(board, row, col, n):
    # Check if a queen can be placed at this spot
    
    # Check the row to the left
    for j in range(col):
        if board[row][j] == 'Q':
            return False
    
    # Check upper diagonal to the left
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 'Q':
            return False
    
    # Check lower diagonal to the left
    for i, j in zip(range(row, n), range(col, -1, -1)):
        if board[i][j] == 'Q':
            return False
    
    return True

def solve_nqueens(n): 
    # Create an empty chess board
    board = [['.' for x in range(n)] for y in range(n)]
    
    def solve_board(col):
        # If we placed all queens, we're done
        if col >= n:
            return True
        
        # Try placing a queen in each row of this column
        for row in range(n):
            if is_safe(board, row, col, n):
                # Place the queen
                board[row][col] = 'Q'
                
                # increment to solve for the rest of the columns
                if solve_board(col + 1):
                    return True
                
                # Backtrack: remove the queen
                board[row][col] = '.'
        
        return False
    
    # first column
    if solve_board(0):
        # Print the solution
        for row in board:
            print(' '.join(row))
    else:
        print("No solution exists")

# Get user input for n
try:
    n = int(input("Enter the number of queens (n): "))
    if n <= 0:
        print("Please enter a positive integer.")
    else:
        print(f"\nSolving {n}-Queens problem...\n")
        solve_nqueens(n)
except ValueError:
    print("Invalid input. Please enter a valid integer.")