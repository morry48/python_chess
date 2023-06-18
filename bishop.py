import chess_rule
from board import Board
from piece import Piece


class Bishop(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        """sets initial values by calling the constructor of Piece"""
        super().__init__(pos_X, pos_Y, side_)

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to rule [Rule1] and [Rule3] (see section Intro)
        Hint: use is_piece_at
        """

        # out of range
        if pos_X > B[0] or pos_Y > B[0]:
            return False

        if not self.is_diagonal(pos_X, pos_Y):
            return False

        direction = self.get_direction(pos_X, pos_Y)

        if not direction:
            return False
        for step in range(1, abs(self.pos_y - pos_Y) + 1):
            move_x = self.pos_x + (step * direction[0])
            move_y = self.pos_y + (step * direction[1])
            if chess_rule.is_out_board(move_x, move_y, B):
                break
            if chess_rule.is_piece_at(move_x, move_y, B):
                encountering_piece = chess_rule.piece_at(move_x, move_y, B)
                if encountering_piece.side != self.side:
                    if encountering_piece.pos_x == pos_X and encountering_piece.pos_y == pos_Y:
                        return True
                return False
        return True

    def is_diagonal(self, x: int, y: int):
        return abs(self.pos_x - x) == abs(self.pos_y - y)

    def get_direction(self, pos_X: int, pos_Y: int):
        if self.pos_x < pos_X and self.pos_y < pos_Y:
            x = 1
            y = 1
        elif self.pos_x > pos_X and self.pos_y < pos_Y:
            x = -1
            y = 1
        elif self.pos_x < pos_X and self.pos_y > pos_Y:
            x = 1
            y = -1
        elif self.pos_x > pos_X and self.pos_y > pos_Y:
            x = -1
            y = -1
        else:
            return False
        return x, y

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """
        checks if this bishop can move to coordinates pos_X, pos_Y
        on board B according to all chess rules

        Hints:
        - firstly, check [Rule1] and [Rule3] using can_reach
        - secondly, check if result of move is capture using is_piece_at
        - if yes, find the piece captured using piece_at
        - thirdly, construct new board resulting from move
        - finally, to check [Rule4], use is_check on new board
        """

        if not self.can_reach(pos_X, pos_Y, B):
            return False
        new_board = self.build_new_board(pos_X, pos_Y, B)

        if chess_rule.is_check(self.side, new_board):
            return False
        return True

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        """
        returns new board resulting from move of this rook to coordinates pos_X, pos_Y on board B
        assumes this move is valid according to chess rules
        """
        new_board = self.build_new_board(pos_X, pos_Y, B)
        return new_board

    def build_new_board(self, pos_X: int, pos_Y: int, B: Board):
        new_list = []
        for index, piece in enumerate(B[1]):
            if piece.pos_x == self.pos_x and piece.pos_y == self.pos_y and piece.side == self.side:
                continue
            if piece.pos_x == pos_X and piece.pos_y == pos_Y and piece.side != self.side:
                continue
            new_list.append(piece)
        new_piece = Bishop(pos_X, pos_Y, self.side)
        new_list.append(new_piece)
        return B[0], new_list
