import time
from utilities import option
from game_management import multi, single, scores, AI, common
from user_management import user, login

if __name__ == "__main__":
    common.clear()
    print("\nLoading . . .")
    AI.load_dataframe_from_sql()
    incorrect_input = True  # loop statement
    replay = True               # loop statement
    game_mode = ""              # Game-mode chosen by the user
    scores.load_scores()

    common.clear()
    print("--------------------------------------------------------------------------------------------------")
    print("**********************************Welcome to the tic-tac-toe Game**********************************")
    print("--------------------------------------------------------------------------------------------------")

    # Exits if the Player has no account and does not want to create one
    if login.login():
        print(f"\n\nWelcome {user.current_user.name} {user.current_user.last_name} ({user.current_user.user_name})")
        print(f"\nYour description : {user.current_user.description}")

    else:
        exit()

    # As long as the Player(s) want(s) to continue, the loop continues
    while replay:
        replay = False
        # As long as the Game mode is invalid, the loop continues
        while incorrect_input:
            common.clear()
            print("\nChoose your what you want to do :\n1. Multi-Player\n2. Single Player\n3. Change password\n4. "
                  "Change description")
            if user.current_user.admin:
                print("5. Enter option mode")
            game_mode = input("\n\nIn order to choose the what you want to do, please enter the number on "
                              "the left of the option : ")

            try:
                game_mode = int(game_mode)
                if game_mode == 1 or game_mode == 2:
                    incorrect_input = False
                elif game_mode == 3:
                    common.clear()
                    user.change_password()
                elif game_mode == 4:
                    common.clear()
                    user.change_description()
                elif game_mode == 5 and user.current_user.admin:
                    common.clear()
                    option.option()
                else:
                    print("ERROR : choose a valid option (1, 2, 3, 4, 5)")

            except ValueError:
                print("Input was not accepted, please try again...")

            time.sleep(3)

        common.clear()
        if game_mode == 1:
            multi.multi_play()

        else:
            single.single_play()

        scores.print_scores()

        if input("Do you want to replay? (y / n)  ").upper() == "Y":
            replay = True
            incorrect_input = True
            AI.turns = []
            common.clear()
