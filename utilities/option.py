import csv
import mysql.connector
import installation
import os
import pandas
from configparser import ConfigParser
from user_management import user
from game_management import common, AI
from utilities import security


def option():
    """
    Entry point of the 'option' command line.
    From this point the user (which has to be an administrator) will be able to change user settings as well
    as system settings.
    :return: None
    """
    print("You are now in option mode")
    print("Enter command one by one")
    print("Use the 'help' command for more information")

    # verify if the user is the super-administrator
    security.decrypt_file("program_files/config.ini")
    configuration_content = ConfigParser()
    configuration_content.read("program_files/config.ini")
    admin = configuration_content["user_info"]["admin"] == user.current_user.user_name
    security.encrypt_file("program_files/config.ini")

    # while the user wants to enter new commands, repeat
    while True:
        # splits the command at each space
        command = input("\n/tictactoe_AI/option# ").split()
        command[0] = command[0].upper()

        # usernames are case-sensitive, so they must not be transformed
        if command[0] in ["SHOW", "CHEPSILON"]:
            command[1] = command[1].upper()

        # conditions check which command has been entered
        if command[0] == "HELP":
            # show the list of all the commands with their arguments and manuals
            align_character = "\n\t" + 42 * " "
            print("\nWelcome to the command line\n")
            print("Here is a list of the commands you can use :\n")
            print("\t{:20} {:20} {:100}\n".format("Command", "Argument(s)", f"Manual"))
            print("\t{:20} {:20} {:100}".format("autofill", "[None]",
                                                f"Fills the artificial intelligence's database with all "
                                                f"{align_character}the possible game combinations\n"))
            print("\t{:20} {:20} {:100}\n".format("deluser", "[username]",
                                                  "Deletes the user with the username entered as argument\n"))
            print("\t{:20} {:20} {:100}\n".format("chepsilon", "[new_epsilon]",
                                                  f"Changes the epsilon variable of the artificial intelligence, "
                                                  f"{align_character}this value will change the chances whether the ai "
                                                  f"will use a {align_character}random number or its database "
                                                  f"resources\n"))
            print("\t{:20} {:20} {:100}\n".format("mtyscores", "[None]",
                                                  "Empties the score csv file and creates a new one"))
            print("\t{:20} {:20} {:100}\n".format("show", "[File / Table]",
                                                  f"Show the file (login, score, config) or the table (turn_1, "
                                                  f"{align_character}turn_2, turn_3, turn_4, turn_5, turn_6, turn_7, "
                                                  f"turn_8) {align_character}entered as argument. {align_character}"
                                                  f"Some files may only be accessed by the super-admin of the program"
                                                  f"."))
            print("\t{:20} {:20} {:100}\n".format("back", "[None]", f"Goes back to the previous menu"))
            print("\t{:20} {:20} {:100}\n".format("exit", "[None]", f"Exits and closes the whole program"))
            print("\t{:20} {:20} {:100}\n".format("reboot", "[None]", f"Reboots the whole program"))

            if admin:
                # shows the commands for the super-administrator
                print("\t{:20} {:20} {:100}\n".format("setadmin", "[username]",
                                                      f"Sets the user, with the username entered as argument, as "
                                                      f"{align_character}an admin of the program"))
                print("\t{:20} {:20} {:100}\n".format("reinit", "[None]", f"Reinstall the whole program"))
                print("\t{:20} {:20} {:100}\n".format("mtydb", "[None]",
                                                      f"Reinitialize the whole artificial intelligence database "))
        elif command[0] == "AUTOFILL":
            # fills the database with all the possible game combinations
            print("WARNING : this operation can and will take AT LEAST a few hours !")

            if input("Are you sure you want to continue? (y / n)  ").upper() == "Y":
                print("Calculating different game combinations . . .")
                auto_fill_database()
                print("Done")

        elif command[0] == "DELUSER":
            # verifies if an argument has been given by trying to access it
            try:
                print("Deleting user . . .")
                if not delete_user(command[1]):
                    print("ERROR : user was not found or was an admin, please enter another username")
                else:
                    print(f"User {command[1]} successfully deleted")

            # if there is no argument, print an error message
            except IndexError:
                print("ERROR : one additional argument required : [username]\nUse 'help' command for more information")

        elif command[0] == "CHEPSILON":
            # verifies if an argument has been given by trying to access it
            try:
                print("Attempting to change epsilon value . . .")
                command_status = change_epsilon(command[1])

                # if the command failed
                if not command_status[0]:
                    # check what the problem was
                    if command_status[1] == "NaN":
                        print("ERROR : Argument [new_epsilon] must be a float")

                    elif command_status[1] == "WRONG_INTERVAL":
                        print("ERROR : Argument [new_epsilon] must be a float between 0.0 and 0.6")

                else:
                    print(f"Epsilon successfully changed to {command[1]}")

            # if there is no argument, print an error message
            except IndexError:
                print(
                    "ERROR : one additional argument required : [new_epsilon]\nUse 'help' command for more information")

        elif command[0] == "MTYSCORES":
            # empties the score file
            print("Deleting current scores files and creating a new one . . .")
            empty_scores()
            print("Done")

        elif command[0] == "SHOW":
            # verifies if an argument has been given by trying to access it
            try:
                argument = command[1]

            # if there is no argument, print an error message
            except IndexError:
                print(
                    "ERROR : 1 additional argument required : [File / Table]\nUse 'help' command for more information")
                continue

            # check what the value of the argument is
            if argument == "LOGIN" and admin:
                # print all the users from the login file
                all_users = show_all_users()
                print("\n{:30} {:30} {:30} {:30} {:30} {:10} {}\n".format("Username", "Password", "Name", "Last Name",
                                                                          "E-mail", "Admin", "Description"))
                for row in all_users:
                    print(
                        "\n{:30} {:30} {:30} {:30} {:30} {:10} {}".format(row["user_name"], row["password"],
                                                                          row["name"], row["last_name"],
                                                                          row["email"], row["admin"],
                                                                          row["description"]))

            elif argument == "SCORES":
                # print all the scores from the scores file
                print(show_scores())

            elif argument[0:5] == "TURN_":
                # print the database table entered in argument
                # verify if the table entered exists
                try:
                    print(AI.database_tables[int(argument[-1]) - 1])

                # if the database table does not exist, print an error message
                except ValueError or IndexError:
                    print("ERROR : wrong table name for argument [File / Table]\nUse 'help' for more information")

            else:
                print(
                    "ERROR : the object you try to access may be inexistant, inaccessible\nor requires to be "
                    "super administrator")

        elif command[0] == "BACK":
            # redirects back to the previous menu
            return None

        elif command[0] == "EXIT":
            # exits the program
            exit()

        elif command[0] == "REBOOT":
            # reboots the program
            os.system("python main.py")
            print("Restarting . . .")
            common.clear()
            exit()

        elif command[0] in ["SETADMIN", "REINIT", "MTYDB"] and not admin:
            # if one of these commands are accessed without the super-administrator permissions, print an error message
            print("\nRESTRICTED ACCESS : This command can be accessed by the super administrator only")

        elif command[0] == "SETADMIN":
            # verify if an argument was entered by trying accessing it
            try:
                # if the function returns false, print an error message
                if not set_admin(command[1]):
                    print(f"ERROR : user with username {command[1]} does not exist")

            # if no argument is given, print an error message
            except IndexError:
                print("ERROR : one additional argument required : [username]\nUse 'help' command for more information")

        elif command[0] == "REINIT":
            # reinstall the program
            print("Reinitializing program . . .")
            reinstall_program()
            print("Done")

        elif command[0] == "MTYDB":
            # empty the artificial intelligence database
            print("Deleting artificial intelligence and creating it again . . .")
            empty_ai_database()
            print("Done")

        else:
            print(f"\nERROR : {command[0]} has not been recognized as an internal command, please try again")


def auto_fill_database():
    """
    Function which calculates the different winning combinations and stores each one of them in the database
    :return: None
    """
    # if there is a database installed
    if AI.load_dataframe_from_sql():
        # change the epsilon value, since the AI will contain all the possible combinations
        change_epsilon(0.0)

        # create 2 virtual players
        computer_1 = common.Player("computer_1", "O")
        computer_2 = common.Player("computer_2", "X")

        # calculate different values
        for turn_8 in range(2):
            for turn_7 in range(3):
                for turn_6 in range(4):
                    for turn_5 in range(5):
                        for turn_4 in range(6):
                            for turn_3 in range(7):
                                for turn_2 in range(8):
                                    for turn_1 in range(9):
                                        # initialize the variables for the virtual game
                                        computer_1.winner = False
                                        computer_2.winner = False
                                        temp_game_board = [i for i in range(9)]
                                        AI.turns = []
                                        plays = [i for i in range(9)]

                                        # new combination
                                        temp_turns = [turn_1, turn_2, turn_3, turn_4, turn_5, turn_6, turn_7, turn_8]

                                        # virtual game
                                        for i in range(0, 8, 2):
                                            # virtual player 1 plays
                                            AI.turns.append(AI.PlayerMove(computer_1.sign, i + 1, plays[temp_turns[i]]))
                                            temp_game_board[plays[temp_turns[i]]] = computer_1.sign
                                            plays.remove(plays[temp_turns[i]])

                                            # if there is a winner, exit the loop
                                            if temp_game_board[0] == temp_game_board[1] == temp_game_board[2] or \
                                                    temp_game_board[3] == temp_game_board[4] == temp_game_board[
                                                5] or temp_game_board[6] == temp_game_board[7] == \
                                                    temp_game_board[8] or temp_game_board[0] == temp_game_board[
                                                3] == temp_game_board[6] or temp_game_board[1] == \
                                                    temp_game_board[4] == temp_game_board[7] or temp_game_board[
                                                2] == temp_game_board[5] == temp_game_board[8] or \
                                                    temp_game_board[0] == temp_game_board[4] == temp_game_board[
                                                8] or temp_game_board[2] == temp_game_board[4] == \
                                                    temp_game_board[6]:
                                                computer_1.winner = True
                                                break

                                            # virtual player 2 plays
                                            AI.turns.append(AI.PlayerMove(computer_2.sign, i + 2, plays[temp_turns[i + 1]]))
                                            temp_game_board[plays[temp_turns[i + 1]]] = computer_2.sign
                                            plays.remove(plays[temp_turns[i + 1]])

                                            # if there is a winner, exit the loop
                                            if temp_game_board[0] == temp_game_board[1] == temp_game_board[2] or \
                                                    temp_game_board[3] == temp_game_board[4] == temp_game_board[
                                                5] or temp_game_board[6] == temp_game_board[7] == \
                                                    temp_game_board[8] or temp_game_board[0] == temp_game_board[
                                                3] == temp_game_board[6] or temp_game_board[1] == \
                                                    temp_game_board[4] == temp_game_board[7] or temp_game_board[
                                                2] == temp_game_board[5] == temp_game_board[8] or \
                                                    temp_game_board[0] == temp_game_board[4] == temp_game_board[
                                                8] or temp_game_board[2] == temp_game_board[4] == \
                                                    temp_game_board[6]:
                                                computer_2.winner = True
                                                break

                                        # check who the winner was and change the result of the winning turns
                                        if computer_1.winner:
                                            for turn in AI.turns:
                                                if turn.sign == computer_1.sign:
                                                    turn.result = 1.0

                                        elif computer_2.winner:
                                            for turn in AI.turns:
                                                if turn.sign == computer_2.sign:
                                                    turn.result = 1.0

                                        else:
                                            for turn in AI.turns:
                                                turn.result = 0.5

                                        # update the in RAM dataframes
                                        AI.update_ai_database()

        # write the changes over to the database
        AI.write_to_database()

    else:
        print("ERROR : connection error : no database found")


def set_admin(username):
    """
    Adds or removes a user administrator privileges
    :param username: username of the user
    :return: True if there are no failures
    """
    temporary_user = False

    # check if the username entered is not the username of the super administrator
    security.decrypt_file("program_files/config.ini")
    configuration_content = ConfigParser()
    configuration_content.read("program_files/config.ini")
    super_admin = configuration_content["user_info"]["admin"] == username
    security.encrypt_file("program_files/config.ini")

    # open the login.csv file
    with open("program_files\\login.csv", "r") as csv_login_file:
        csv_file_content = csv.DictReader(csv_login_file)

        # iteration trough the login file
        for user_instance in csv_file_content:
            # if the username and password exists in the login file
            if user_instance["user_name"] == username:
                # initialize the current_user variable in the user module and return True
                temporary_user = user.User(user_instance["user_name"], user_instance["password"],
                                           user_instance["name"], user_instance["last_name"], user_instance["email"],
                                           user_instance["description"], user_instance["admin"])

    # if there was a corresponding username and it's not the one of the super administrator
    if temporary_user and not super_admin:
        # check whether the user was already an admin or not
        if temporary_user.admin:
            temporary_user.admin = False
            print(f"{username} is not an admin anymore")

        else:
            temporary_user.admin = True
            print(f"{username} is now an admin")

        security.encrypt_file("program_files\\login.csv")
        return True

    security.encrypt_file("program_files\\login.csv")
    return False


def delete_user(username):
    """
    Deletes a user
    :param username: username of the user to delete
    :return: True if no failures occurred
    """
    all_users = []
    found = False
    security.decrypt_file("program_files/login.csv")

    with open("program_files\\login.csv", "r") as csv_login_file:
        csv_file_content = csv.DictReader(csv_login_file)

        for row in csv_file_content:
            # if the username is found, don't add it to the list
            if not row["user_name"] == username or row["admin"] == "True":
                all_users.append(row)
            else:
                found = True

    if not found:
        security.encrypt_file("program_files/login.csv")
        return False

    # write the new list to the file again
    with open("program_files/login.csv", "w", newline="") as csv_login_file:
        fieldnames = ["user_name", "password", "name", "last_name", "email", "description", "admin"]
        csv_file_content = csv.DictWriter(csv_login_file, fieldnames=fieldnames)
        csv_file_content.writeheader()
        csv_file_content.writerows(all_users)

    security.encrypt_file("program_files/login.csv")
    return True


def show_all_users():
    """
    Reads the login.csv file and returns a list with its content
    :return: a list with all the users
    """
    all_users = []
    security.decrypt_file("program_files/login.csv")

    with open("program_files/login.csv", "r") as csv_login_file:
        csv_file_content = csv.DictReader(csv_login_file)

        for row in csv_file_content:
            all_users.append(row)

    security.encrypt_file("program_files/login.csv")
    return all_users


def change_epsilon(new_epsilon):
    """
    Changes the epsilon value to the value entered as argument
    :param new_epsilon: new value suggestion of epsilon
    :return: True if no failure occured, False with the failure description
    """
    # check if the argument si a float
    try:
        new_epsilon = float(new_epsilon)
    except ValueError:
        return False, "NaN"

    # check if it is a valid input
    if 0 > new_epsilon > 0.6:
        return False, "WRONG_INTERVAL"

    security.decrypt_file("program_files/config.ini")

    # save the new data in the configuration file
    configuration_content = ConfigParser()
    configuration_content.read("program_files/config.ini")
    configuration_content.set("system_var", "epsilon", str(new_epsilon))

    # write the changes to the configuration file
    with open("program_files/config.ini", "w") as config_file:
        configuration_content.write(config_file)

    security.encrypt_file("program_files/config.ini")
    return True


def empty_scores():
    """
    Deletes and recreates the scores.csv file
    :return: None
    """
    os.remove("program_files/scores.csv")
    installation.create_csv_scores()


def empty_ai_database(reinstall=True):
    """
    deletes and recreates the AI database
    :return: None
    """

    # reads the database login from the configuration file
    security.decrypt_file("program_files/config.ini")
    configuration_content = ConfigParser()
    configuration_content.read("program_files\\config.ini")

    # connect to database
    database = mysql.connector.connect(
        host="localhost",
        user=configuration_content["database_login"]["username"],
        password=configuration_content["database_login"]["password"],
        database="tictactoe"
    )

    security.encrypt_file("program_files/config.ini")
    cursor = database.cursor()
    cursor.execute("DROP DATABASE tictactoe")

    if reinstall:
        installation.create_ai_database()


def reinstall_program():
    """
    Deletes and recreates all the program files as well as the database
    :return: None
    """
    # delete all the files
    empty_ai_database(False)
    os.remove("program_files/key.key")
    os.remove("program_files/login.csv")
    os.remove("program_files/config.ini")

    # recreate all the files
    security.create_key()
    installation.create_csv_login()
    installation.create_config_file()
    empty_scores()
    installation.create_ai_database()


def show_scores():
    """
    Put the scores.csv file into a dataframe and return it
    :return: dataframe with the scores in
    """
    security.decrypt_file("program_files/scores.csv")
    scores_dataframe = pandas.read_csv("program_files/scores.csv")
    security.encrypt_file("program_files/scores.csv")
    return scores_dataframe


if __name__ == "__main__":
    option()
