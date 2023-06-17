import pytest
from chess_puzzle import *


def test_location2index1():
    assert location2index("e2") == (5, 2)


def test_location2indexCaseMax():
    assert location2index("z26") == (26, 26)


def test_location2indexCaseMin():
    assert location2index("a1") == (1, 1)


def test_location2indexCaseNgFormat():
    # out of 26
    with pytest.raises(IOError):
        location2index("a27")
    # out of 26
    with pytest.raises(IOError):
        location2index("a0")
    # not start alfabet
    with pytest.raises(IOError):
        location2index("02")
    # including not int
    with pytest.raises(IOError):
        location2index("a")
    # including not int
    with pytest.raises(IOError):
        location2index("ab")
    # whether is capital permitted
    with pytest.raises(IOError):
        location2index("A1")


def test_index2location1():
    assert index2location(5, 2) == "e2"


def test_index2locationMax():
    assert index2location(26, 26) == "z26"


def test_index2locationMin():
    assert index2location(1, 1) == "a1"


def test_index2locationdexCaseNgRange():
    with pytest.raises(FileNotFoundError):
        index2location(1, 0)
    with pytest.raises(FileNotFoundError):
        index2location(0, 1)
    with pytest.raises(FileNotFoundError):
        index2location(27, 1)
    with pytest.raises(FileNotFoundError):
        index2location(1, 27)


wb1 = Bishop(2, 5, True)
wb2 = Bishop(4, 4, True)
wb3 = Bishop(3, 1, True)
wb4 = Bishop(5, 5, True)
wb5 = Bishop(4, 1, True)

wk1 = King(3, 5, True)
wk1a = King(2, 5, True)

bb1 = Bishop(3, 3, False)
bb2 = Bishop(5, 3, False)
bb3 = Bishop(1, 2, False)

bk1 = King(2, 3, False)

B1 = (5, [wb1, bb1, wb2, bb2, wb3, wk1, bk1])


def test_is_piece_at1():
    assert is_piece_at(2, 2, B1) == False


def test_is_piece_at_case_true():
    assert is_piece_at(2, 5, B1) == True

    # todo case for is_piece_at
    # black
    # white
    # King
    #
    # out of range
    # than 27
    # less 0
    # assert is_piece_at(2, 5, B1) == True


def test_piece_at1():
    assert piece_at(3, 3, B1) == bb1


def test_piece_at_for_false_side():
    assert piece_at(3, 3, B1) != wb1


def test_piece_at_for_true_side():
    assert piece_at(5, 3, B1) == bb2

    # todo case for piece_at
    # not found


def test_can_reach1():
    assert wb2.can_reach(5, 5, B1) == True


def test_can_reach_for_diagonal_ok_but_the_same_side():
    assert wb2.can_reach(3, 5, B1) == False


def test_can_reach_for_diagonal_ok_and_the_opponent_side():
    assert wb2.can_reach(5, 3, B1) == True
    assert bb1.can_reach(4, 4, B1) == True


def test_can_reach_for_not_diagonal_ng():
    assert wb1.can_reach(1, 3, B1) == False


def test_can_reach_for_the_opponent_side_but_there_are_opponent_piece_between_them():
    assert bb1.can_reach(5, 5, B1) == False


def test_can_reach_for_firstly_same():
    assert wb2.can_reach(4, 4, B1) == False


def test_can_reach_for_over_range_for_board():
    assert wb2.can_reach(6, 6, B1) == False
    assert wb1.can_reach(1, 6, B1) == False


def test_can_reach_for_king_vertical():
    assert wk1.can_reach(3, 4, B1) == True
    assert wk1.can_reach(4, 5, B1) == True
    assert wk1.can_reach(4, 6, B1) == True


def test_can_reach_for_more_than_two():
    assert wk1.can_reach(3, 7, B1) == False


def test_can_reach_for_the_same_side():
    assert wk1.can_reach(4, 4, B1) == False


def test_can_reach_for_wb_beside_opponent_k():
    wb_besides_opponent_k = Bishop(2, 2, True)
    B_case_of_wb_besides_opponent_k = (5, [wb1, bb1, wb2, bb2, wb3, wk1, bk1, wb_besides_opponent_k])
    assert bk1.can_reach(2, 2, B_case_of_wb_besides_opponent_k) == True

    # todo case for can_reach
    # less than 1


def test_can_move_to1():
    assert wb2.can_move_to(5, 5, B1) == False


def test_can_move_to_for_bishop_ok():
    wk_moved = King(4, 1, True)
    B_moved_wk_for_ok = (5, [wb1, bb1, wb2, bb2, wb3, wk_moved, bk1])
    assert wb2.can_move_to(5, 5, B_moved_wk_for_ok) == True


def test_can_move_to_for_king_ok():
    assert wk1.can_move_to(4, 5, B1) == True


def test_can_move_to_for_king_ng():
    assert wk1.can_move_to(3, 4, B1) == False

    # ng to ok
    bk_moved = King(2, 2, False)
    B_wk_moved_for_ok = (5, [wb1, bb1, wb2, bb2, wb3, wk1, bk_moved])
    assert wk1.can_move_to(3, 4, B_wk_moved_for_ok) == True

    # todo case for get opponent


def test_move_to1():
    wb2a = Bishop(3, 3, True)
    Actual_B = wb2.move_to(3, 3, B1)
    Expected_B = (5, [wb2a, wb1, wk1, bk1, bb2, wb3])

    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

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


def test_move_to_for_king():
    wk1_after = King(4, 5, True)
    Actual_B = wk1.move_to(4, 5, B1)
    Expected_B = (5, [wb1, bb1, wb2, bb2, wb3, wk1_after, bk1])

    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

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

    # todo case for move_to
    # king get opponent


def test_is_check1():
    B2 = (5, [wb1, wk1, bk1, bb1, bb2, wb3])
    assert is_check(True, B2) == True


def test_is_check_by_bishop_false():
    B2 = (5, [wb1, wk1, bk1, bb1, bb2, wb3])
    assert is_check(False, B2) == False
    B_for_false = (5, [wb1, wk1, bk1, bb1, wb3])
    assert is_check(True, B_for_false) == False


def test_is_check_by_king_visualiser():
    wk1_for_true = King(3, 3, True)
    B_wk1_for_true = (5, [wb1, wk1_for_true, bk1, bb1, wb3])
    assert is_check(True, B_wk1_for_true) == True
    assert is_check(False, B_wk1_for_true) == True


def test_is_checkmate1():
    B3 = (5, [wk1a, wb4, bk1, bb2, bb3, wb3, wb5])
    assert is_checkmate(False, B3) == True


def test_is_checkmate_for_ng():
    B3_fixed_for_false = (5, [wk1a, wb4, bk1, bb2, wb3, wb5])
    assert is_checkmate(False, B3_fixed_for_false) == False


def test_is_stalemate_true():
    wk = King(1, 1, True)
    bb = Bishop(1, 2, False)
    bk = King(3, 3, False)
    B_stalemate = (5, [wk, bb, bk])
    assert is_stalemate(True, B_stalemate) == True

    assert is_stalemate(False, B_stalemate) == False


def test_is_stalemate_false():
    wk = King(1, 1, True)
    bb = Bishop(1, 2, False)
    bk = King(4, 3, False)
    B_stalemate = (5, [wk, bb, bk])
    assert is_stalemate(True, B_stalemate) == False

    assert is_stalemate(False, B_stalemate) == False


def test_read_board1():
    B = read_board("board_examp.txt")
    assert B[0] == 5

    for piece in B[1]:  # we check if every piece in B is also present in B1; if not, the test will fail
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]:  # we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found


def test_save_board():
    filename = "board_examp_write.txt"

    save_board(filename, B1)
    B = read_board(filename)
    for piece in B[1]:
        found = False
        for piece1 in B1[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece1 in B1[1]:  # we check if every piece in B1 is also present in B; if not, the test will fail
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found


def test_read_board_for_B2():
    B2 = (5, [wb1, wk1, bk1, bb1, bb2, wb3])

    B = read_board("board_examp_b2.txt")
    assert B[0] == 5

    for piece in B[1]:
        found = False
        for piece1 in B2[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found

    for piece1 in B2[1]:
        found = False
        for piece in B[1]:
            if piece.pos_x == piece1.pos_x and piece.pos_y == piece1.pos_y and piece.side == piece1.side and type(
                    piece) == type(piece1):
                found = True
        assert found
