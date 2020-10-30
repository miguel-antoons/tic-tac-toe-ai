import multi
import single

incorrect_game_mode = True  # loop statement
replay = True               # loop statement
game_mode = ""              # game-mode chosen by the user


print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
print("Welcome to the tic-tac-toe game")
print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

# As lon as the player(s) want(s) to continue, the loop ocontinues
while replay:

    # As long as the game mode is invalie, the loop continues
    while incorrect_game_mode:
        print("Choose your game mode:\n1. Multi-player\n2. Single player\n\nIn order to choose the game mode, please press the number on the left of the option.")
        game_mode = input()

        try:
            game_mode = int(game_mode)
            if game_mode == 1 or 2:
                incorrect_game_mode = False

        except ValueError:
            print("Input was not accepted, please try again...")

    if game_mode == 1:
        multi.multi_play()

    else:
        single.single_play()

    print("Do you want to replay ?\n1. Yes\n2. No\n")
    choice = input("Enter 1 if you want to replay, press any key if you don't : ")

    if not choice == "1":
        replay = False
