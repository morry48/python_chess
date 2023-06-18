class Piece:
    pos_x: int
    pos_y: int
    side: bool  # True for White and False for Black

    def __init__(self, pos_X: int, pos_Y: int, side_: bool):
        """sets initial values"""
        self.pos_x = pos_X
        self.pos_y = pos_Y
        self.side = side_

    def can_move_to(self, pos_X: int, pos_Y: int, B):
        pass

    def can_reach(self, pos_X: int, pos_Y: int, B):
        pass

    def move_to(self, pos_X: int, pos_Y: int, B):
        pass

    def remove_piece_from_board(self, pos_X: int, pos_Y: int, B):
        new_list = []
        for index, piece in enumerate(B[1]):
            if piece.pos_x == self.pos_x and piece.pos_y == self.pos_y and piece.side == self.side:
                continue
            if piece.pos_x == pos_X and piece.pos_y == pos_Y and piece.side != self.side:
                continue
            new_list.append(piece)
        return new_list
