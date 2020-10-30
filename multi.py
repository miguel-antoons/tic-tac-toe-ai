import common


def multi_play():
    """
    Runs the multiplayer mode
    :return: None
    """
    unfinished = (True, "")                                         # loop statement (bool: shows if the game is done or not, string: shows the winning sign)
    name_player1 = input("Enter the name of the first player : ")   # name of the first player
    name_player2 = input("Enter the name of the second player : ")  # name of the second player

    print(f"{name_player1} will represent the 'O' plays and {name_player2} will represent the 'X' plays.\n")

    if input("Press any key to continue..."):
        pass

    print("Let's begin !")
    common.show_play_board(common.game_board)

    # As long as the game is unfinished, the loop will continue
    while unfinished[0]:
        common.player_plays(name_player1, "O")
        unfinished = common.game_not_finished(common.game_board, "O")

        if unfinished[0]:
            common.player_plays(name_player2, "X")
            unfinished = common.game_not_finished(common.game_board, "X")

    if unfinished[1] == "O":
        print(f"Congratulations, {name_player1} won !")

    elif unfinished[1] == "X":
        print(f"Congratulations {name_player2}, you won !")

    else:
        print("It's a tie...")
