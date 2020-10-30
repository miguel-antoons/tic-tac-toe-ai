import common


def single_play():
    """
    Runs the single play mode
    :return: None
    """
    incorrect_sign = True                       # loop statement
    unfinished = (True, False)                  # loop statement
    computer_sign = ""                          # sign the computer will use
    player_sign = ""                            # sign the player will use
    name_player = input("Enter your name : ")   # name of the human player

    # As long as there is no valid entry, the loop keeps asking which sign the player wants
    while incorrect_sign:
        incorrect_sign = False
        player_sign = input("Enter the sign you want to play (O begins first) : ")

        if player_sign == "O":
            computer_sign = "X"

        elif player_sign == "X":
            computer_sign = "O"

        else:
            incorrect_sign = True

    print(f"{name_player}, you will represent the {player_sign} plays and the computer will represent the {computer_sign} plays.\n")

    if input("Press any key to continue..."):
        pass

    print("Let's begin !")
    common.show_play_board(common.game_board)

    # As long as there is no winner, the game continues
    while unfinished[0]:
        if player_sign == "O":
            common.player_plays(name_player, "O")
            unfinished = common.game_not_finished(common.game_board, player_sign)

            if unfinished[0]:
                computer_plays(computer_sign)
                unfinished = common.game_not_finished(common.game_board, computer_sign)

        else:
            computer_plays(computer_sign)
            unfinished = common.game_not_finished(common.game_board, computer_sign)

            if unfinished[0]:
                common.player_plays(name_player, "X")
                unfinished = common.game_not_finished(common.game_board, player_sign)

    if unfinished[1] == player_sign:
        print(f"Congratulations, {name_player} won !")

    elif unfinished[1] == computer_sign:
        print(f"Looser, the computer won !")

    else:
        print("It's a tie...")


def computer_plays(sign):
    """
    This function will execute the choice of the computer
    :param sign: the sign the computer is playing with
    :return: None
    """
    play = common.available_plays[common.random_number(end=len(common.available_plays))]    # variable contains the play the computer will execute
    print("Computer's turn !")
    print(f"The computer chose number {common.game_board[play]}")
    common.game_board[play] = sign                                                          # execution of the play
    common.available_plays.remove(play)                                                     # the play is removed from the available plays
    common.show_play_board(common.game_board)
