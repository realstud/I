import matplotlib.pyplot as plt
import numpy as np

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
    
    def display_board(self, title="Tic Tac Toe"):
        """Display the Tic-Tac-Toe board using Matplotlib."""
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-0.5, 2.5)
        
        # Draw grid lines
        for i in range(1, 3):
            ax.axhline(i - 0.5, color='black', linewidth=2)
            ax.axvline(i - 0.5, color='black', linewidth=2)
        
        # Plot X's and O's
        for i in range(9):
            row, col = divmod(i, 3)
            if self.board[i] == 'X':
                ax.text(col, 2 - row, 'X', ha='center', va='center', fontsize=40, color='blue')
            elif self.board[i] == 'O':
                ax.text(col, 2 - row, 'O', ha='center', va='center', fontsize=40, color='red')
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(title, fontsize=16)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()
    
    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']
    
    def empty_squares(self):
        return ' ' in self.board
    
    def num_empty_squares(self):
        return self.board.count(' ')
    
    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False
    
    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        
        return False

def minimax(board, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
    if board.current_winner == 'X':
        return 1 * (board.num_empty_squares() + 1)
    elif board.current_winner == 'O':
        return -1 * (board.num_empty_squares() + 1)
    elif board.num_empty_squares() == 0:
        return 0
    
    if is_maximizing:
        max_eval = float('-inf')
        for move in board.available_moves():
            board.make_move(move, 'X')
            eval = minimax(board, depth + 1, False, alpha, beta)
            board.board[move] = ' '
            board.current_winner = None
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.available_moves():
            board.make_move(move, 'O')
            eval = minimax(board, depth + 1, True, alpha, beta)
            board.board[move] = ' '
            board.current_winner = None
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board):
    best_score = float('-inf')
    best_move = None
    
    for move in board.available_moves():
        board.make_move(move, 'X')
        score = minimax(board, 0, False)
        board.board[move] = ' '
        board.current_winner = None
        
        if score > best_score:
            best_score = score
            best_move = move
    
    return best_move

def play_game():
    tic_tac_toe = TicTacToe()
    
    print("Tic Tac Toe using Minimax with AI (X) vs Human (O)")
    print("Board positions are numbered 1-9, left to right, top to bottom.")
    tic_tac_toe.display_board(title="Initial Board")
    
    while tic_tac_toe.empty_squares():
        # Human player's move (O)
        human_move = None
        while human_move not in tic_tac_toe.available_moves():
            try:
                print("Available moves:", [i+1 for i in tic_tac_toe.available_moves()])
                human_move = int(input("Enter your move (1-9): ")) - 1
                if human_move not in tic_tac_toe.available_moves():
                    print("Invalid move. Try again.")
            except ValueError:
                print("Please enter a number between 1-9.")
        
        tic_tac_toe.make_move(human_move, 'O')
        tic_tac_toe.display_board(title="After Your Move (O)")
        
        if tic_tac_toe.current_winner:
            print("You win!")
            return
        
        if not tic_tac_toe.empty_squares():
            print("It's a tie!")
            return
        
        # AI's move (X)
        ai_move = find_best_move(tic_tac_toe)
        tic_tac_toe.make_move(ai_move, 'X')
        tic_tac_toe.display_board(title="After Dragon's Move (X)")
        
        if tic_tac_toe.current_winner:
            print("Dragon wins!")
            return

if __name__ == "__main__":
    play_game()