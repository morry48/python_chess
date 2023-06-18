from chess_rule import *


def main() -> None:
    """
    runs the play

    Hint: implementation of this could start as follows:
    filename = input("File name for initial configuration: ")
    ...
    """
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
