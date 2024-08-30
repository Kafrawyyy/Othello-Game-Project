import tkinter as tk
import numpy as np
import copy
from tkinter import messagebox


class GameController:
    def __init__(self, game, gui):
        self.player_color = "Black"  # Initializing player color
        self.game = game  # Initializing the game object
        self.gui = gui  # Initializing the GUI object
        self.current_player = -1  # Start with player -1 (Black)

    def switch_player(self):
        self.current_player = -self.current_player  # Switch between players (1 and -1)
        self.player_color = "White" if self.current_player == 1 else "Black"  # Change player color

    def player_move(self, row, col):
        # Check if the move is valid and update the game board
        if (row, col) in self.game.get_valid_moves():
            self.game.make_move(row, col)  # Make the move
            self.gui.update_ui()  # Update the GUI

            # Check if the game is over
            if self.game.is_game_over():
                self.end_game()  # End the game
            else:
                # AI's turn to move
                self.ai_move()  # AI makes its move
        elif len(self.game.get_valid_moves()) == 0:
            self.switch_player()  # Switch player if no valid moves

    def ai_move(self):
        messagebox.showinfo("AI Turn", "AI is thinking...")  # Display AI turn message

        if len(self.game.get_valid_moves()) != 0:
            best_move = get_best_move(self.game, self.gui.ai_depth)  # Get the best move from AI

            self.game.make_move(best_move[0], best_move[1])  # Make the AI move
            self.gui.update_ui()  # Update the GUI

            # Switch to the next player
            self.switch_player()  # Switch player

            # Check if the game is over
            if self.game.is_game_over():
                self.end_game()  # End the game
        else:
            print("Ai has no valid moves")
            self.switch_player()  # Switch player

    def end_game(self):
        white_count, black_count = self.game.count_pieces()  # Get counts of white and black pieces
        if white_count > black_count:
            message = f"White wins!\nWhite: {white_count}, Black: {black_count}"  # Display winner message
        elif black_count > white_count:
            message = f"Black wins!\nWhite: {white_count}, Black: {black_count}"  # Display winner message
        else:
            message = f"It's a tie!\nWhite: {white_count}, Black: {black_count}"  # Display tie message

        # Display the winner and end the game
        messagebox.showinfo("Game Over", message)  # Show game over message
        self.gui.window.destroy()  # Close the GUI window


# Define the Othello class
class Othello:
    def __init__(self):
        # Initialize the board size and the board state
        self.board_size = 8
        self.board = np.zeros((self.board_size, self.board_size))
        # Place initial pieces
        self.board[3][3] = self.board[4][4] = 1  # White pieces
        self.board[3][4] = self.board[4][3] = -1  # Black pieces
        # Set current player (-1 for Black, 1 for White)
        self.current_player = -1
        # Game over flag
        self.game_over = False

        # Check if a move is valid

    def is_valid_move(self, row, col):
        # Ensure the position is empty
        if self.board[row][col] != 0:
            # If the cell is not empty,this means not a valid move
            # Then it returns false
            return False

        # These are the possible Directions for checking valid moves
        # up, down, left, right.
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        opponent = -self.current_player

        # Check each direction
        for d in directions:  # Loop through each of the 4 directions.
            rows, columns = row + d[0], col + d[1]

            # Check if the adjacent cell is within bounds and contains an opponent's piece
            if 0 <= rows < self.board_size and 0 <= columns < self.board_size and self.board[rows][columns] == opponent:
                rows += d[0]  # Move one more step in the current direction.
                columns += d[1]

                # Continue moving in the current direction while staying within the board's boundaries
                # it has sandwiched the current opponent's pieces.
                while 0 <= rows < self.board_size and 0 <= columns < self.board_size:

                    # If it finds the current player's own piece, it's a valid move.
                    if self.board[rows][columns] == self.current_player:
                        return True

                    # If it finds an empty cell, stop checking in this direction.
                    # not a valid move
                    elif self.board[rows][columns] == 0:
                        break
                    rows += d[0]  # Move to the next cell in the same direction.
                    columns += d[1]

        # If no valid move is found in any direction, return False.
        return False

        # Make a move on the board

    def make_move(self, row, col):
        # Check if the move is valid
        if not self.is_valid_move(row, col):
            # If the move is not valid, return False.
            return False

        # Put the current player's piece on the board at the specified position.
        self.board[row][col] = self.current_player
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        opponent = -self.current_player

        # Flip opponent's pieces in each direction
        # Loop through each direction.
        for d in directions:

            # Move to the next cell in the current direction.
            rows, columns = row + d[0], col + d[1]

            # List to keep track of opponent pieces that need to be flipped.
            to_flip = []

            # While within board boundaries and encountering opponent's pieces
            while 0 <= rows < self.board_size and 0 <= columns < self.board_size and self.board[rows][
                columns] == opponent:
                # Add the opponent's piece position to the list.
                to_flip.append((rows, columns))

                # Move one more step in the current direction.
                rows += d[0]
                columns += d[1]

            # Check if the line ends with the current player's piece
            if 0 <= rows < self.board_size and 0 <= columns < self.board_size and self.board[rows][
                columns] == self.current_player:

                # Flip all opponent pieces in the opponent list.
                for flip_r, flip_c in to_flip:
                    self.board[flip_r][flip_c] = self.current_player

        # Switch current player
        self.current_player = -self.current_player

        # Return True when the move was successful.
        return True

    # Get a list of valid moves for the current player
    def get_valid_moves(self):
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves

    # Check if the game is over
    def is_game_over(self):
        if len(self.get_valid_moves()) == 0:
            self.current_player = -self.current_player
            if len(self.get_valid_moves()) == 0:
                self.game_over = True
        return self.game_over

    # Create a copy of the game state
    def copy(self):
        copied_game = Othello()
        copied_game.board = copy.deepcopy(self.board)
        copied_game.current_player = self.current_player
        copied_game.game_over = self.game_over
        return copied_game

    # Count the number of white and black pieces
    def count_pieces(self):
        white_count = np.count_nonzero(self.board == 1)
        black_count = np.count_nonzero(self.board == -1)
        return white_count, black_count


# Utility function for evaluating the game state
def utility_function(game, current_player):
    # Count the white and black pieces
    white_count, black_count = game.count_pieces()
    # Calculate score based on the current player's perspective
    if current_player == 1:
        # White's perspective
        score = white_count - black_count
    else:
        # Black's perspective
        score = black_count - white_count
    return score


# Implementation of the minimax algorithm with alpha-beta pruning
def max_value(depth, game, alpha, beta):
    maximum_player = True  # max player

    # Evaluate the board state using the utility function if depth is zero or the game is over
    if depth == 0 or game.is_game_over():
        return utility_function(game, maximum_player)  # return the utility value

    maximum = -np.inf  # Initialize the maximum value to negative infinity
    valid_moves = game.get_valid_moves()  # Get all valid moves for the maximizing player
    # iterate over the valid moves
    for move in valid_moves:
        new_game = game.copy()  # create a copy of the game to simulate the move without affecting the original one
        new_game.make_move(move[0], move[1])
        evaluation = min_value(depth - 1, new_game, alpha, beta)
        maximum = max(maximum, evaluation)  # Update the maximum value
        alpha = max(alpha, maximum)  # Update alpha with the maximum value found so far
        if beta <= alpha:  # Prune the remaining branches as they won't affect the final decision
            break
    return maximum


def min_value(depth, game, alpha, beta):
    maximum_player = False  # min player

    if depth == 0 or game.is_game_over():
        return utility_function(game, maximum_player)

    minimum = np.inf  # Initialize the minimum value to infinity
    valid_moves = game.get_valid_moves()  # Get all valid moves for the minimizing player
    # iterate over the valid moves
    for move in valid_moves:
        new_game = game.copy()  # create a copy of the game to simulate the move without affecting the original one
        new_game.make_move(move[0], move[1])
        evaluation = max_value(depth - 1, new_game, alpha, beta)
        minimum = min(minimum, evaluation)  # Update the minimum value
        beta = min(beta, minimum)
        if beta <= alpha:  # Prune the remaining branches as they won't affect the final decision
            break
    return minimum


# perform minimax alpha-beta pruning
def minimax_alpha_beta(depth, maximum_player, game, alpha, beta):
    if maximum_player:  # if maximum player is true
        return max_value(depth, game, alpha, beta)  # return the maximum value
    else:
        return min_value(depth, game, alpha, beta)  # return the minimum value


# Get the best move for the game
def get_best_move(game, depth):
    best_move = None  # Stores the best move found
    maximum = -np.inf  # initialize the maximum to negative infinity the best it could have right now
    valid_moves = game.get_valid_moves()  # get valid moves
    # Iterate through all valid moves and calculate evaluations
    for move in valid_moves:
        new_game = game.copy()  # create a copy of the game to simulate the move without affecting the original one
        new_game.make_move(move[0], move[1])  # make move
        evaluation = minimax_alpha_beta(depth, False, new_game, -np.inf, np.inf)
        # Track the move with the highest evaluation
        if evaluation > maximum:  # if the evaluation is better than the current maximum let the current = evaluation
            maximum = evaluation
            best_move = move  # update the best move to the current move with max evaluation
    return best_move


# Class for the graphical user interface (GUI)
class OthelloGUI:
    def __init__(self, game, ai_depth):
        # Initialize the game and AI difficulty level
        self.game = game
        self.ai_depth = ai_depth
        self.game_controller = GameController(self.game, self)
        # Create a window
        self.window = tk.Tk()
        self.window.title("Othello")
        self.cell_size = 60  # Define cell size for the board
        self.create_board()
        self.update_ui()
        # Start the Tkinter main loop
        self.window.mainloop()

    # Create the board grid and canvas
    def create_board(self):
        # Create a canvas for drawing the board
        self.canvas = tk.Canvas(
            self.window,
            width=self.cell_size * 8,
            height=self.cell_size * 8,
            bg='SeaGreen3'
        )
        self.canvas.grid(row=0, column=0)

        # Bind the click event to handle user moves
        self.canvas.bind("<Button-1>", self.handle_click)

        # Draw the board grid
        for i in range(1, 8):
            # Vertical lines
            self.canvas.create_line(
                i * self.cell_size, 0,
                i * self.cell_size, self.cell_size * 8,
                fill='black'
            )
            # Horizontal lines
            self.canvas.create_line(
                0, i * self.cell_size,
                   self.cell_size * 8, i * self.cell_size,
                fill='black'
            )

    # Handle click events on the board
    def handle_click(self, event):
        # Calculate the row and column of the click event
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        if self.game.current_player == -1 and (row, col) in self.game.get_valid_moves():
            self.game_controller.player_move(row, col)
        else:
            messagebox.showinfo("invalid", "It's not the human player's turn.")
            self.game_controller.ai_move()

        # Update the user interface to reflect the current state of the board

    def update_ui(self):
        # Clear the canvas
        self.canvas.delete("all")

        # Draw the board grid again
        for i in range(1, 8):
            # Draw vertical and horizontal lines
            self.canvas.create_line(
                i * self.cell_size, 0,
                i * self.cell_size, self.cell_size * 8,
                fill='black'
            )
            self.canvas.create_line(
                0, i * self.cell_size,
                   self.cell_size * 8, i * self.cell_size,
                fill='black'
            )

        # Draw the current state of the board on the canvas
        for row in range(8):
            for col in range(8):
                piece = self.game.board[row][col]
                if piece != 0:
                    self.draw_piece(row, col, piece)

        # Highlight the valid moves for the current player
        self.highlight_valid_moves()

    # Draw pieces on the board
    def draw_piece(self, row, col, piece):
        # Calculate the center coordinates of the cell
        x = col * self.cell_size + self.cell_size // 2
        y = row * self.cell_size + self.cell_size // 2

        # Define the radius of the piece
        radius = self.cell_size // 3

        # Choose color for the piece
        color = 'black' if piece == -1 else 'white'

        # Draw a circle representing the piece
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=color
        )

    # Highlight valid moves for the current player
    def highlight_valid_moves(self):
        # Get the list of valid moves for the current player
        valid_moves = self.game.get_valid_moves()
        for row, col in valid_moves:
            # Calculate the coordinates of the tile
            x0 = col * self.cell_size
            y0 = row * self.cell_size
            x1 = (col + 1) * self.cell_size
            y1 = (row + 1) * self.cell_size

            # Create a frame around the tile as a highlight for the valid move
            self.canvas.create_rectangle(x0 + 5, y0 + 5, x1 - 5, y1 - 5, outline="yellow", width=1)

    # Function to end the game


# Function to start the game with a specified difficulty
def start_game_with_difficulty(ai_depth):
    # Create a new instance of the Othello game
    game = Othello()
    # Initialize the GUI with the specified AI depth
    OthelloGUI(game, ai_depth)


# Main function
def main():
    # Create the Tkinter root window for selecting difficulty
    selection_window = tk.Tk()
    selection_window.title("Select Difficulty")

    # Create a label to instruct the user
    instruction_label = tk.Label(selection_window, text="Select AI Difficulty Level:")
    instruction_label.pack(pady=10)

    # Create buttons for selecting different difficulty levels
    easy_button = tk.Button(
        selection_window,
        text="Easy",
        command=lambda: [selection_window.destroy(), start_game_with_difficulty(1)]  # Set AI depth to 1 for Easy
    )
    easy_button.pack(pady=5)

    medium_button = tk.Button(
        selection_window,
        text="Medium",
        command=lambda: [selection_window.destroy(), start_game_with_difficulty(3)]  # Set AI depth to 3 for Medium
    )
    medium_button.pack(pady=5)

    hard_button = tk.Button(
        selection_window,
        text="Hard",
        command=lambda: [selection_window.destroy(), start_game_with_difficulty(5)]  # Set AI depth to 5 for Hard
    )
    hard_button.pack(pady=5)

    # Start the selection window's main loop
    selection_window.mainloop()


# Execute the main function
if __name__ == "__main__":
    main()
