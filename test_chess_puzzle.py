import pytest

from test_utils import *
from chess_puzzle import *


def test_location2index1():
    assert location2index("e2") == (5, 2)


def test_location2indexCaseMax():
    assert location2index("z26") == (26, 26)


def test_location2indexCaseMin():
    assert location2index("a1") == (1, 1)


def test_location2indexCaseNgFormat():
    # out of 26
    assert location2index("a27") == ()
    # out of 26
    assert location2index("a0") == ()
    # not start alfabet
    assert location2index("02") == ()
    # including not int
    assert location2index("a") == ()
    # including not int
    assert location2index("ab") == ()
    # whether is capital permitted
    assert location2index("A1") == ()


def test_index2location1():
    assert index2location(5, 2) == "e2"


def test_index2locationMax():
    assert index2location(26, 26) == "z26"


def test_index2locationMin():
    assert index2location(1, 1) == "a1"


def test_index2locationdexCaseNgRange():
    assert index2location(1, 0) == ""
    assert index2location(0, 1) == ""
    assert index2location(27, 1) == ""
    assert index2location(1, 27) == ""


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


def test_is_piece_at_case_exist_black_king():
    assert is_piece_at(2, 3, B1) == True


def test_is_piece_at_case_exist_black_bishop():
    assert is_piece_at(5, 3, B1) == True


def test_is_piece_at_case_exist_white_king():
    assert is_piece_at(3, 5, B1) == True


def test_is_piece_at_case_exist_white_bishop():
    assert is_piece_at(2, 5, B1) == True


def test_piece_at_b1():
    assert piece_at(3, 3, B1) == bb1


def test_piece_at_black_king():
    assert piece_at(2, 3, B1) == bk1


def test_piece_at_black_bishop():
    assert piece_at(5, 3, B1) == bb2


def test_piece_at_white_king():
    assert piece_at(3, 5, B1) == wk1


def test_piece_at_white_bishop():
    assert piece_at(3, 1, B1) == wb3


def test_piece_at_for_false_side():
    assert piece_at(3, 3, B1) != wb1


def test_piece_at_for_true_side():
    assert piece_at(5, 3, B1) == bb2


def test_can_reach1():
    assert wb2.can_reach(5, 5, B1) == True


def test_can_reach_bishoptest_can_reach_bishop_for_diagonal_ok_but_the_same_side_for_diagonal_ok_but_the_same_side():
    assert wb2.can_reach(3, 5, B1) == False


def test_can_reach_bishop_for_diagonal_ok_and_the_opponent_side():
    assert wb2.can_reach(5, 3, B1) == True
    assert bb1.can_reach(4, 4, B1) == True


def test_can_reach_bishop_can_reach_for_not_diagonal_ng():
    assert wb1.can_reach(1, 3, B1) == False


def test_can_reach_bishop_can_reach_for_the_opponent_side_but_there_are_opponent_piece_between_them():
    assert bb1.can_reach(5, 5, B1) == False


def test_can_reach_bishop_for_firstly_same():
    assert wb2.can_reach(4, 4, B1) == False


def test_can_reach_bishop_for_over_range_for_board():
    assert wb2.can_reach(6, 6, B1) == False
    assert wb1.can_reach(1, 6, B1) == False


def test_is_diagonal():
    assert bb1.is_diagonal(5, 5) == True
    assert bb1.is_diagonal(1, 5) == True
    assert bb1.is_diagonal(5, 1) == True
    assert bb1.is_diagonal(1, 1) == True
    assert bb1.is_diagonal(1, 2) == False


def test_get_direction():
    assert bb1.get_direction(5, 5) == (1, 1)
    assert bb1.get_direction(1, 5) == (-1, 1)
    assert bb1.get_direction(5, 1) == (1, -1)
    assert bb1.get_direction(1, 1) == (-1, -1)


def test_get_direction_false():
    assert bb1.get_direction(1, 3) == False


def test_is_out_board():
    assert is_out_board(1, 1, B1) == False
    assert is_out_board(5, 5, B1) == False
    assert is_out_board(6, 1, B1) == True
    assert is_out_board(1, 0, B1) == True
    assert is_out_board(1, 6, B1) == True
    assert is_out_board(0, 1, B1) == True


def test_can_reach_king_vertical():
    assert wk1.can_reach(3, 4, B1) == True
    assert wk1.can_reach(4, 5, B1) == True
    assert wk1.can_reach(4, 6, B1) == True


def test_can_reach_king_for_more_than_two():
    assert wk1.can_reach(3, 7, B1) == False


def test_can_reach_king_for_the_same_side():
    assert wk1.can_reach(4, 4, B1) == False


def test_can_reach_for_wb_beside_opponent_k():
    wb_besides_opponent_k = Bishop(2, 2, True)
    B_case_of_wb_besides_opponent_k = (5, [wb1, bb1, wb2, bb2, wb3, wk1, bk1, wb_besides_opponent_k])
    assert bk1.can_reach(2, 2, B_case_of_wb_besides_opponent_k) == True


def test_can_move_to1():
    assert wb2.can_move_to(5, 5, B1) == False


def test_can_move_to_for_bishop_ok():
    wk_moved = King(4, 1, True)
    B_moved_wk_for_ok = (5, [wb1, bb1, wb2, bb2, wb3, wk_moved, bk1])
    assert wb2.can_move_to(5, 5, B_moved_wk_for_ok) == True


def test_can_move_to_for_bishop_ng():
    wk_moved = King(4, 1, True)
    B_moved_wk_for_ok = (5, [wb1, bb1, wb2, bb2, wb3, wk_moved, bk1])
    assert wb2.can_move_to(3, 4, B_moved_wk_for_ok) == False


def test_can_move_to_for_king_ok():
    assert wk1.can_move_to(4, 5, B1) == True


def test_can_move_to_for_king_ng():
    assert wk1.can_move_to(3, 4, B1) == False

    bk_moved = King(2, 2, False)
    B_wk_moved_for_ok = (5, [wb1, bb1, wb2, bb2, wb3, wk1, bk_moved])
    assert wk1.can_move_to(3, 4, B_wk_moved_for_ok) == True


def test_can_move_to_beat_opponent_king():
    B = read_board("to_beat_opponent_king.txt")
    prev_piece = piece_at(5, 2, B)
    assert prev_piece.can_move_to(4, 2, B) == True


def test_move_to1():
    wb2a = Bishop(3, 3, True)
    Actual_B = wb2.move_to(3, 3, B1)
    Expected_B = (5, [wb2a, wb1, wk1, bk1, bb2, wb3])

    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

    comparing_boards(Expected_B, Actual_B)


def test_move_to_for_bishop_not_beat_opponent():
    wb2a2 = Bishop(5, 5, True)
    Actual_B = wb2.move_to(5, 5, B1)
    Expected_B = (5, [wb2a2, wb1, bb1, wk1, bk1, bb2, wb3])

    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

    comparing_boards(Expected_B, Actual_B)


def test_move_to_for_king():
    wk1_after = King(4, 5, True)
    Actual_B = wk1.move_to(4, 5, B1)
    Expected_B = (5, [wb1, bb1, wb2, bb2, wb3, wk1_after, bk1])

    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

    comparing_boards(Expected_B, Actual_B)


def test_move_to_for_king_beat_opponent():
    bk1_after = King(2, 3, False)
    wb_got = Bishop(2, 3, True)
    B_Before = (5, [wb1, bb1, wb2, bb2, wb3, wk1, bk1, wb_got])

    Actual_B = bk1.move_to(2, 3, B_Before)
    # not exist wb_getted
    Expected_B = (5, [wb1, bb1, wb2, bb2, wb3, wk1, bk1_after])

    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

    comparing_boards(Expected_B, Actual_B)


def test_build_new_board():
    wb2a = Bishop(3, 3, True)
    Actual_B = wb2.build_new_board(3, 3, B1)
    Expected_B = (5, [wb2a, wb1, wk1, bk1, bb2, wb3])

    # check if actual board has same contents as expected
    assert Actual_B[0] == 5

    comparing_boards(Expected_B, Actual_B)


def test_remove_piece_from_board():
    # wb2a = Bishop(3, 3, True)
    new_list = wb2.remove_piece_from_board(3, 3, B1)
    Actual_B = (5, new_list)
    Expected_B = (5, [wb1, wk1, bk1, bb2, wb3])
    comparing_boards(Expected_B, Actual_B)


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
    assert is_checkmate(True, B3) == False


def test_is_checkmate_for_ng1():
    B3_fixed_for_false = (5, [wk1a, wb4, bk1, bb2, wb3, wb5])
    assert is_checkmate(False, B3_fixed_for_false) == False
    assert is_checkmate(True, B3_fixed_for_false) == False


def test_is_checkmate_for_ng2():
    wk = King(1, 1, True)
    bb = Bishop(1, 2, False)
    bk = King(2, 3, False)
    B_stalemate = (26, [wk, bb, bk])
    assert is_checkmate(True, B_stalemate) == False
    assert is_checkmate(False, B_stalemate) == False


def test_is_stalemate_true():
    wk = King(1, 1, True)
    bb = Bishop(1, 2, False)
    bk = King(2, 3, False)
    B_stalemate = (26, [wk, bb, bk])
    assert is_stalemate(True, B_stalemate) == True
    assert is_stalemate(False, B_stalemate) == False


def test_is_stalemate_False1():
    wk = King(1, 1, True)
    bb = Bishop(1, 2, False)
    bk = King(3, 3, False)
    B_stalemate = (5, [wk, bb, bk])
    assert is_stalemate(True, B_stalemate) == False
    assert is_stalemate(False, B_stalemate) == False


def test_is_stalemate_false2():
    wk = King(1, 1, True)
    bb = Bishop(1, 2, False)
    bk = King(4, 3, False)
    B_stalemate = (5, [wk, bb, bk])
    assert is_stalemate(True, B_stalemate) == False

    assert is_stalemate(False, B_stalemate) == False


def test_is_make_moving_anywhere():
    wk = King(1, 1, True)
    bb = Bishop(1, 2, False)
    bk = King(2, 3, False)
    B = (26, [wk, bb, bk])
    assert is_make_moving_anywhere(True, B) == True
    assert is_make_moving_anywhere(False, B) == False


def test_read_board1():
    B = read_board("board_examp.txt")
    assert B[0] == 5

    comparing_boards(B, B1)


def test_read_board_for_big():
    bb_big = Bishop(26, 26, False)
    B2 = (26, [wb1, wk1, bk1, bb1, bb2, wb3, bb_big])

    B = read_board("board_examp_b2.txt")
    assert B[0] == 26

    comparing_boards(B, B2)


def test_read_board_for_min():
    wb = Bishop(3, 2, True)
    wk = King(3, 3, True)
    bk = King(1, 1, False)
    B_actual = (3, [wb, wk, bk])

    B_expected = read_board("board_examp_b_min3.txt")
    assert B_expected[0] == 3

    comparing_boards(B_expected, B_actual)


def test_read_board_for_check_situation():
    wk = King(1, 1, True)
    bb_1 = Bishop(3, 3, False)
    bk = King(1, 5, False)
    bb_2 = Bishop(3, 2, False)
    B2 = (5, [wk, bb_1, bk, bb_2])

    B = read_board("check_situation.txt")
    assert B[0] == 5

    comparing_boards(B, B2)


def test_read_board_ng():
    with pytest.raises(IOError):
        read_board("board_examp_invalid_for_few_board_size.txt")
    with pytest.raises(IOError):
        read_board("board_examp_invalid_for_too_large_board_size.txt")
    with pytest.raises(IOError):
        read_board("board_examp_invalid_form.txt")
    with pytest.raises(IOError):
        read_board("board_examp_less_line.txt")
    with pytest.raises(IOError):
        read_board("board_examp_too_many_line.txt")
    with pytest.raises(IOError):
        read_board("notExist.txt")


def test_construct_format_lines():
    with open('board_examp.txt', 'r') as file:
        lines = file.readlines()
    plain_format_lines = construct_format_lines(lines)
    assert plain_format_lines == [['5'], ['Bb5', 'Kc5', 'Bd4', 'Bc1'], ['Kb3', 'Bc3', 'Be3']]


def test_construct_format_lines_case_dot_space():
    with open('board_examp_add_dot.txt', 'r') as file:
        lines = file.readlines()
    plain_format_lines = construct_format_lines(lines)
    assert plain_format_lines == [['5'], ['Bb5', 'Kc5', 'Bd4', 'Bc1'], ['Kb3', 'Bc3', 'Be3']]


def test_construct_format_lines_ng():
    with open('board_examp_empty_line.txt', 'r') as file:
        lines = file.readlines()
    with pytest.raises(IOError):
        construct_format_lines(lines)


def test_set_board_size():
    board_size_line = ["9"]
    assert set_board_size(board_size_line) == 9
    board_size_line = ["3"]
    assert set_board_size(board_size_line) == 3
    board_size_line = ["26"]
    assert set_board_size(board_size_line) == 26


def test_set_board_size_ng():
    board_size_line = ["2"]
    with pytest.raises(IOError):
        set_board_size(board_size_line)
    board_size_line = ["27"]
    with pytest.raises(IOError):
        set_board_size(board_size_line)
    board_size_line = []
    with pytest.raises(IOError):
        set_board_size(board_size_line)
    board_size_line = ["26", "4"]
    with pytest.raises(IOError):
        set_board_size(board_size_line)


def test_save_board():
    filename = "board_examp_write.txt"

    save_board(filename, B1)
    B = read_board(filename)
    comparing_boards(B, B1)
