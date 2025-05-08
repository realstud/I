import numpy as np

def play_tic_tac_toe():
    def print_board(board):
        for row in board:
            print(" | ".join(row))
            print("-" * 5)

    def check_winner(board):
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != " ":
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != " ":
                return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != " ":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != " ":
            return board[0][2]
        return None

    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    moves = 0

    while moves < 9:
        print_board(board)
        print(f"Player {current_player}, make your move (row and column: 1-3): ")
        try:
            row, col = map(int, input().split())
            if not (1 <= row <= 3 and 1 <= col <= 3):
                print("Row and column must be between 1 and 3. Try again!")
                continue
            if board[row - 1][col - 1] != " ":
                print("Cell already taken. Try again!")
                continue
            board[row - 1][col - 1] = current_player
            moves += 1

            winner = check_winner(board)
            if winner:
                print_board(board)
                print(f"Player {winner} wins!")
                return
            current_player = "O" if current_player == "X" else "X"
        except (ValueError, IndexError):
            print("Invalid input. Please enter row and column separated by a space.")

    print_board(board)
    print("It's a draw!")

def solve_n_queens():
    def print_solution(board):
        for row in board:
            print(" ".join("Q" if cell else "." for cell in row))
        print()

    def is_safe(board, row, col):
        for i in range(col):
            if board[row][i]:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j]:
                return False
        for i, j in zip(range(row, len(board)), range(col, -1, -1)):
            if board[i][j]:
                return False
        return True

    def solve(board, col):
        if col >= len(board):
            print_solution(board)
            return True
        res = False
        for i in range(len(board)):
            if is_safe(board, i, col):
                board[i][col] = True
                res = solve(board, col + 1) or res
                board[i][col] = False
        return res

    try:
        n = int(input("Enter the size of the chessboard (N): "))
        if n <= 0:
            print("N must be a positive integer.")
            return
        board = [[False] * n for _ in range(n)]
        if not solve(board, 0):
            print("No solution exists.")
    except ValueError:
        print("Invalid input. Please enter a positive integer.")

def generate_odd_magic_square(n):
    magic_square = np.zeros((n, n), dtype=int)
    i, j = 0, n // 2
    for num in range(1, n * n + 1):
        magic_square[i][j] = num
        i -= 1
        j += 1
        if num % n == 0:
            i += 2
            j -= 1
        elif i < 0:
            i = n - 1
        elif j == n:
            j = 0
    return magic_square

def generate_even_magic_square(n):
    if n % 2 != 0 or n < 4:
        raise ValueError("This function is for even numbers >= 4 only")
    square = [[0 for _ in range(n)] for _ in range(n)]
    count = 1
    for i in range(n):
        for j in range(n):
            square[i][j] = count
            count += 1
    if n == 4:
        positions_to_swap = [
            (0, 0), (0, 3), (1, 1), (1, 2),
            (2, 1), (2, 2), (3, 0), (3, 3)
        ]
        for i, j in positions_to_swap:
            square[i][j] = n * n + 1 - square[i][j]
    else:
        for i in range(0, n, 4):
            for j in range(0, n, 4):
                for k in range(4):
                    for l in range(4):
                        if (k in [0, 3] and l in [0, 3]) or (k in [1, 2] and l in [1, 2]):
                            square[i+k][j+l] = n * n + 1 - square[i+k][j+l]
    return square

def is_magic_square(matrix):
    size = len(matrix)
    magic_sum = sum(matrix[0])
    for row in matrix:
        if sum(row) != magic_sum:
            return False
    for col in range(size):
        if sum(matrix[row][col] for row in range(size)) != magic_sum:
            return False
    if sum(matrix[i][i] for i in range(size)) != magic_sum:
        return False
    if sum(matrix[i][size - 1 - i] for i in range(size)) != magic_sum:
        return False
    return True

def print_magic_square(square):
    n = len(square)
    magic_sum = n * (n * n + 1) // 2
    print(f"\nMagic Square of size {n}x{n} (Sum should be {magic_sum}):")
    max_width = len(str(n * n))
    for row in square:
        print(" ".join(str(x).rjust(max_width) for x in row))
    print("\nVerification:")
    print("Row sums:", [sum(row) for row in square])
    print("Column sums:", [sum(square[i][j] for i in range(n)) for j in range(n)])
    print("Main diagonal sum:", sum(square[i][i] for i in range(n)))
    print("Other diagonal sum:", sum(square[i][n-1-i] for i in range(n)))
    all_numbers = sorted([num for row in square for num in row])
    if all_numbers == list(range(1, n * n + 1)):
        print("All numbers from 1 to", n*n, "are present exactly once.")
    else:
        print("Warning: Not all numbers from 1 to", n*n, "are present exactly once!")

def magic_square():
    print("1. Check if a matrix is a magic square")
    print("2. Generate a magic square")
    choice = input("Enter your choice: ")
    if choice == "1":
        try:
            n = int(input("Enter the size of the square matrix: "))
            if n <= 0:
                print("Size must be a positive integer.")
                return
            print("Enter the matrix row by row:")
            matrix = [list(map(int, input().split())) for _ in range(n)]
            if len(matrix) != n or any(len(row) != n for row in matrix):
                print("Invalid matrix dimensions.")
                return
            if is_magic_square(matrix):
                print("The entered matrix is a magic square.")
            else:
                print("The entered matrix is NOT a magic square.")
        except ValueError:
            print("Invalid input. Please enter valid integers.")
    elif choice == "2":
        try:
            n = int(input("Enter the size of the magic square: "))
            if n <= 0:
                print("Size must be a positive integer.")
                return
            if n % 2 == 1:
                square = generate_odd_magic_square(n)
                print_magic_square(square)
            else:
                if n < 4:
                    print("Even-sized magic squares must be 4x4 or larger.")
                    return
                square = generate_even_magic_square(n)
                print_magic_square(square)
        except ValueError as e:
            print("Error:", str(e))
    else:
        print("Invalid choice.")

def main():
    while True:
        print("\nMenu:")
        print("1. Tic Tac Toe")
        print("2. N Queens")
        print("3. Magic Square")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            play_tic_tac_toe()
        elif choice == "2":
            solve_n_queens()
        elif choice == "3":
            magic_square()
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()