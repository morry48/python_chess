def location2index(loc: str) -> tuple[int, int]:
    '''converts chess location to corresponding x and y coordinates'''
    chars = list('abcdefghijklmnopqrstuvwxyz')
    return chars.index(loc[0]) + 1, int(loc[1:].strip(","))


def isTwoCharacters(loc: str) -> bool:
    return len(str) == 2


def index2location(x: int, y: int) -> str:
    '''converts  pair of coordinates to corresponding location'''
    chars = list('abcdefghijklmnopqrstuvwxyz')
    alf = chars[x - 1]
    return alf + str(y)


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
    # todo in case of not found
    for piece in B[1]:
        if piece.pos_x == pos_X and piece.pos_y == pos_Y:
            return piece


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

        if not self.can_reach(pos_X, pos_Y, B) or is_piece_at(pos_X, pos_Y, B):
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
                        print(i, j)
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
    board_size = int(lines[0].strip())
    board = (board_size, [])
    for index, line in enumerate(lines[1:]):
        if index == 0:
            side = True
        else:
            side = False
        positions = line.strip().split(', ')
        for piece in positions:
            if not piece:
                continue
            piece_type = piece[0]
            str_location = piece[1:]
            location_tuple = location2index(str_location)
            if piece_type == "B":
                board[1].append(Bishop(location_tuple[0], location_tuple[1], side))
            else:
                board[1].append(King(location_tuple[0], location_tuple[1], side))
    return board


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


def conf2unicode(B: Board) -> str:
    '''converts board cofiguration B to unicode format string (see section Unicode board configurations)'''


def display_borad(B: Board) -> None:
    print("The initial configuration is:", end="")
    for i in range(1, B[0] + 1):
        for j in range(1, B[0] + 1):
            flg = False
            for piece in B[1]:
                if piece.pos_x == i and piece.pos_y == j:
                    flg = True
                    if piece.side and isinstance(piece, King):
                        print("\u2654", end="")
                    elif piece.side and isinstance(piece, Bishop):
                        print("\u2657", end="")
                    elif not piece.side and isinstance(piece, King):
                        print("\u265A", end="")
                    elif not piece.side and isinstance(piece, Bishop):
                        print("\u265D", end="")
                    break
            if not flg:
                print("\u2001", end="")
        print("", end="\n")


def main() -> None:
    '''
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    '''
    # tmp
    # filename = input("File name for initial configuration:")
    filename = "texttest.txt"
    # todo validate This is not a valid file. File name for initial configuration:
    board = read_board(filename)
    display_borad(board)
    side = True
    if side:
        input_for_moving = input("Next move of White:")
    else:
        input_for_moving = input("Next move of Black:")

    if input_for_moving == "QUIT":
        save_filename = input("File name to store the configuration:")
        save_board(save_filename, board)
        print("The game configuration saved.")






if __name__ == '__main__':  # keep this in
    main()
