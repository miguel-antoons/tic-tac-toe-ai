import subprocess
import sys
import csv
import getpass
from utilities import security
from configparser import ConfigParser
from os import path, system, environ, execv, mkdir


def installer():
    """
    Start point of the installer program
    :return: None
    """
    print("--------------------------------------------------------------------------------------------------")
    print("*******************Welcome to the installation program for the tic-tac-toe Game.*******************")
    print("--------------------------------------------------------------------------------------------------")
    print("This program is exclusively designed to turn on WINDOWS !")

    system_requirements()
    download_program_files()
    security.create_key()
    install_mysql()
    create_config_file()
    create_csv_login()
    create_csv_scores()
    create_ai_database()
    create_desktop_shortcut()
    print("End of the installation program.\nIf you haven't had any error messages, the program should work")


def system_requirements():
    """
    Prints the system requirements
    :return: None
    """
    print("Before continuing, make sure the following requirements are fulfilled : \n")
    print("1. Python interpreter version is 3.8")
    print("2. Git bash is installed and accessible from the command line")
    print("3. The following libraries are needed for the program to run flawlessly : \n")
    print("\tpandas")
    print("\tcopy")
    print("\tpymysql")
    print("\tsqlalchemy")
    print("\tconfigparser")
    print("\ttime")
    print("\tcryptography")
    print("\tcsv")
    print("\trandom")
    print("\tmath")
    print("\tdatetime")
    print("\tos")
    print("\tmysql.connector\n")

    input("press any key to continue . . .")


def download_program_files():
    """
    Downloads program files form github
    :return: None
    """
    print("\nBefore downloading program files, make sure git is accessible from command line\n")

    system('pause')

    if not path.exists("tic-tac-toe-ai") and not path.exists("../tic-tac-toe-ai"):
        print("Downloading program files...")
        dl_program = subprocess.Popen("git clone https://github.com/Miguel-Antoons/tic-tac-toe-ai.git", shell=True)
        dl_program.wait()
        print("\nDone")

    else:
        print("program files already exist")


def install_mysql():
    """
    Function which show the steps in order to install a mysql server
    :return: None
    """
    print("\n*****Steps in order to download and install MySQL*****\n")
    print("Please make sure Python 3.8 is installed as other versions may not be compatible with this program\n")

    if input(
            "If you already have MySQL and the MySQL Python connector installed, press any key to continue.\nYou can "
            "skip this step by pressing 0") == "0":
        return None

    subprocess.Popen("explorer https://dev.mysql.com/downloads/installer/", shell=True)
    print("\n1. Go to https://dev.mysql.com/downloads/installer/ and download the MySQL\n   installer\n")
    print("2. Open the MySQL installer\n")
    print("3. Accept  all  default  settings  until  the  'Check  requirements'  page\n")
    print(
        "4. When the page 'Check requirements' shows up, click the 'execute' button\n   The program could ask to "
        "install Microsoft  visual  studio, just ignore\n   it and continue the installation.\n")
    print("5. Accept  all  default  settings  until  the  'Accounts  and Roles'  page\n")
    print(
        "6. When  the page  'Accounts and Roles'  shows up, set a password for your\n   database, your  default "
        "username will be 'root'. Remember your password\n   and username as you will need them later during the "
        "installation.\n")
    print(
        "7. Click  next and the 'Windows Service'  page  shows  up. Make  sure  the\n  'Start  the  MySQL  Server  as "
        " System  Startup'   option   is   checked\n")
    print("8. Accept  all  default  settings  until  the  'Connect  to  Server'  page\n")
    print(
        "9. When  the  page  'Connect to Server'  shows  up, enter  your previously\n   chosen  password  in the "
        "password  field  and click next. If there is a\n   green mark next to the check button, you can proceed. "
        "Again, be sure to\n   remember you password and username !\n")
    print(
        "10. Accept  all  the  default  settings  until  you  reach  the end of the\n    installation program  MySQL "
        "shell and MySQL Workbench could  open, you\n    won't need them so they may be closed\n")

    system("pause")
    print("\n--MySQL should be installed !--\n")


def create_config_file():
    """
    Creates the configuration file of the Game
    :return: None
    """
    # find the program directory
    if path.exists("tic-tac-toe-ai"):
        conf_file_path = "tic-tac-toe-ai\\program_files\\config.ini"

    elif path.exists("..\\tic-tac-toe-ai"):
        conf_file_path = "program_files\\config.ini"

    else:
        print("error: unable to create configuration file --> could not find program directory")
        return None

    # if the configuration file does not exist
    if not path.exists(conf_file_path):
        print("Creating configuration file...")
        configuration_content = ConfigParser()

        # initialize the variables for the configuration file
        configuration_content["system_var"] = {
            "epsilon": "0.6"
        }

        configuration_content["user_info"] = {
            "admin": ""
        }

        configuration_content["database_login"] = {
            "username": "",
            "password": ""
        }

        # write the variables to the configuration file
        with open(conf_file_path, "w") as conf:
            configuration_content.write(conf)

        security.encrypt_file(conf_file_path)
        print("Done")


def create_csv_login():
    """
    Creates the csv file which will contain the information of the users
    :return: None
    """
    # find the program directory
    if path.exists("tic-tac-toe-ai"):
        csv_file_path = "tic-tac-toe-ai\\program_files\\login.csv"

    elif path.exists("..\\tic-tac-toe-ai"):
        csv_file_path = "program_files\\login.csv"

    else:
        print("error: unable to create configuration file --> could not find program directory")
        return None

    # check if the login.csv file already exists
    if not path.exists(csv_file_path):
        print("Creating login.csv...")

        # initializing the keys of the csv file and writing them to the file
        with open(csv_file_path, "w", newline="") as csv_login_file:
            fieldnames = ["user_name", "password", "name", "last_name", "email", "description", "admin"]
            csv_writer = csv.DictWriter(csv_login_file, fieldnames=fieldnames)
            csv_writer.writeheader()

        security.encrypt_file(csv_file_path)
        print("Done")


def create_csv_scores():
    """
    Creates the csv file which will contain the user's scores
    :return: None
    """
    # find the program directory
    if path.exists("tic-tac-toe-ai"):
        csv_file_path = "tic-tac-toe-ai\\program_files\\scores.csv"

    elif path.exists("..\\tic-tac-toe-ai"):
        csv_file_path = "program_files\\scores.csv"

    else:
        print("error: unable to create scores.csv file --> could not find program directory")
        return None

    # if the scores.csv file does not exist, create it
    if not path.exists(csv_file_path):
        print("Creating scores.csv...")

        # initializing the keys of the csv file and writing them to the file
        with open(csv_file_path, "w", newline="") as csv_login_file:
            fieldnames = ["player_name", "sign", "n_moves", "date"]
            csv_writer = csv.DictWriter(csv_login_file, fieldnames=fieldnames)
            csv_writer.writeheader()

        security.encrypt_file(csv_file_path)
        print("Done")


def create_ai_database():
    """
    Creates the database and its tables fot the Artificial intelligence
    :return: None
    """
    print("In order to play against an artificial intelligence, you have to install a database.")
    print("However, the artificial intelligence is optional and must not be installed for the game to work,")

    if input("Do you want to install the database? (y / n) ").upper() == "N":
        return None

    import mysql.connector

    mysql_server = ""
    mysql_cursor = ""
    incorrect_values = True

    # find the configuration file
    if path.exists("Python_project"):
        conf_file_path = "Python_project\\program_files\\config.ini"

    elif path.exists("..\\Python_project"):
        conf_file_path = "program_files\\config.ini"

    else:
        print("error: unable to find the configuration file --> could not find program directory")
        return None

    # while the user inputs incorrect values and he wants to try again
    while incorrect_values:
        # ask the mysql server login
        user = input("Enter the username of the mysql server : ")
        password = getpass.getpass()

        security.decrypt_file(conf_file_path)

        # save the login in the configuration file
        configuration_content = ConfigParser()
        configuration_content.read(conf_file_path)
        configuration_content.set("database_login", "username", user)
        configuration_content.set("database_login", "password", password)

        # write the changes to the configuration file
        with open(conf_file_path, "w") as config_file:
            configuration_content.write(config_file)

        security.encrypt_file(conf_file_path)

        # trying to connect to the mysql server
        try:
            print("Attempting to connect to local MySQL server...")
            mysql_server = mysql.connector.connect(
                host="localhost",
                user=user,
                password=password
            )

            mysql_cursor = mysql_server.cursor()

            incorrect_values = False
            print("Done")

        # if there is a connection failure aks again for the login
        except mysql.connector.Error as error:
            print(f"error: unable to connect to database: {error}")

            if input("Enter 0 if you want to exit the installation process.") == "0":
                return None

    # check if the database exists, store the results in the results variable
    mysql_cursor.execute("SHOW DATABASES LIKE 'tictactoe'")
    results = mysql_cursor.fetchall()

    # if the variable does not exist
    if not len(results):
        print("Creating database...")

        # create the database
        mysql_cursor.execute("CREATE DATABASE tictactoe")
        mysql_cursor.execute("USE tictactoe")

        print("Done")

        print("Creating AI database tables...")

        # create the tables of the AI database
        mysql_cursor.execute("""CREATE TABLE turn_1 (
            play int(11) not null,
            probability float(24, 23) not null,
            n_references int(11) not null,
            CONSTRAINT pk_turn_1 PRIMARY KEY (play)
        )""")
        mysql_cursor.execute("""CREATE TABLE turn_2 (
            play int(11) not null,
            turn_1 int(11) not null,
            probability float(24, 23) not null,
            n_references int(11) not null,
            CONSTRAINT pk_turn_2 PRIMARY KEY (play, turn_1)
        )""")
        mysql_cursor.execute("""CREATE TABLE turn_3 (
            play int(11) not null,
            turn_1 int(11) not null,
            turn_2 int(11) not null,
            probability float(24, 23) not null,
            n_references int(11) not null,
            CONSTRAINT pk_turn_3 PRIMARY KEY (play, turn_1, turn_2)
        )""")
        mysql_cursor.execute("""CREATE TABLE turn_4 (
            play int(11) not null,
            turn_1 int(11) not null,
            turn_2 int(11) not null,
            turn_3 int(11) not null,
            probability float(24, 23) not null,
            n_references int(11) not null,
            CONSTRAINT pk_turn_4 PRIMARY KEY (play, turn_1, turn_2, turn_3)
        )""")
        mysql_cursor.execute("""CREATE TABLE turn_5 (
            play int(11) not null,
            turn_1 int(11) not null,
            turn_2 int(11) not null,
            turn_3 int(11) not null,
            turn_4 int(11) not null,
            probability float(24, 23) not null,
            n_references int(11) not null,
            CONSTRAINT pk_turn_5 PRIMARY KEY (play, turn_1, turn_2, turn_3, turn_4)
        )""")
        mysql_cursor.execute("""CREATE TABLE turn_6 (
            play int(11) not null,
            turn_1 int(11) not null,
            turn_2 int(11) not null,
            turn_3 int(11) not null,
            turn_4 int(11) not null,
            turn_5 int(11) not null,
            probability float(24, 23) not null,
            n_references int(11) not null,
            CONSTRAINT pk_turn_6 PRIMARY KEY (play, turn_1, turn_2, turn_3, turn_4, turn_5)
        );""")
        mysql_cursor.execute("""CREATE TABLE turn_7 (
            play int(11) not null,
            turn_1 int(11) not null,
            turn_2 int(11) not null,
            turn_3 int(11) not null,
            turn_4 int(11) not null,
            turn_5 int(11) not null,
            turn_6 int(11) not null,
            probability float(24, 23) not null,
            n_references int(11) not null,
            CONSTRAINT pk_turn_7 PRIMARY KEY (play, turn_1, turn_2, turn_3, turn_4, turn_5, turn_6)
        )""")
        mysql_cursor.execute("""CREATE TABLE turn_8 (
            play int(11) not null,
            turn_1 int(11) not null,
            turn_2 int(11) not null,
            turn_3 int(11) not null,
            turn_4 int(11) not null,
            turn_5 int(11) not null,
            turn_6 int(11) not null,
            turn_7 int(11) not null,
            probability float(24, 23) not null,
            n_references int(11) not null,
            CONSTRAINT pk_turn_8 PRIMARY KEY (play, turn_1, turn_2, turn_3, turn_4, turn_5, turn_6, turn_7)
        )""")
        print("Done")

    else:
        print("Database already exists")

    mysql_cursor.close()
    mysql_server.close()


def create_desktop_shortcut():
    """
    Creates a desktop shortcut if the user wants so
    :return: None
    """
    print("\n*****Desktop shortcut*****")

    # check if there is no desktop shortcut and ask the user if he wants one
    if path.exists(path.join(environ["HOMEPATH"], "Desktop\\tic-tac-toe.lnk")) or input(
            "\nDo you want a desktop shortcut? (y / n)").upper() == "N":
        print("shortcut already exists")
        return None

    print("Creating desktop shortcut...")
    desktop_path = path.join(environ["HOMEPATH"], "Desktop\\tic-tac-toe.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut_object = shell.CreateShortCut(desktop_path)

    # find the program directory and adapt the paths to create the shortcut
    if path.exists("tic-tac-toe-ai"):
        target = path.join(path.dirname(path.realpath(__file__)), "tic-tac-toe-ai\\main.py")
        working_directory = path.join(path.dirname(path.realpath(__file__)), "tic-tac-toe-ai")
        icon = path.join(path.dirname(path.realpath(__file__)), "tic-tac-toe-ai\\program_files\\shortcut_icon.ico")

    elif path.exists("../tic-tac-toe-ai"):
        target = path.join(path.dirname(path.realpath(__file__)), "main.py")
        working_directory = path.dirname(path.realpath(__file__))
        icon = path.join(path.dirname(path.realpath(__file__)), "program_files\\shortcut_icon.ico")

    else:
        print("error: cannot find working directory")
        return None

    # create the shortcut
    shortcut_object.TargetPath = target
    shortcut_object.WorkingDirectory = working_directory
    shortcut_object.IconLocation = icon
    shortcut_object.save()
    print("Done")


if __name__ == "__main__":
    # check if the win32com.client exists
    try:
        from win32com.client import Dispatch

    # if it does not exist, install it and restart the program
    except ImportError or ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", '--upgrade', 'pip'])
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'pywin32'])
        subprocess.check_call([sys.executable, "-m", "pip", "install", 'pypiwin32'])
        execv(sys.executable, ['python'] + sys.argv)

    # security.create_key()
    # create_csv_login()
    # create_config_file()
    # create_csv_scores()
    # create_ai_database()
    installer()
    system('pause')
