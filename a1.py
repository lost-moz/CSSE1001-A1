# DO NOT modify or add any import statements
from typing import Optional
from a1_support import *

# Name: Connor Ilic
# Student Number: s4883934
# ----------------

# Write your classes and functions here
def num_hours() -> float:
    """Returns the number of hours spent on this assignment."""
    return 15.0

def generate_initial_board() -> list[str]:
    """Returns an empty board, a list of 8 strings, which each string
    has 8 '-' characters.
    
    Each string of the board is a column where index 1 of the string is
    the top and index 7 is the bottom.
    """
    return ["--------", "--------", "--------", "--------",
             "--------", "--------", "--------", "--------"]

def is_column_full(column: str) -> bool:
    """Checks if a column is full.
    Args:
        Column: A column string that belongs to the board list.
    
    Returns:
        A boolean, True if there isn't a blank piece in the column,
        otherwise False.
    """
    return not BLANK_PIECE in column

def is_column_empty(column: str) -> bool:
    """Checks if a column is empty.
    Args:
        Column: A column string that belongs to the board list.
    
    Returns:
        A boolean, True if there isn't a X or O piece in the column,
        otherwie False.
    """
    return not (PLAYER_1_PIECE in column or PLAYER_2_PIECE in column)

def display_board(board: list[str]) -> None:
    """Prints the board as a string in the terminal.

    Args:
        board: The board, a list of 8 string with 8 characters each,
            to be displayed.
    """
    
    board_visual: str = ""

    """
    These for loops iterates through characters from the board by
    column then row, from left to right then top to bottom
    """
    for row in range(0, BOARD_SIZE):
        for column in range(0, BOARD_SIZE):
            board_visual += f"{COLUMN_SEPARATOR}{board[column][row]}"
        board_visual += f"{COLUMN_SEPARATOR}\n"

    board_visual += " 1 2 3 4 5 6 7 8 "
    print(board_visual)

def check_input(command: str) -> bool:
    """Checks if the command is valid.

    Valid commands (not capital sensitive) include: 'H', 'Q', 'AX',
    'RX' (X is a number between 1-8). Prints the corresponding
    error message if not valid.

    Args:
        command: The action that the user has inputted.
    
    Returns:
        A boolean, True if the command is valid, otherwise False.
    """
    command = command.capitalize()
    if command == "H":
        return True
    
    if command == "Q":
        return True
    
    if len(command) == 2:
        if command[0] in "AR":
            if command[1] in "09":
                print(INVALID_COLUMN_MESSAGE)
                return False
            elif command[1] in "12345678":
                return True
        
    
    print(INVALID_FORMAT_MESSAGE)
    return False

def get_action() -> str:
    """Asks the user for an action.
    
    Repeatedly asks the user for an action until the action is valid,
    then return the action.
    """
    while (True):
        action: str = input("Please enter action (h to see valid commands): ")
        if check_input(action):
            break
    return action

def add_piece(board: list[str], piece: str, column_index: int) -> bool:
    """Updates the board when a piece is added.
    
    Args:
        board: The board for the game,
            a list of 8 strings each with 8 characters.
        piece: The piece to be added to the column.
        column_index: The index of the column in the board
            that the piece will be added to.
    
    Returns:
        A boolean, True if the piece can be added, otherwise False.
    """
    column: str = board[column_index]

    if is_column_full(column):
        print(FULL_COLUMN_MESSAGE)
        return False
    
    """
    the .rfind(BLANK_PIECE) string method returns
    the index of the last occurring '-' in the string
    """
    last_blank_piece_index: int = column.rfind(BLANK_PIECE)

    board[column_index] = (column[:last_blank_piece_index]
                            + piece
                            + column[last_blank_piece_index + 1:])
    return True

def remove_piece(board: list[str], column_index: int) -> bool:
    """Updates the board when a piece is removed.
    
    Args:
        board: The board for the game,
            a list of 8 strings each with 8 characters.
        column_index: The index of the column in the board
            that a piece will be removed from.
    
    Returns:
        A boolean, True if the piece can be remove, otherwise False.
    """
    column: str = board[column_index]
    if is_column_empty(column):
        print(EMPTY_COLUMN_MESSAGE)
        return False
    
    board[column_index] = BLANK_PIECE + column[:-1]
    return True

def create_comparison_list(board: list[str]) -> list[str]:
    """Creates a list for comparing who won the game.
    
    The list contains all the horizontals, verticles, and diagonals
    of the board.
    
    Args:
        board: The board for the game,
            a list of 8 strings each with 8 characters.
    
    Returns:
        A list that contains all the horizontal, verticle,
        and diagonal lines of the board.
    """
    comparison_list: list[str] = []

    #Verticles
    comparison_list += board

    #Horizontals
    for row in range(0, BOARD_SIZE):
        string = ""
        for column in range(0, BOARD_SIZE):
            string += board[column][row]
        comparison_list.append(string)

    
    #Diagonals
    #Left to right diagonals
    """
    Since there is only 9 diagonal lines in the board that
    can have more than 3 pieces in it, we create a list of 9 strings
    """
    diagonals: list[str] = ["", "", "", "", "", "", "", "", ""]
    """
    These for loops iterate through rows then columns,
    from top to bottom then left to right
    """
    for column in range(0, 8):
        for row in range(0, 8):
            """
            The diagonal an element belongs to can be identified by
            subtracting the element's row index from the column index.
            For example, take board[3][2], 3 - 2 = 1, hence board[3][2]
            belongs to the 1 diagonal. Another example,
            take board[4][6], 4 - 6 = -2, hence board[4][6]
            belongs to the -2 diagonal.
            """
            diagonal_ID = column - row
            """
            We only add diagonals that can have 4 or more pieces to the
            diagonals list, which is the diagonals between -4 and 4
            """
            if diagonal_ID <= 4 and diagonal_ID >= -4:
                """
                Since the diagonal domain is [-4, 4] add 4 so it can
                be used as its corresponding diagonals list index
                """
                diagonal_ID += 4
                diagonals[diagonal_ID] += board[column][row]

    comparison_list += diagonals

    #Right to left diagonals
    diagonals = ["", "", "", "", "", "", "", "", ""]
    """
    These for loops iterate through rows then columns,
    from top to bottom then right to left
    """
    for column in range(7, -1, -1):
        for row in range(0, 8):
            """
            The diagonal an element belongs to can be identified
            by adding the element's row index to the column index.
            For example, take board[3][2], 3 + 2 = 6, hence
            board[3][2] belongs to the 6 diagonal.
            Another example, take board[4][6],
            4 + 6 = 10, hence board[4][6] belongs to the 10 diagonal.
            """
            diagonal_ID = column + row

            #Only diagonals from 3 to 11 can have more than 3 pieces
            if diagonal_ID >= 3 and diagonal_ID <= 11:
                #Subtract 3 to be used as the diagonals list index
                diagonal_ID -= 3
                diagonals[diagonal_ID] += board[column][row]

    comparison_list += diagonals
    return comparison_list


def check_win(board: list[str]) -> Optional[str]:
    """Checks if there is a winner and which player won.

    Args:
        board: The board for the game,
            a list of 8 strings each with 8 characters.
    
    Returns:
        A string, 'X' means player 1 won, 'O' player 2 won,
        '-' draw, if None returns than no one has won.
    """
    comparison_list: list[str] = create_comparison_list(board)
    
    did_X_win: bool = False
    did_O_win: bool = False
    for i in comparison_list:
        if PLAYER_1_PIECE*4 in i:
            did_X_win = True
        
        if PLAYER_2_PIECE*4 in i:
            did_O_win = True
        
        if did_O_win and did_X_win:
            break
    
    if did_O_win and did_X_win:
        return BLANK_PIECE
    
    if did_X_win:
        return PLAYER_1_PIECE
    
    if did_O_win:
        return PLAYER_2_PIECE

def act(board: list[str], piece: str, action: str) -> bool:
    """Does an action by calling other function or printing a message.
    
    Args:
        board: The board for the game,
            a list of 8 strings each with 8 characters.
        piece: The current player's piece.
        action: The action that the current player has inputted.
    
    Returns:
        A boolean, False if the action does not progress the game,
        otherwise True.
    """
    continue_round: bool = False
    if action[0] == "A":
        continue_round = add_piece(board, piece, int(action[1]) - 1)
    
    if action[0] == "R":
        continue_round = remove_piece(board, int(action[1]) - 1)
    
    if action == "H":
        print(HELP_MESSAGE)
        continue_round = False
    
    if action == "Q":
        continue_round = True
    
    return continue_round

def play_round(board: list[str], round_number: int) -> bool:
    """Plays a round of the game.

    Args:
        board: The board for the game,
            a list of 8 strings each with 8 characters.
        round_number: What round as an integer the game
            is currently on.
    
    Returns:
        A boolean that dictates whether the game should continue,
        False if the player inputs the quit action, otherwise True.
    """
    if round_number % 2 == 0:
        move_message: str = PLAYER_1_MOVE_MESSAGE
        piece: str = PLAYER_1_PIECE
    else:
        move_message: str = PLAYER_2_MOVE_MESSAGE
        piece: str = PLAYER_2_PIECE
    
    display_board(board)
    print(move_message)

    continue_round = False
    #Loops until the player enters an action that progresses the game
    while (not continue_round):
        
        action = get_action().capitalize()
        continue_round = act(board, piece, action)

        if action == "H":
            display_board(board)
            print(move_message)
    return action != "Q"

def play_game() -> None:
    """Plays a game of connect 4."""
    board: list[str] = generate_initial_board()
    round_number: int = 0
    continue_game: bool = True

    while(continue_game):
        continue_game = play_round(board, round_number)
        round_number += 1

        winner: str = check_win(board)
        if winner:
            display_board(board)
            if winner == PLAYER_1_PIECE:
                print(PLAYER_1_VICTORY_MESSAGE)
            if winner == PLAYER_2_PIECE:
                print(PLAYER_2_VICTORY_MESSAGE)
            if winner == BLANK_PIECE:
                print(DRAW_MESSAGE)
            break



def main() -> None:
    """The main function"""
    continue_response = "Y"
    while (continue_response == "Y"):
        play_game()
        continue_response = input(CONTINUE_MESSAGE).capitalize()

    

if __name__ == "__main__":
    main()
    
