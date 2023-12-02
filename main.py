# import stuff here
game_vars = {
    "turn": 0,
    "coins": 10,
    "game_over": False,
}


def get_input(max_options):
    while True:
        option = input("Your choice? ")
        if option.isdigit():
            option = int(option)
            if 1 <= option <= max_options:
                return option
            else:
                print(f"Choice must be between 1 and {max_options}.")
        else:
            print("Choice must be a number.")


def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. High Scores")
    print("4. Quit")
    # Get what user wants to do
    option = get_input(4)
    return option


def show_high_scores():
    # TODO: implement the high score system
    pass


# Main game loop, displays main menu then changes game state if a game has been started
if __name__ == "__main__":
    while True:
        print("Ngee Ann City")
        print("-------------")
        print("Build it Better!\n")
        game_playing = False
        while not game_playing:
            main_option = show_main_menu()

            if main_option == 1:
                game_playing = not game_playing
                # TODO: initialise game
            elif main_option == 2:  # TODO: add load_game(game_vars) to this condition later
                game_playing = not game_playing
            elif main_option == 3:
                show_high_scores()
            elif main_option == 4:
                raise SystemExit

        while not game_vars["game_over"]:
            # TODO: implement turn-to-turn gameplay logic
            pass
