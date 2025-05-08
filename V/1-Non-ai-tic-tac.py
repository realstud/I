def print_board(board):
    for row in board:
        print(" | ".join(row))
    print()

def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != ' ':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != ' ':
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    return None

# Main function
def tic_tac_toe():
    board = [[' ' for _ in range(3)] for _ in range(3)]  # Empty board
    current_player = 'X'

    for _ in range(9):  # Maximum of 9 moves
        print_board(board)
        print(f"Player {current_player}'s turn")
        row = int(input("Enter row (0-2): "))
        col = int(input("Enter column (0-2): "))

        # Check if the cell is empty
        if board[row][col] == ' ':
            board[row][col] = current_player
        else:
            print("Cell already taken, try again.")
            continue

        # Check for a winner
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} wins!")
            return

        # Switch players
        current_player = 'O' if current_player == 'X' else 'X'

    # If no winner after 9 moves, it's a tie
    print_board(board)
    print("It's a tie!")

# Run the game
tic_tac_toe()
