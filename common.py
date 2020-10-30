import random


game_board = [i for i in range(9)]          # contains the current state of the came
available_plays = [i for i in range(9)]     # contains the available plays


def game_not_finished(board, sign):
    """
    Verifies if a player has already won, this function is called after each play.

    :param board: list containing current state of the game
    :param sign: the sign that was previously played
    :return: a boolean: True if the game has to continue and False if the game has to stop, the sign previously played
    """
    full = True     # loop statement

    if len(available_plays) > 0:
        full = False

    if board[0] == board[1] == board[2] or board[3] == board[4] == board[5] or board[6] == board[7] == board[8] or board[0] == board[3] == board[6] or board[1] == board[4] == board[7] or board[2] == board[5] == board[8] or board[0] == board[4] == board[8] or board[2] == board[4] == board[6]:
        return False, sign

    elif full:
        return False, "full"

    else:
        return True, ""


def show_play_board(board):
    """
    Prints the current state of the board to the screen

    :param board: list containing current state of the game
    :return:
    """
    print("+", "+", "+", "+", sep='-------')
    print("|       |       |       |")
    print(f"|   {board[0]}", board[1], f"{board[2]}   |", sep='   |   ')
    print("|       |       |       |")
    print("+", "+", "+", "+", sep='-------')
    print("|       |       |       |")
    print(f"|   {board[3]}", board[4], f"{board[5]}   |", sep='   |   ')
    print("|       |       |       |")
    print("+", "+", "+", "+", sep='-------')
    print("|       |       |       |")
    print(f"|   {board[6]}", board[7], f"{board[8]}   |", sep='   |   ')
    print("|       |       |       |")
    print("+", "+", "+", "+", sep='-------')


def random_number(begin=0, end=10, step=1):
    """
    Generates a random number from 'begin' to 'end' with a step of 'step'
    :param begin: range begins from this argument
    :param end: range ends from this argument
    :param step: step of the numbers
    :return: either a random float or int, depending on the inputs
    """
    if isinstance(begin, float) and isinstance(end, float):
        return random.uniform(begin, end)

    elif isinstance(begin, int) and isinstance(end, int) and isinstance(step, int):
        return random.randrange(begin, end, step)

    else:
        print("Values entered were not accepted, inputs must be either int or float and must be of the same class !")


def player_plays(player_name, sign):
    """
    Lets the player input the number of the case he wants to check
    :param player_name: name of the player that is playing
    :param sign: sign of the player that is playing
    :return: None
    """
    invalid_play = True     # loop statement
    play = ""               # variable will contain the players play

    print(f"Your turn {player_name} !")

    # As long as there is no valid entry, the loop keeps asking for a number
    while invalid_play:
        play = input("Enter the number of the box you want to mark : ")

        try:
            play = int(play)

            if play not in available_plays:
                raise ValueError

            else:
                available_plays.remove(play)
                invalid_play = False

        except ValueError:
            print("The value entered was not accepted, please try again...")

    game_board[play] = sign
    show_play_board(game_board)
