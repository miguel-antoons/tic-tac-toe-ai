import pandas
import copy
import pymysql
from sqlalchemy import create_engine
from configparser import ConfigParser
from utilities import security


turns = []              # list of instances of the PlayerMove class
database_tables = []    # list of database tables in dataframe form


class PlayerMove:
    """
    Represents a move performed by a Player
    """
    def __init__(self, sign: str, turn_n: int, move: int, result=0.0):
        self.__sign = sign      # sign of the Player which made the move
        self.__turn_n = turn_n  # turn number
        self.__move = move      # the move performed by the Player
        self.__result = result  # the result of the move (1 = win, 0 = loss)

    @property
    def sign(self):
        return self.__sign

    @property
    def turn_n(self):
        return self.__turn_n

    @property
    def move(self):
        return self.__move

    @property
    def result(self):
        return self.__result

    @result.setter
    def result(self, result):
        self.__result = result

    def __str__(self):
        return f"turn_n: {self.__turn_n}\tmove: {self.__move}\tresult: {self.__result}"


def load_dataframe_from_sql():
    """
    Loads the tables from the database into dataframes
    :return: True if there is a database, False if not
    """
    database_connection = create_connection()
    if database_connection:
        for i in range(1, 9):
            database_tables.append(pandas.read_sql(f"SELECT * from turn_{i}", database_connection))

        database_connection.close()
        return True

    else:
        return False


def create_connection():
    """
    Returns a connection to the artificial intelligence database
    :return: the connection if no failure occurred, otherwise the function returns False
    """
    # read the configuration file
    security.decrypt_file("program_files/config.ini")
    configuration_content = ConfigParser()
    configuration_content.read("program_files\\config.ini")
    security.encrypt_file("program_files/config.ini")

    # try to make a connection
    try:
        return create_engine(f"mysql+pymysql://{configuration_content['database_login']['username']}:"
                             f"{configuration_content['database_login']['password']}@127.0.0.1/tictactoe").connect()

    # if no database exists, return False
    except Exception:
        return False


def ai_move():
    """
    Function represents a player with an artificial intelligence and calculates the best move to perform
    :return: The best move to perform or 'NOT_FOUND' if no good move was found
    """
    security.decrypt_file("program_files/config.ini")
    configuration_content = ConfigParser()
    configuration_content.read("program_files/config.ini")
    security.encrypt_file("program_files/config.ini")

    # take the the correct dataframe (according to the turn number)
    try:
        dataframe = copy.copy(database_tables[len(turns)])

    # if there is no dataframe in the list (because there is no database) return 'NOT_FOUND'
    except IndexError:
        return "NOT_FOUND"

    # filter the dataframe in order to get the correct combinations
    for i, turn in enumerate(turns):
        dataframe = dataframe.loc[dataframe[f"turn_{i + 1}"] == turn.move]

    # select the move with the highest probability
    highest_probability = dataframe["probability"].max()

    # if this probability is higher than epsilon, store the play in the turns list
    if highest_probability > float(configuration_content["system_var"]["epsilon"]):
        play = dataframe.loc[dataframe["probability"] == highest_probability, ["play"]].iloc[0].play.item()
        if (len(turns) + 1) % 2:
            sign = "O"
        else:
            sign = "X"

        turns.append(PlayerMove(sign, len(turns) + 1, play))
        return turns[-1].move
    else:
        return "NOT_FOUND"


def update_ai_database():
    """
    Writes the game over to the dataframes stored in the RAM
    :return: None
    """
    # change the epsilon value, since new experience is acquired
    security.decrypt_file("program_files/config.ini")
    configuration_content = ConfigParser()
    configuration_content.read("program_files/config.ini")
    configuration_content.set("system_var", "epsilon", str(float(configuration_content["system_var"]["epsilon"])
                                                           - 0.00000133))

    # write the changes to the configuration file
    with open("program_files/config.ini", "w") as config_file:
        configuration_content.write(config_file)

    security.encrypt_file("program_files/config.ini")

    # iterate over the turns played
    for i, turn in enumerate(turns):
        try:
            dataframe = copy.copy(database_tables[i])
        except IndexError:
            return None

        # filter until we have the corresponding move
        for j in range(i):
            dataframe = dataframe.loc[dataframe[f"turn_{j + 1}"] == turns[j].move]
        dataframe = dataframe.loc[dataframe["play"] == turn.move]

        # check if the move already exists
        if dataframe.empty:
            # if it doesn't exist, create and initialize it
            new_data = {"play": turn.move}
            for j in range(i):
                new_data[f"turn_{j + 1}"] = turns[j].move
            new_data["probability"] = turn.result
            new_data["n_references"] = 1
            database_tables[i] = database_tables[i].append(new_data, ignore_index=True)

        else:
            # if it already exists, update the values
            probability = dataframe.iloc[0].probability.item()
            n_references = dataframe.iloc[0].n_references.item()
            probability = (n_references * probability + turn.result) / (n_references + 1)
            n_references += 1
            database_tables[i].at[dataframe.index[0], "probability"] = probability
            database_tables[i].at[dataframe.index[0], "n_references"] = n_references


def write_to_database():
    """
    Writes the content of the 'database_tables' to the on disk database
    :return: None
    """
    database_connection = create_connection()

    if database_connection:
        for i, table in enumerate(database_tables):
            name = f"turn_{i + 1}"
            table.to_sql(name, con=database_connection, if_exists='replace', index=False)

        database_connection.close()


if __name__ == "__main__":
    ai_move()
