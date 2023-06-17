import random

import const


def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    chars = list('abcdefghijklmnopqrstuvwxyz')
    if not loc[0] in 'abcdefghijklmnopqrstuvwxyz':
        raise IOError

    try:
        y = int(loc[1:].strip(","))
    except:
        raise IOError
    if y < const.MIN_BOARD_SIZE or y > const.LIMIT_BOARD_SIZE:
        raise IOError
    return chars.index(loc[0]) + 1, y


def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    if 1 > x or x > 26 or 1 > y or y > 26:
        raise Exception
    chars = list('abcdefghijklmnopqrstuvwxyz')
    try:
        alf = chars[x - 1]
        str_y = str(y)
    except:
        raise IOError
    return alf + str_y


class Piece:
    pos_x: int
    pos_y: int
    side: bool  # True for White and False for Black

    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values'''
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_


Board = tuple[int, list[Piece]]


def is_piece_at(pos_X: int, pos_Y: int, B: Board) -> bool:
    '''checks if there is piece at coordinates pox_X, pos_Y of board B'''
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return True
    return False


def piece_at(pos_X: int, pos_Y: int, B: Board) -> Piece:
    '''
    returns the piece at coordinates pox_X, pos_Y of board B
    assumes some piece at coordinates pox_X, pos_Y of board B is present
    '''
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return piece
    raise Exception


class Bishop(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        '''

        # out of range
        if pos_X > B[0] or pos_Y > B[0]:
            return False

        #  todo made func (is it exists on the diagonal)
        if abs(self.pos_x - pos_X) != abs(self.pos_y - pos_Y):
            return False

        flg = True
        move_x = self.pos_x
        move_y = self.pos_y
        while flg:
            if move_x > B[0] or move_y > B[0]:
                break

            if self.pos_x < pos_X and self.pos_y < pos_Y:
                move_x += 1
                move_y += 1

            elif self.pos_x > pos_X and self.pos_y < pos_Y:
                move_x -= 1
                move_y += 1

            elif self.pos_x < pos_X and self.pos_y > pos_Y:
                move_x += 1
                move_y -= 1
            elif self.pos_x > pos_X and self.pos_y > pos_Y:
                move_x -= 1
                move_y -= 1
            else:
                return False
            if move_x < 1 or move_y < 1:
                break
            if move_x > B[0] or move_y > B[0]:
                break
            if is_piece_at(move_x, move_y, B):
                encountering_piece = piece_at(move_x, move_y, B)
                if encountering_piece.side != self.side:
                    if encountering_piece.pos_x == pos_X and encountering_piece.pos_y == pos_Y:
                        return True
                return False
        return True

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to all chess rules
        
        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board
        '''

        if not self.can_reach(pos_X, pos_Y, B):
            return False
        new_list = []
        for index, piece in enumerate(B[1]):
            if piece.pos_x == self.pos_x and piece.pos_y == self.pos_y and piece.side == self.side:
                continue
            if piece.pos_x == pos_X and piece.pos_y == pos_Y and piece.side != self.side:
                continue
            new_list.append(piece)
        new_piece = Bishop(pos_X, pos_Y, self.side)
        new_list.append(new_piece)
        new_board = (B[0], new_list)

        if is_check(self.side, new_board):
            return False
        return True

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        '''
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        new_list = []
        for index, piece in enumerate(B[1]):
            if piece.pos_x == self.pos_x and piece.pos_y == self.pos_y and piece.side == self.side:
                continue
            if piece.pos_x == pos_X and piece.pos_y == pos_Y and piece.side != self.side:
                continue
            new_list.append(piece)
        new_piece = Bishop(pos_X, pos_Y, self.side)
        new_list.append(new_piece)
        new_board = (B[0], new_list)

        return new_board


class King(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        '''sets initial values by calling the constructor of Piece'''
        super().__init__(pos_X, pos_Y, side_)

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]'''

        diff_x = abs(self.pos_x - pos_X)
        diff_y = abs(self.pos_y - pos_Y)

        # Check if the destination coordinates are within the king's range
        if diff_x <= 1 and diff_y <= 1 and (diff_x != 0 or diff_y != 0):
            if is_piece_at(pos_X, pos_Y, B):
                encountering_piece = piece_at(pos_X, pos_Y, B)
                if encountering_piece.side != self.side:
                    return True
            else:
                return True
        return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        '''checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules'''
        if not self.can_reach(pos_X, pos_Y, B) or is_piece_at(pos_X, pos_Y, B):
            return False

        new_list = []
        for index, piece in enumerate(B[1]):
            if piece.pos_x == self.pos_x and piece.pos_y == self.pos_y and piece.side == self.side:
                continue
            if piece.pos_x == pos_X and piece.pos_y == pos_Y and piece.side != self.side:
                continue
            new_list.append(piece)
        new_piece = King(pos_X, pos_Y, self.side)
        new_list.append(new_piece)
        new_board = (B[0], new_list)
        if is_check(self.side, new_board):
            return False
        return True

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        '''
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B 
        assumes this move is valid according to chess rules
        '''
        new_list = []
        for index, piece in enumerate(B[1]):
            if piece.pos_x == self.pos_x and piece.pos_y == self.pos_y and piece.side == self.side:
                continue
            if piece.pos_x == pos_X and piece.pos_y == pos_Y and piece.side != self.side:
                continue
            new_list.append(piece)
        new_piece = King(pos_X, pos_Y, self.side)
        new_list.append(new_piece)
        new_board = (B[0], new_list)

        return new_board


def is_check(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is check for side
    Hint: use can_reach
    '''
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
    '''
    checks if configuration of B is checkmate for side

    Hints: 
    - use is_check
    - use can_move_to
    '''
    if not is_check(side, B):
        return False
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


def is_stalemate(side: bool, B: Board) -> bool:
    '''
    checks if configuration of B is stalemate for side

    Hints: 
    - use is_check
    - use can_move_to 
    '''
    if is_check(side, B):
        return False
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
    '''
    reads board configuration from file in current directory in plain format
    raises IOError exception if file is not valid (see section Plain board configurations)
    '''
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
        elements = [elem for elem in line.split(", ") if elem.strip()]
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
        if not is_piece_in_board(board[0], location_tuple):
            raise IOError

        add_to_board_build_peice(board, location_tuple[0], location_tuple[1], side, piece_type)


def is_bishop(piece_type: str) -> bool:
    return piece_type == "B"


def is_king(piece_type: str) -> bool:
    return piece_type == "K"


def is_piece_in_board(board_size: int, location_tuple: tuple) -> bool:
    return location_tuple[0] <= board_size and location_tuple[1] <= board_size


def add_to_board_build_peice(board: Board, pos_x: int, pos_y: int, side: bool, piece_type: str) -> None:
    if is_bishop(piece_type):
        board[1].append(Bishop(pos_x, pos_y, side))
    elif is_king(piece_type):
        board[1].append(King(pos_x, pos_y, side))
    else:
        raise IOError


def save_board(filename: str, B: Board) -> None:
    '''saves board configuration into file in current directory in plain format'''
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
    '''
    returns (P, x, y) where a Black piece P can move on B to coordinates x,y according to chess rules 
    assumes there is at least one black piece that can move somewhere

    Hints: 
    - use methods of random library
    - use can_move_to
    '''

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
    '''Converts board configuration to a Unicode string for display in the terminal.'''
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
                unicode_board += "."

        unicode_board += "\n"
    return unicode_board


def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''
    filename = input("File name for initial configuration:")
    # tmp for test
    # filename = "board_examp.txt"
    # todo validate This is not a valid file. File name for initial configuration:
    board = False
    while not board:
        try:
            board = read_board(filename)
            break
        except IOError:
            filename = input("This is not a valid file. File name for initial configuration: ")

    print(conf2unicode(board))
    side = True
    game_continue = True
    print("The initial configuration is:", end="")
    while game_continue:
        if is_checkmate(side, board):
            if side:
                print("Game over. Black wins.")
                game_continue = False
                continue
            else:
                print("Game over. White wins.")
                game_continue = False
                continue

        if is_stalemate(side, board):
            print("Game over. Stalemate.")
            game_continue = False
            continue

        if side:
            input_for_moving = input("Next move of White:")
        else:
            found = find_black_move(board)
            board = found[0].move_to(found[1], found[2], board)
            print("Next move of Black is "
                  + index2location(found[0].pos_x, found[0].pos_y)
                  + index2location(found[1], found[2])
                  + ". The configuration after Black's move is:")
            print(conf2unicode(board))
            side = not side
            continue

        if input_for_moving == "QUIT":
            save_filename = input("File name to store the configuration:")
            save_board(save_filename, board)
            print("The game configuration saved.")
            game_continue = False
            continue

        if input_for_moving[2].isdecimal():
            prev = input_for_moving[:3]
            after = input_for_moving[3:]
        else:
            prev = input_for_moving[:2]
            after = input_for_moving[2:]

        # exception
        prev2index = location2index(prev)
        if not is_piece_at(prev2index[0], prev2index[1], board):
            print("This is not a valid move.", end="")
            continue
        prev_piece = piece_at(prev2index[0], prev2index[1], board)
        if not prev_piece.side == side:
            print("This is not a valid move.", end="")
            continue
        after2index = location2index(after)
        if not prev_piece.can_move_to(after2index[0], after2index[1], board):
            print("This is not a valid move.", end="")
            continue
        board = prev_piece.move_to(after2index[0], after2index[1], board)
        side = not side


if __name__ == '__main__':  # keep this in
    main()
