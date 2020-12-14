import csv
from utilities import security


all_scores = []     # list which will contain all the scores


class Score:
    """
    Represents a score
    """
    def __init__(self, player: str, sign: str, moves: int, date: str):
        self.__user_name = player
        self.__sign = sign
        self.__n_moves = moves
        self.__date = date

    def return_calculated_score(self):
        """
        returns the score
        :return: the calculated score
        """
        return self.__calculate_score()

    def __calculate_score(self):
        """
        calculates the score
        :return: the calculated score
        """
        if self.__sign == "O":
            return int(round((((self.__n_moves ** -1) * 10000) * 7 / 1000)))
        else:
            return int(round((((self.__n_moves ** -1) * 10000) * 10 / 1000)))

    def save_score(self):
        """
        Saves the score inside the scores.csv file
        :return: None
        """
        new_score = {
            "player_name": self.__user_name,
            "sign": self.__sign,
            "n_moves": self.__n_moves,
            "date": self.__date,
        }

        security.decrypt_file("program_files/scores.csv")

        # append the new score to the scores.csv file
        with open("program_files\\scores.csv", "a+", newline="") as csv_login_file:
            fieldnames = ["player_name", "sign", "n_moves", "date"]
            csv_writer = csv.DictWriter(csv_login_file, fieldnames=fieldnames)

            csv_writer.writerow(new_score)

        security.encrypt_file("program_files/scores.csv")

    def __str__(self):
        return "{:40} {:25} {:10}".format(self.__user_name, self.__date, str(self.__calculate_score()))


def load_scores():
    """
    Load the scores into the RAM with an array
    :return: None
    """
    security.decrypt_file("program_files/scores.csv")

    with open("program_files/scores.csv", "r") as score_file:
        csv_file_content = csv.DictReader(score_file)

        for score_instance in csv_file_content:
            all_scores.append(Score(score_instance["player_name"], score_instance["sign"],
                                    int(score_instance["n_moves"]), score_instance["date"]))

    security.encrypt_file("program_files/scores.csv")


def print_scores():
    """
    Sorts the scores and prints it
    :return: None
    """
    sorted_scores = sort_scores()

    print("\n{:4} {:40} {:25} {:10}\n".format("Nr", "Username", "Date", "Score"))

    for i in range(25):
        try:
            print("{:4}".format(str(i + 1)), sorted_scores[i])
        except IndexError:
            break


def sort_scores():
    """
    Sorts the score
    :return: the sorted list
    """
    return sorted(all_scores, key=return_score, reverse=True)


def return_score(elem):
    return elem.return_calculated_score()


if __name__ == "__main__":
    load_scores()
    print_scores()
