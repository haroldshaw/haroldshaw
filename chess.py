
"""
Chess Game
Assignment 1
Semester 2, 2021
CSSE1001/CSSE7030
"""

from typing import Optional, Tuple

from a1_support import *

# Replace these <strings> with your name, student number and email address.
__author__ = "Harold Shaw, 47020665"
__email__ = "s4702066@student.uq.edu.au"

def initial_state() -> Board:
    """Sets initial state of board.

    Returns:
        (Board): each piece is in starting position.
    """
    row_b1 = "rnbqkbnr"
    row_b2 = "pppppppp"
    row_w1 = row_b1.upper()
    row_w2 = row_b2.upper()
    row_emp = 8 * EMPTY

    return (row_b1, row_b2, row_emp, row_emp, row_emp, row_emp, row_w2, row_w1)

def print_board(board: Board) -> None:
    """Prints board.

    Parameters:
        board (Board): The current state of the board.

    Returns:
        (None)
    """
    count = 0

    # Prints each line of board with its corresponding row number.
    while count < BOARD_SIZE:
        row = board[count]
        print(row + '  ' + str(BOARD_SIZE - count))
        count += 1

    # Prints column letters under rest of board.
    print('\nabcdefgh')

def square_to_position(square: str) -> Position:
    """Converts position in square format to position in (row, col) format.

    Parameters:
        square (str): A square on the board.

    Returns:
        (Position): A position on the board.
    """
    letter_input = square[0]
    number_input = int(square[1])

    row = 8 - int(number_input)

    cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    for letter in cols:
        if letter == letter_input or letter == letter_input.lower():
            col = cols[letter]
    return (row, col)

def process_move(user_input: str) -> Move:
    """Converts move from two squares to two positions.

    Parameters:
        user_input (str): A move of the form "letternum letternum".

    Returns:
        (Move): A move of the form ((row, col), (row, col)).
    """
    from_input = user_input[0:2]
    to_input = user_input[3:5]

    pos_from = square_to_position(from_input)
    pos_to = square_to_position(to_input)

    return (pos_from, pos_to)

def change_position(board: Board, position: Position, character: str) -> Board:
    """Changes original character at position to character.

    Parameters:
        board (Board): The current state of the board.
        position (Position): A position on the board of form (row, col).
        character (str): A piece on the board.

    Returns:
        (Board): An updated state of the board with character at position.
    """
    # Isolates position to be changed on board and substitutes character.
    row_accessed = list(board[position[0]])
    row_accessed[position[1]] = character
    updated_row = ''.join(row_accessed) # joins each element of row_accessed

    # Substitutes updated row containing 'character' for original row.
    board = list(board)
    board[position[0]] = updated_row
    updated_board = tuple(board)

    return updated_board

def clear_position(board: Board, position: Position) -> Board:
    """Changes character at position on board to an empty character.

    Parameters:
        board (Board): The current state of the board.
        position (Position): A position on the board of form (row, col).

    Returns:
        (Board): An updated state of the board with position being EMPTY.
    """
    return change_position(board, position, EMPTY)

def update_board(board: Board, move: Move) -> Board:
    """Moves character from initial position to valid position.

    Parameters:
        board (Board): The current state of the board.
        move (Move): A move of form ((row, col), (row, col)).

    Returns:
        (Board): An updated state of the board with move completed.
    """
    # Finds character at initial position.
    character = piece_at_position(move[0], board)

    # Changes position of character to intended position.
    board = change_position(board, move[1], character)

    # Clears initial position of character.
    updated_board = clear_position(board, move[0])

    return updated_board

def get_current_players_pieces(whites_turn: bool):
    """Determines pieces of player whose turn it is.

    Parameters:
        whites_turn (bool): True iff it is white's turn.

    Returns:
        (Pieces): The set of pieces belonging to the player whose turn it is.
    """
    if whites_turn == True:
        current_pieces = WHITE_PIECES
    else:
        current_pieces = BLACK_PIECES

    return current_pieces

def get_other_players_pieces(whites_turn: bool):
    """Determines pieces of player whose turn it is not.

    Parameters:
        whites_turn (bool): True iff it is white's turn.

    Returns:
        (Pieces): The set of pieces belonging to the player whose turn it isn't.
    """
    if whites_turn == True:
        other_pieces = BLACK_PIECES
    else:
        other_pieces = WHITE_PIECES

    return other_pieces

def is_current_players_piece(piece: str, whites_turn: bool) -> bool:
    """Checks if piece belongs to the player whose turn it is.

    Parameters:
        piece (str): A specific piece belonging to a player.
        whites_turn (bool): True iff it is white's turn.

    Returns:
        (bool): True iff piece belongs to the player whose turn it is.
    """
    current_pieces = get_current_players_pieces(whites_turn)

    for character in current_pieces:
        if character == piece:
            return True
    return False

def is_move_position_valid(move: Move, board: Board, whites_turn: bool) -> bool:
    """Checks whether move position is empty or hosts a piece of other player.

    Parameters:
        move (Move): A move of format ((row, col), (row, col)).
        board (Board): The current state of the board.
        whites_turn (bool): True iff it is white's turn.

    Returns:
        (bool): True iff move position is empty or hosts piece of other player.
    """
    character = piece_at_position(move[1], board)
    other_pieces = get_other_players_pieces(whites_turn)

    if character == EMPTY:
        return True
    else:
        for piece in other_pieces:
            if piece == character:
                return True
        return False

def can_piece_perform(move: Move, board: Board, whites_turn: bool) -> bool:
    """Checks whether a move is appropriate for the deltas of a specific piece
    from a specific position on board.

    Parameters:
        move (Move): A move of format ((row, col), (row, col)).
        board (Board): The current state of the board.
        whites_turn (bool): True iff it is white's turn.

    Returns:
        (bool): True iff move is appropriate for deltas of specified piece at
        specified position.
    """
    possible_moves = get_possible_moves(move[0], board)
    for possible_move in possible_moves:
        if possible_move == move[1]:
            return True
    return False

def is_move_valid(move: Move, board: Board, whites_turn: bool) -> bool:
    """Checks whether a move is valid based on board and whose turn it is.

    Parameters:
        move (Move): A move of format ((row, col), (row, col)).
        board (Board): The current state of the board.
        whites_turn (bool): True iff it is white's turn.

    Returns:
        (bool): True iff move is valid for given board and player's turn.
    """
    count = 0
    character = piece_at_position(move[0], board)

    # Checks intended move position exist on board
    if out_of_bounds(move[1]) == False:
        count += 1

    # Checks both positions in move are distinct
    if move[0] != move[1]:
        count += 1

    # Checks if piece belongs to player whose turn it is.
    if is_current_players_piece(character, whites_turn) == True:
        count += 1

    # Checks to is either empty or belongs to a piece of other player
    if is_move_position_valid(move, board, whites_turn) == True:
        count += 1

    # Checks move is appropriate for specific piece's deltas
    if can_piece_perform(move, board, whites_turn) == True:
        count += 1

    # Checks that move does not put player whose turn it is in check
    updated_board = update_board(board, move)
    if is_in_check(updated_board, whites_turn) == False:
        count += 1

    # Checks if all above conditions are met
    if count == 6:
        return True
    return False


def can_move(board: Board, whites_turn: bool) -> bool:
    """Determines whether the player whose turn it is can (has the ability to)
    move.

    Parameters:
        board (Board): The current state of the board.
        whites_turn(bool): True iff it is white's turn.

    Returns:
        (bool): True iff player whose turn it is can move based on board.
    """
    current_pieces = get_current_players_pieces(whites_turn)
    piece_locations = ()
    possible_moves = ()
    count = 0
    valid = 0

    # Finds positions of all pieces belonging to player whose turn it is.
    for piece in current_pieces:
        piece_locations += (find_piece(piece, board),)

    # Gets all possible moves for each of the players pieces on board.
    for location in piece_locations:
        if location != None:
            moves_to_append = list(get_possible_moves(location, board))
            # Stores moves valid for piece at location with location.
            possible_moves += (location, moves_to_append,)
            possible_moves = list(possible_moves)

    # Checks moves for each of players respective pieces remaining are valid.
    for moves in possible_moves:
        count += 1 # ensures moves are selected, not locations.
        if count % 2 != 0:
            piece_pos = moves
        else:
            # Checks whether for possible moves of each piece, if any are valid.
            for move in moves:
                if is_move_valid((piece_pos, move), board, whites_turn) == True:
                    valid += 1
    if valid >= 1:
        return True
    return False

def is_stalemate(board: Board, whites_turn: bool) -> bool:
    """Checks if there is a stalemate.

    Parameters:
        board (Board): The current state of the board.
        whites_turn (bool): True iff it is white's turn.

    Returns:
        (bool): True iff there is a stalemate.
    """
    if is_in_check(board, whites_turn) == False:
        if can_move(board, whites_turn) == False:
            return True
    return False

def check_game_over(board: Board, whites_turn: bool) -> bool:
    """Checks whether game is over by either checkmate or stalemate.

    Parameters:
        board (Board): The current state of the board.
        whites_turn (bool): True iff it is white's turn.

    Returns:
        (bool): True iff the game is over.
    """
    if is_in_check(board, whites_turn) == True:
        if can_move(board, whites_turn) == False:
            print("\nCheckmate")
            return True
        else:
            if whites_turn == True:
                print("\nWhite is in check")
                return False
            else:
                print("\nBlack is in check")
                return False
    else:
        if is_stalemate(board, whites_turn) == True:
            print("\nStalemate")
            return True
        return False

def interpret_move(move: Move) -> str:
    """Determines whether user input is a move, request to quit or request
    for help.

    Parameters:
        move (Move): User input.

    Returns:
        (str): Either 'HELP', 'QUIT' or 'MOVE' depending on the format of the
                    user input.

    Examples:
        >>> inperpret_move("e2 e4")
        'MOVE'
        >>> interpret_move("h")
        'HELP'
        >>> interpret_move("q")
        'QUIT'
    """
    if move == 'h' or move == 'H':
        return 'HELP'
    elif move == 'q' or move == 'Q':
        return 'QUIT'
    else:
        return 'MOVE'

def make_a_move(board: Board, move: Move, whites_turn: bool) -> Optional[Board]:
    """Updates board with users move after completing validating and
    processing move.

    Parameters:
        board (Board): The current state of the board.
        move (Move): A move of format ((row, col), (row, col)).
        whites_turn (bool): True iff it is white's turn.

    Returns:
        (Board | False): An updated board state with move implemented.
    """
    if valid_move_format(move) == True:
        move = process_move(move)
        if is_move_valid(move, board, whites_turn) == True:
            updated_board = update_board(board, move)
            return updated_board
        else:
            return False
    else:
        return False

def change_turn(whites_turn: bool) -> bool:
    """Changes whose turn it is.

    Parameters:
        whites_turn (bool): True iff it is white's turn.

    Returns:
        (bool): True iff black has most recently had their turn.
    """
    if whites_turn == True:
        whites_turn = False
    else:
        whites_turn = True

    return whites_turn

def main():
    """Entry point to gameplay"""
    board = initial_state()
    print_board(board)

    whites_turn = True

    while True:
        # Gets move input from user.
        if whites_turn == True:
            move = str(input("\nWhite's move: "))
        else:
            move = str(input("\nBlack's move: "))

        # Determines whether move is help, quit or move.
        if interpret_move(move) == 'HELP':
            print(HELP_MESSAGE)
            print_board(board)
        elif interpret_move(move) == 'QUIT':
            quit_confirm = input("Are you sure you want to quit? ")
            if quit_confirm == 'y' or quit_confirm == 'Y':
                break
            else:
                print_board(board)
        else:
            # Validates move.
            test_board = make_a_move(board, move, whites_turn)
            if test_board == False:
                print("Invalid move\n")
                print_board(board)
            else:
                # Completes move.
                board = test_board
                print_board(board)
                whites_turn = change_turn(whites_turn)
                if check_game_over(board, whites_turn) == True:
                    break

if __name__ == "__main__":
    main()
