import chess_rule
from piece import Piece
from board import Board


# from bishop import Bishop


class King(Piece):
    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        """sets initial values by calling the constructor of Piece"""
        super().__init__(pos_X, pos_Y, side_)

    def can_reach(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """checks if this king can move to coordinates pos_X, pos_Y on board B according to rule [Rule2] and [Rule3]"""

        diff_x = abs(self.pos_x - pos_X)
        diff_y = abs(self.pos_y - pos_Y)

        # Check if the destination coordinates are within the king's range
        if diff_x <= 1 and diff_y <= 1 and (diff_x != 0 or diff_y != 0):
            if chess_rule.is_piece_at(pos_X, pos_Y, B):
                encountering_piece = chess_rule.piece_at(pos_X, pos_Y, B)
                if encountering_piece.side != self.side:
                    return True
            else:
                return True
        return False

    def can_move_to(self, pos_X: int, pos_Y: int, B: Board) -> bool:
        """checks if this king can move to coordinates pos_X, pos_Y on board B according to all chess rules"""
        if not self.can_reach(pos_X, pos_Y, B) or chess_rule.is_piece_at(pos_X, pos_Y, B):
            return False

        new_board = self.build_new_board(pos_X, pos_Y, B)
        if chess_rule.is_check(self.side, new_board):
            return False
        return True

    def move_to(self, pos_X: int, pos_Y: int, B: Board) -> Board:
        """
        returns new board resulting from move of this king to coordinates pos_X, pos_Y on board B
        assumes this move is valid according to chess rules
        """
        new_board = self.build_new_board(pos_X, pos_Y, B)

        return new_board

    def build_new_board(self, pos_X: int, pos_Y: int, B: Board):
        new_list = self.remove_piece_from_board(pos_X, pos_Y, B)
        new_piece = King(pos_X, pos_Y, self.side)
        new_list.append(new_piece)
        return B[0], new_list
