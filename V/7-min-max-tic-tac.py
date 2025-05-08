import math 
# Initial board 
board = [' ' for _ in range(9)] 
 
def print_board(board): 
    for row in [board[i*3:(i+1)*3] for i in range(3)]: 
        print('| ' + ' | '.join(row) + ' |') 
 
def is_winner(board, player): 
    win_cond = [ 
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows 
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns 
        [0, 4, 8], [2, 4, 6]              # Diagonals 
    ] 
    return any(all(board[i] == player for i in cond) for cond in win_cond) 
 
def is_board_full(board): 
    return ' ' not in board 
 
def get_available_moves(board): 
    return [i for i, spot in enumerate(board) if spot == ' '] 
 
# Minimax algorithm 
def minimax(board, depth, is_maximizing): 
    if is_winner(board, 'X'): 
        return 1 
    if is_winner(board, 'O'): 
        return -1 
    if is_board_full(board): 
        return 0 
 
    if is_maximizing: 
        best_score = -math.inf 
        for move in get_available_moves(board): 
            board[move] = 'X' 
            score = minimax(board, depth + 1, False) 
            board[move] = ' ' 
            best_score = max(score, best_score) 
        return best_score 
    else: 
        best_score = math.inf 
        for move in get_available_moves(board): 
            board[move] = 'O' 
            score = minimax(board, depth + 1, True) 
            board[move] = ' ' 
            best_score = min(score, best_score) 
        return best_score 
 
# AI move 
def best_move(): 
    best_score = -math.inf 
    move = None 
    for i in get_available_moves(board): 
        board[i] = 'X' 
        score = minimax(board, 0, False) 
        board[i] = ' ' 
        if score > best_score: 
            best_score = score 
            move = i 
    return move 
 
# Game loop 
def play_game(): 
    print("Welcome to Tic Tac Toe!") 
    print_board(board) 
 
    while True: 
        # Human move 
        human_move = int(input("Enter your move (1-9): ")) - 1 
        if board[human_move] != ' ': 
            print("Invalid move! Try again.") 
            continue 
        board[human_move] = 'O' 
        print_board(board) 
 
        if is_winner(board, 'O'): 
            print("You win!") 
            break 
        if is_board_full(board): 
            print("It's a draw!") 
            break 
 
        # AI move 
        ai_move = best_move() 
        board[ai_move] = 'X' 
        print("AI chose position", ai_move + 1) 
        print_board(board) 
 
        if is_winner(board, 'X'): 
            print("AI wins!") 
            break 
        if is_board_full(board): 
            print("It's a draw!") 
            break 
 
# Run the game 
if __name__ == "__main__": 
    play_game() 