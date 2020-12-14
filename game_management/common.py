import random
import math
from datetime import datetime
from game_management import scores
from game_management import AI
from gui import interface
from os import system


class Game:
    """
    Defines the Game state and all the functions related to the Game
    """
    def __init__(self, gui=False):
        self.__board_status = [i for i in range(9)]     # represents the game board
        self.__available_plays = [i for i in range(9)]  # contains the available plays
        self.__round_nb = 0                             # round number of the game
        self.__end = False                              # True if the game comes to an ending
        self.__gui = gui

    @property
    def round_nb(self):
        return self.__round_nb

    @property
    def end(self):
        return self.__end

    @property
    def available_plays(self):
        return self.__available_plays

    def make_move(self, index, moving_player):
        """
        Makes changes to the game board
        :param index: the play the player wants to perform
        :param moving_player: the player who performs the play
        :return: True if the play is invalid
        """
        if (moving_player.sign == "X" and not self.__round_nb % 2) or \
                (moving_player.sign == "O" and self.__round_nb % 2) or self.__end:
            return False

        # check if the play is an integer
        try:
            index = int(index)
        except ValueError:
            return True

        # check if the play is valid
        if index in self.__board_status:
            self.__round_nb += 1
            self.__board_status[index] = moving_player.sign
            self.__available_plays.remove(index)
            self.print_board()
            self.print_board()
            self.__check_winner(moving_player)
            if 9 > self.__round_nb > len(AI.turns):
                AI.turns.append(AI.PlayerMove(moving_player.sign, self.__round_nb, index))
            return False

        else:
            return True

    def print_board(self):
        if self.__gui:
            interface.Grille().update()
        else:
            clear()
            print("+", "+", "+", "+", sep='-------')
            print("|       |       |       |")
            print(f"|   {self.__board_status[0]}", self.__board_status[1], f"{self.__board_status[2]}   |", sep='   |   ')
            print("|       |       |       |")
            print("+", "+", "+", "+", sep='-------')
            print("|       |       |       |")
            print(f"|   {self.__board_status[3]}", self.__board_status[4], f"{self.__board_status[5]}   |", sep='   |   ')
            print("|       |       |       |")
            print("+", "+", "+", "+", sep='-------')
            print("|       |       |       |")
            print(f"|   {self.__board_status[6]}", self.__board_status[7], f"{self.__board_status[8]}   |", sep='   |   ')
            print("|       |       |       |")
            print("+", "+", "+", "+", sep='-------')

    def __check_winner(self, pot_winner):
        """
        Checks if the player entered as argument has won
        :param pot_winner: player that played last
        :return: None
        """
        if self.__board_status[0] == self.__board_status[1] == self.__board_status[2] or self.__board_status[3] == \
                self.__board_status[4] == self.__board_status[5] or self.__board_status[6] == self.__board_status[7] \
                == self.__board_status[8] or self.__board_status[0] == self.__board_status[3] == \
                self.__board_status[6] or self.__board_status[1] == self.__board_status[4] == self.__board_status[7] \
                or self.__board_status[2] == self.__board_status[5] == self.__board_status[8] or \
                self.__board_status[0] == self.__board_status[4] == self.__board_status[8] or self.__board_status[2]\
                == self.__board_status[4] == self.__board_status[6]:
            pot_winner.winner = True
            self.__end = True

        elif not any(i in [0, 1, 2, 3, 4, 5, 6, 7, 8] for i in self.__board_status):
            pot_winner.winner = "full"
            self.__end = True


game = Game()


class Player:
    """
    Defines a Player's property for in Game use
    """
    def __init__(self, user_name, sign=""):
        self.__user_name = user_name
        self.__sign = sign
        self.__winner = False

    @property
    def user_name(self):
        return self.__user_name

    @property
    def sign(self):
        return self.__sign

    @property
    def winner(self):
        return self.__winner

    @sign.setter
    def sign(self, sign):
        self.__sign = sign

    @winner.setter
    def winner(self, status=True):
        self.__winner = status


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
        raise ValueError


def announce_winner(player_1, player_2):
    """
    Checks which of the 2 players has win and prints the result on the screen

    :param player_1: {class Player}
    :param player_2: {class Player}
    :return: {None}
    """
    winner = ""

    # check what the end status of the game is
    if (player_1.winner or player_2.winner) == "full":
        print("It's a tie !")

        for turn in AI.turns:
            turn.result = 0.5

        AI.update_ai_database()
        return None

    elif player_1.winner:
        winner = player_1

    elif player_2.winner:
        winner = player_2

    # print a message adapted to the winner
    if not winner.user_name == "computer":
        scores.all_scores.append(scores.Score(winner.user_name, winner.sign, math.ceil(game.round_nb / 2),
                                              datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        scores.all_scores[-1].save_score()
        print(f"Congratulations, {winner.user_name} won with a score of "
              f"{scores.all_scores[-1].return_calculated_score()}!")

    else:
        print("The computer won...")

    # update the probability of the moves that were played
    for turn in AI.turns:
        if turn.sign == winner.sign:
            turn.result = 1.0
        else:
            turn.result = 0.0

    AI.update_ai_database()
    AI.write_to_database()


def clear():
    system('cls')
