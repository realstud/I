def generate_magic_square(n):
    if n % 2 == 0:
        print("Magic square generation works only for odd numbers!")
        return

    magic_square = [[0] * n for _ in range(n)]
    i, j = 0, n // 2

    for num in range(1, n * n + 1):
        magic_square[i][j] = num
        new_i = (i - 1) % n
        new_j = (j + 1) % n
        if magic_square[new_i][new_j] != 0:  # Collision
            i = (i + 1) % n
        else:
            i, j = new_i, new_j

    print(f"\nMagic Square (n = {n}):")
    for row in magic_square:
        print(" ".join(f"{num:2d}" for num in row))
    print()


def is_magic_square(matrix):
    n = len(matrix)
    magic_sum = sum(matrix[0])

    # Check rows
    for row in matrix:
        if sum(row) != magic_sum:
            return False

    # Check columns
    for col in range(n):
        if sum(matrix[row][col] for row in range(n)) != magic_sum:
            return False

    # Check diagonals
    if sum(matrix[i][i] for i in range(n)) != magic_sum or sum(matrix[i][n - i - 1] for i in range(n)) != magic_sum:
        return False

    return True


def menu():
    while True:
        print("\nMenu:")
        print("1. Generate Magic Square")
        print("2. Check if a Matrix is a Magic Square")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            n = int(input("Enter the size of the magic square (odd number): "))
            generate_magic_square(n)
        elif choice == "2":
            n = int(input("Enter the size of the matrix (n x n): "))
            print("Enter the matrix values row by row:")
            matrix = []
            for _ in range(n):
                row = list(map(int, input().split()))
                matrix.append(row)

            if is_magic_square(matrix):
                print("\nThe entered matrix is a Magic Square!")
            else:
                print("\nThe entered matrix is NOT a Magic Square!")
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the menu
menu()
