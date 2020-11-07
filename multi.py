import common


def multi_play():
    """
    Runs the multiplayer mode
    :return: None
    """
    game = common.game()                                      # loop statement (bool: shows if the game is done or not, string: shows the winning sign)
    multi_player_1 = common.player(input("Enter the name of the first player : "), "O")   # name of the first player
    multi_player_2 = common.player(input("Enter the name of the second player : "), "X")  # name of the second player

    print(f"{multi_player_1.user_name} will represent the {multi_player_1.sign} plays and {multi_player_2.user_name} will represent the {multi_player_2.sign} plays.\n")

    input("Press any key to continue...")

    print("Let's begin !")
    game.print_board()

    # As long as the game is unfinished, the loop will continue
    while not game.end:
        for i in [multi_player_1, multi_player_2]:
            while not game.end and game.make_move(input(f"Your turn {i.user_name} !\nEnter a number : "), i):
                pass

    common.announce_winner(multi_player_1, multi_player_1)
