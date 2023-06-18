from chess_puzzle import *


def comparing_boards(Expected_B: Board, Actual_B: Board):
    for piece1 in Actual_B[
        1]:  # we check if every piece in Actual_B is also present in Expected_B; if not, the test will fail
        found = False
        for piece in Expected_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece in Expected_B[
        1]:  # we check if every piece in Expected_B is also present in Actual_B; if not, the test will fail
        found = False
        for piece1 in Actual_B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found
