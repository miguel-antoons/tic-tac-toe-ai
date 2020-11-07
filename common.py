import random
# import AI
from os import system


clear = lambda: system('cls')


class game:
    """
    Defines the game state and all the functions related to the game
    """
    def __init__(self):
        self.__board_status = [i for i in range(9)]
        self.__available_plays = [i for i in range(9)]
        self.__round_nb = 0
        self.__end = False

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
        if (moving_player.sign == "X" and not self.__round_nb % 2) or (moving_player.sign == "O" and self.__round_nb % 2) or self.__end:
            return False

        try:
            index = int(index)
        except ValueError:
            return True

        if index in self.__board_status:
            self.__round_nb += 1
            self.__board_status[index] = moving_player.sign
            self.__available_plays.remove(index)
            self.print_board()
            self.__check_winner(moving_player)

            # AI.turns.append(AI.player_move(moving_player.sign, self.__round_nb, index))
            return False
        else:
            return True

    def print_board(self):
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
        if self.__board_status[0] == self.__board_status[1] == self.__board_status[2] or self.__board_status[3] == self.__board_status[4] == self.__board_status[5] or self.__board_status[6] == self.__board_status[7] == self.__board_status[8] or self.__board_status[0] == self.__board_status[3] == self.__board_status[6] or self.__board_status[1] == self.__board_status[4] == self.__board_status[7] or self.__board_status[2] == self.__board_status[5] == self.__board_status[8] or self.__board_status[0] == self.__board_status[4] == self.__board_status[8] or self.__board_status[2] == self.__board_status[4] == self.__board_status[6]:
            pot_winner.winner = True
            self.__end = True
        elif not any(i in [0, 1, 2, 3, 4, 5, 6, 7, 8] for i in self.__board_status):
            pot_winner.winner = "full"
            self.__end = True


class player:
    """
    Defines a player's property for in game use
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
        print("Values entered were not accepted, inputs must be either int or float and must be of the same class !")


def announce_winner(player_1, player_2):
    """
    Checks which of the 2 players has win and prints the result on the screen

    :param player_1: {class player}
    :param player_2: {class player}
    :return: {None}
    """
    if (player_1.winner or player_2.winner) == "full":
        print("It's a tie !")

    elif player_1.winner:
        print(f"Congratulations, {player_1.user_name} won !")
        """
        for turn in AI.turns:
            if turn.sign == player_1.sign:
                turn.result = 1
        """

    elif player_2.winner:
        print(f"Congratulations, {player_2.user_name} won !")
        """
        for turn in AI.turns:
            if turn.sign == player_2.sign:
                turn.result = 1
        """

    # AI.update_ai_database()
