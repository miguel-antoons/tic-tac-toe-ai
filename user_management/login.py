import getpass
import csv
from utilities import security
from user_management import user
from configparser import ConfigParser


def login():
    """
    Start point of the login program
    :return: None
    """
    print("\n--------------------------------------------------------------------------------------------------")
    print("***********************************************LOGIN***********************************************")
    print("--------------------------------------------------------------------------------------------------")

    # while the Player does not want to create an account and he wants to try again
    while True:
        username = input("username : ")
        password = getpass.getpass()

        if verify_login(username, password):
            print(f"Access granted\n")
            return True

        else:
            print("Access denied, do you want to try again ? (y / n)  ")
            if input().upper() == "Y":
                continue

        if input("Would you like to create a new account? (y / n)  ").upper() == "Y":
            create_account()
        else:
            return False


def verify_login(username, password):
    """
    Verifies if a username and password are valid (exists in the csv file)
    :param username: the username entered by the user
    :param password: the password entered by the user
    :return: True if the login is valid, False if not
    """
    security.decrypt_file("program_files\\login.csv")

    with open("program_files\\login.csv", "r") as csv_login_file:
        csv_file_content = csv.DictReader(csv_login_file)

        # iteration trough the login file
        for user_instance in csv_file_content:
            # if the username and password exists in the login file
            if (user_instance["user_name"] == username or user_instance["email"] == username) and \
                    user_instance["password"] == password:
                # initialize the current_user variable in the user module and return True
                user.current_user = user.User(user_instance["user_name"], user_instance["password"],
                                              user_instance["name"], user_instance["last_name"], user_instance["email"],
                                              user_instance["description"], user_instance["admin"])

                security.encrypt_file("program_files\\login.csv")
                return True

    security.encrypt_file("program_files\\login.csv")
    return False


def create_account():
    """
    Function which asks the user inputs in order to create a new account
    :return: None
    """
    user_information = {}   # dictionary which will contain the user's inputs
    no_input = True         # loop statement

    # while no input has been given or the username entered already exists
    while no_input:
        no_input = False
        user_information["user_name"] = input("New Username : \t\t")

        if user_information["user_name"] == "":
            no_input = True

        security.decrypt_file("program_files\\login.csv")

        # open the login file and check if the username has not been taken yet
        with open("program_files\\login.csv", "r") as csv_login_file:
            csv_file_content = csv.DictReader(csv_login_file)

            for user_instance in csv_file_content:
                # if the username has been taken, ask a new username
                if user_information["user_name"] == user_instance["user_name"]:
                    print("Username already exists or no username was entered. Please try again\n")
                    no_input = True

        security.encrypt_file("program_files\\login.csv")

    # cals a function in order to set a password
    user_information["password"] = user.set_password()

    no_input = True

    # while no input has been given
    while no_input:
        no_input = False
        user_information["name"] = input("Your name : \t\t")
        if user_information["name"] == "":
            print("A name must be entered. Please try again.\n")
            no_input = True

    no_input = True

    # while no input has been given
    while no_input:
        no_input = False
        user_information["last_name"] = input("Your last name : \t")
        if user_information["last_name"] == "":
            print("A last name must be entered. Please try again.\n")
            no_input = True

    no_input = True

    # while no input has been given
    while no_input:
        no_input = False
        user_information["email"] = input("Your e-mail : \t\t")
        if user_information["email"] == "":
            print("An e-mail address must be entered. Please try again.\n")
            no_input = True

    # cals a function in order to set a description
    user_information["description"] = user.set_description()

    # read of the configuration file
    security.decrypt_file("program_files\\config.ini")
    configuration_content = ConfigParser()
    configuration_content.read("program_files\\config.ini")

    # if no super-admin has been set yet, the user will be the super-admin
    if configuration_content["user_info"]["admin"] == "":
        print("You are now the administrator of the system")
        configuration_content.set("user_info", "admin", str(user_information["user_name"]))

        with open("program_files\\config.ini", "w") as config_file:
            configuration_content.write(config_file)

        user_information["admin"] = True
    else:
        user_information["admin"] = False

    security.encrypt_file("program_files\\config.ini")
    security.decrypt_file("program_files\\login.csv")

    # append the new user to the login file
    with open("program_files\\login.csv", "a+", newline="") as csv_login_file:
        print("Creating user...")
        fieldnames = ["user_name", "password", "name", "last_name", "email", "description", "admin"]
        csv_writer = csv.DictWriter(csv_login_file, fieldnames=fieldnames)

        csv_writer.writerow(user_information)

    security.encrypt_file("program_files\\login.csv")
    print("Done\n")


if __name__ == "__main__":
    # login()
    # user.change_description()
    print(user.current_user.description)
