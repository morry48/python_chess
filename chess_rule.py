import random

import const
from bishop import Bishop
from board import Board
from king import King
from piece import Piece


def location2index(loc: str) -> tuple[int, int]:
    """converts chess location to corresponding x and y coordinates"""
    chars = list('abcdefghijklmnopqrstuvwxyz')
    if not loc[0] in 'abcdefghijklmnopqrstuvwxyz':
        return ()

    try:
        y = int(loc[1:].strip(","))
    except:
        return ()

    if y < const.MIN_CELL_NUMBER or y > const.LIMIT_BOARD_SIZE:
        return ()
    return chars.index(loc[0]) + 1, y


def index2location(x: int, y: int) -> str:
    """converts  pair of coordinates to corresponding location"""
    if 1 > x or x > 26 or 1 > y or y > 26:
        return ""
    chars = list('abcdefghijklmnopqrstuvwxyz')
    try:
        alf = chars[x - 1]
        str_y = str(y)
    except:
        return ""
    return alf + str_y


def is_piece_at(pos_X: int, pos_Y: int, B: Board) -> bool:
    """checks if there is piece at coordinates pox_X, pos_Y of board B"""
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return True
    return False


def piece_at(pos_X: int, pos_Y: int, B: Board) -> Piece:
    """
    returns the piece at coordinates pox_X, pos_Y of board B
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    """
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return piece


def is_out_board(x: int, y: int, B: Board):
    return x > B[0] or y > B[0] or x < 1 or y < 1


def is_check(side: bool, B: Board) -> bool:
    """
    checks if configuration of B is check for side
    Hint: use can_reach
    """
    king = Piece
    for piece in B[1]:
        if piece.side == side and isinstance(piece, King):
            king = piece
            break
    for present_piece in B[1]:
        if not present_piece.side == side:
            if present_piece.can_reach(king.pos_x, king.pos_y, B):
                return True
    return False


def is_checkmate(side: bool, B: Board) -> bool:
    """
    checks if configuration of B is checkmate for side

    Hints:
    - use is_check
    - use can_move_to
    """
    if not is_check(side, B):
        return False
    if not is_make_moving_anywhere(side, B):
        return False
    return True


def is_stalemate(side: bool, B: Board) -> bool:
    """
    checks if configuration of B is stalemate for side

    Hints:
    - use is_check
    - use can_move_to
    """
    if is_check(side, B):
        return False
    if not is_make_moving_anywhere(side, B):
        return False
    return True


def is_make_moving_anywhere(side: bool, B: Board) -> bool:
    for piece in B[1]:
        if piece.side == side:
            for i in range(1, B[0] + 1):
                for j in range(1, B[0] + 1):
                    if not piece.can_reach(i, j, B):
                        continue
                    if piece.can_move_to(i, j, B):
                        new_bord = piece.move_to(i, j, B)
                        if not is_check(side, new_bord):
                            return False
    return True


def read_board(filename: str) -> Board:
    """
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    """
    with open(filename, 'r') as file:
        lines = file.readlines()

    plain_format_lines = construct_format_lines(lines)
    if len(plain_format_lines) != const.TEXT_LINE_BUILD_BOARD:
        raise IOError
    board_size = set_board_size(plain_format_lines[const.TEXT_SIZE_LINE_INDEX])

    board = (board_size, [])

    build_board_one_side(
        board,
        plain_format_lines[const.BOARD_WHITE_SIDE_LINE_INDEX],
        const.WHITE_SIDE
    )

    build_board_one_side(
        board,
        plain_format_lines[const.BOARD_BLACK_SIDE_LINE_INDEX],
        const.BLACK_SIDE
    )

    return board


def construct_format_lines(lines):
    format_lines = []
    for index, line in enumerate(lines):
        line = line.strip()
        if not line:
            if index < const.TEXT_LINE_BUILD_BOARD:
                raise IOError
            else:
                continue
        elements = [elem.strip() for elem in line.split(",") if elem.strip()]
        format_lines.append(elements)
    return format_lines


def set_board_size(board_size_line: list) -> int:
    if len(board_size_line) != 1:
        raise IOError
    try:
        board_size = int(board_size_line[0].strip())
    except:
        raise IOError
    if board_size < const.MIN_BOARD_SIZE or board_size > const.LIMIT_BOARD_SIZE:
        raise IOError
    return board_size


def build_board_one_side(board: Board, plain_format_line: list, side) -> None:
    for piece in plain_format_line:
        if not piece:
            continue
        piece_type = piece[0]
        str_location = piece[1:]
        location_tuple = location2index(str_location)
        if not location_tuple:
            raise IOError
        if not is_piece_in_board(board[0], location_tuple):
            raise IOError

        add_to_board_build_piece(board, location_tuple[0], location_tuple[1], side, piece_type)


def is_bishop(piece_type: str) -> bool:
    return piece_type == "B"


def is_king(piece_type: str) -> bool:
    return piece_type == "K"


def is_piece_in_board(board_size: int, location_tuple: tuple) -> bool:
    return location_tuple[0] <= board_size and location_tuple[1] <= board_size


def add_to_board_build_piece(board: Board, pos_x: int, pos_y: int, side: bool, piece_type: str) -> None:
    if is_bishop(piece_type):
        board[1].append(Bishop(pos_x, pos_y, side))
    elif is_king(piece_type):
        board[1].append(King(pos_x, pos_y, side))
    else:
        raise IOError


def save_board(filename: str, B: Board) -> None:
    """saves board configuration into file in current directory in plain format"""
    with open(filename, 'w') as file:
        # Write the board size
        file.write(str(B[0]) + '\n')
        while_line = ""
        black_line = ""
        for row in B[1]:
            str_position = index2location(row.pos_x, row.pos_y)
            if isinstance(row, King):
                p_type = "K"
            else:
                p_type = "B"
            if row.side:
                while_line = while_line + p_type + str_position + ", "
            else:
                black_line = black_line + p_type + str_position + ", "
        file.write(while_line + '\n')
        file.write(black_line + '\n')


def find_black_move(B: Board) -> tuple[Piece, int, int]:
    """
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules
    assumes there is at least one black piece that can move somewhere

    Hints:
    - use methods of random library
    - use can_move_to
    """

    for piece in B[1]:
        if not piece.side:
            for i in range((B[0] + 1) * (B[0] + 1)):
                a = random.randint(1, B[0])
                b = random.randint(1, B[0])
                if piece.can_move_to(a, b, B):
                    return piece, a, b
    for piece in B[1]:
        if not piece.side:
            for i in range(1, B[0] + 1):
                for j in range(1, B[0] + 1):
                    if piece.can_move_to(i, j, B):
                        return piece, i, j


def conf2unicode(B: Board) -> str:
    """Converts board configuration to a Unicode string for display in the terminal."""
    unicode_board = ""

    for i in range(B[0], 0, -1):  # Iterate in reverse order
        for j in range(1, B[0] + 1):
            piece_found = False

            for piece in B[1]:
                if piece.pos_x == j and piece.pos_y == i:
                    if piece.side and isinstance(piece, King):
                        unicode_board += "\u2654"
                    elif piece.side and isinstance(piece, Bishop):
                        unicode_board += "\u2657"  #
                    elif not piece.side and isinstance(piece, King):
                        unicode_board += "\u265A"
                    elif not piece.side and isinstance(piece, Bishop):
                        unicode_board += "\u265D"

                    piece_found = True
                    break

            if not piece_found:
                unicode_board += "\u2001"

        unicode_board += "\n"
    return unicode_board
