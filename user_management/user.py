import getpass
from utilities import security
import csv


current_user = 0    # variable will contain the current user of the Game


class User:
    """
    Represents a user and his information
    """
    def __init__(self, user_name: str, password: str, name: str, last_name: str, email: str, description: str,
                 admin: str):
        self.__user_name = user_name
        self.__password = password
        self.__name = name
        self.__last_name = last_name
        self.__email = email
        self.__description = description
        if admin == "True":
            self.__admin = True
        else:
            self.__admin = False

    @property
    def user_name(self):
        return self.__user_name

    @property
    def name(self):
        return self.__name

    @property
    def last_name(self):
        return self.__last_name

    @property
    def email(self):
        return self.__email

    @property
    def description(self):
        return self.__description

    @property
    def admin(self):
        return self.__admin

    @property
    def password(self):
        return "Unable to fulfill request"

    @password.setter
    def password(self, new_password):
        self.__password = new_password
        self.__save_changes()

    @description.setter
    def description(self, new_description):
        self.__description = new_description
        self.__save_changes()

    @admin.setter
    def admin(self, admin):
        self.__admin = admin
        self.__save_changes()

    def __save_changes(self):
        """
        Save possible changes to the password, description or administration information
        :return: None
        """
        line_to_change = None
        file_rows = []
        security.decrypt_file("program_files\\login.csv")

        # read the login file
        with open("program_files\\login.csv", "r") as csv_login_file:
            csv_file_content = csv.DictReader(csv_login_file)

            for i, user_instance in enumerate(csv_file_content):
                file_rows.append(user_instance)

                if user_instance["user_name"] == self.__user_name:
                    line_to_change = i

        # apply the changes to the content
        file_rows[line_to_change]["description"] = self.__description
        file_rows[line_to_change]["password"] = self.__password
        file_rows[line_to_change]["admin"] = self.__admin

        # write the changed content to the file again
        with open("program_files\\login.csv", "w", newline="") as csv_login_file:
            fieldnames = ["user_name", "password", "name", "last_name", "email", "description", "admin"]
            writer = csv.DictWriter(csv_login_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(file_rows)

        security.encrypt_file("program_files\\login.csv")


def set_password():
    """
    Asks the user for a password
    :return: the valid password
    """
    password = ""
    no_input = True

    while no_input:
        no_input = False
        password = getpass.getpass(prompt="New Password : ")

        if password == "" or not password == getpass.getpass(prompt="Enter password again : "):
            print("Passwords did not match or no password was entered. Please try again.\n")
            no_input = True

    return password


def change_password():
    """
    Modifies the current password
    :return: None
    """
    current_user.password = set_password()


def set_description():
    """
    Asks the user for a description
    :return: the valid description
    """
    description = ""
    no_input = True

    while no_input:
        no_input = False
        description = input("Describe yourself, this can be modified later : ")

        if description == "":
            print("A description must be entered. Please try again.\n")
            no_input = True

    return description


def change_description():
    """
    Modifies the current description
    :return: None
    """
    current_user.description = set_description()


if __name__ == "__main__":
    pass
