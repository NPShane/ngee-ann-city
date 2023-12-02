import time

game_vars = {
    "turn": 0,
    "coins": 10,
    "game_over": False,
}


# Separate console output into chunks for readability
def await_user():
    print()
    time.sleep(.25)


# Get input from the user, validate before returning
def get_input(max_options):
    # Input must be valid before returning, otherwise loop
    while True:
        option = input("Your choice? ")
        # Verification: input is a digit within the allowed range
        if option.isdigit():
            option = int(option)
            if 1 <= option <= max_options:
                return option
            else:
                print(f"Choice must be between 1 and {max_options}.")
        else:
            print("Choice must be a number.")
        await_user()


def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. High Scores")
    print("4. Quit")
    await_user()
    # Get what user wants to do
    option = get_input(4)
    return option


def show_high_scores():
    try:
        with open('high_scores.txt', 'r') as file:
            # Read the content of the file
            scores = [line.strip().split() for line in file.readlines()]

        if not scores:
            print("No high scores available.")
            return

        print("\nHigh Scores")
        for name, score in scores:
            print(f"{name:15}: {score}")

    except FileNotFoundError:
        print("High scores file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    await_user()


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
