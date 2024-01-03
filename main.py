import random
import time

game_vars = {
    "turn": 0,
    "coins": 10,
    "score": 0,
    "game_state": "MENU",  # Can be MENU, PLAYING or OVER
}

field = [['' for _ in range(20)] for _ in range(20)]

buildings = {
    "Commercial": "C",
    "Industry": "I",
    "Park": "O",
    "Residential": "R",
    "Road": "*"
}


# Separate console output into chunks for readability
def await_user():
    print()
    time.sleep(.25)


# Get input from the user, validate before returning
def get_input(max_options):
    # Input must be valid before returning, otherwise loop
    while True:
        loc_option = input("Your choice? ")
        # Verification: input is a digit within the allowed range
        if loc_option.isdigit():
            loc_option = int(loc_option)
            if 1 <= loc_option <= max_options:
                return loc_option
            else:
                print(f"Choice must be between 1 and {max_options}.")
        else:
            print("Choice must be a number.")
        await_user()


# Show main menu, gets input and returns selected option
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. High Scores")
    print("4. Quit")
    await_user()
    # Get what user wants to do
    loc_option = get_input(4)
    return loc_option


# Draws field and relevant stats
def draw_field(loc_game_vars, loc_field):
    # Get data from loc_game_vars and loc_field to store locally
    turn = loc_game_vars['turn']
    coins = loc_game_vars['coins']
    num_rows, num_cols = len(loc_field), len(loc_field[0])
    # Print column numbers and top line
    print(' ' + ''.join(f'{i + 1:>3}' for i in range(num_cols)))
    print(' +' + '--+' * num_cols)
    # Print each row
    for row_num, row in enumerate(loc_field):
        print(f"{chr(row_num + 65)}|{'|'.join([f'{cell:>2}' for cell in row])}|")
        print(' +' + '--+' * num_cols)
    # Print stats
    print(f"{'Turn: ' + str(turn):<15}{'Coins: ' + str(coins)}")


def buy_building(loc_game_vars, loc_field):
    # Print available buildings
    building_list = [*buildings]  # Advanced syntax: get list of keys from dict
    random_building = random.sample(building_list, 2)
    print("You have been offered")
    print("---------------------")
    print("1.", random_building[0])
    print("2.", random_building[1])
    print()
    print("Choose your option (1 or 2):")
    # Get desired building
    loc_option = get_input(2)
    selected = random_building[loc_option - 1]
    # Check sufficient coins
    if loc_game_vars['coins'] >= 1:
        # Get position
        while True:
            position = input("Place where? ").upper()
            if len(position) == 2 and position[0].isalpha() and position[1].isdigit():
                break
            else:
                print('Enter row letter followed by column number.')
                continue
        # Place building (or cancel if it cannot be placed there)
        if not place_building(loc_field, position, selected):
            print("Invalid position.")
            return False
    else:  # Not enough coins
        print("Not enough coins.")
        return False
    # Pay for building if it is placed
    loc_game_vars["coins"] -= 1
    return True


def show_turn_actions():
    # Print options
    print("1. Build a Building")
    print("2. See Current Score")
    print("3. Save Game")
    print("4. Exit to Main Menu")
    await_user()
    # Get what user wants to do
    loc_option = get_input(4)
    return loc_option


def check_valid_pos(loc_row, loc_col, loc_field):
    num_rows, num_cols = len(loc_field), len(loc_field[0])
    if (0 <= loc_row <= num_rows and
            0 <= loc_col <= num_cols and
            loc_field[loc_row][loc_col] == ''):
        return True
    return False


def place_building(loc_field, position, building_name):
    # Declare local variables needed
    loc_row = ord(position[0]) - 65
    loc_col = int(position[-1]) - 1
    pos_valid = check_valid_pos(loc_row, loc_col, loc_field)
    if pos_valid:
        loc_field[loc_row][loc_col] = buildings[building_name]
        return pos_valid


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


def run_turn(loc_game_vars, loc_field):
    # TODO: implement turn-to-turn gameplay logic
    # PRE-TURN PHASE
    loc_game_vars['turn'] += 1
    draw_field(loc_game_vars, loc_field)

    # MAIN PHASE
    # Execute player's actions
    turn_executed = False
    while not turn_executed:
        # Perform actions according to player's input
        selected_option = show_turn_actions()
        if selected_option == 1:
            turn_executed = buy_building(loc_game_vars, loc_field)
        elif selected_option == 2:
            print(f"Current Score: {calculate_score()}")
        elif selected_option == 3:
            save_game(loc_game_vars, loc_field)
        elif selected_option == 4:
            loc_game_vars["game_state"] = "MENU"
            turn_executed = True

    # CLEANUP PHASE
    # TODO: recalculate score, check game over (change state to OVER), autosave

    await_user()


def update_high_scores(score, player_name="Anonymous"):
    try:
        with open('high_scores.txt', 'a') as file:
            file.write(f"{player_name} {score}\n")
    except Exception as e:
        print(f"An error occurred while updating high scores: {e}")


def calculate_score():
    # TODO: implement the scoring logic based on the specified rules
    # (Residential, Industry, Commercial, Park, Road effects)
    pass


# Load the game from a save file
def load_game(loc_game_vars, loc_field):
    # TODO: implement load save function
    # Find save file
    try:
        file = open('save.txt')
    except FileNotFoundError:
        print('No save file to load from.')
        return False
    # Dissect save file
    file_list = file.read().split('\n\n')[:-1]
    field_list = file_list.pop().split('\n')
    var_list = file_list.pop().split(',')[:-1]
    # Reconstruct game_vars
    count = 0
    for var in loc_game_vars:
        # Account for ints and others (strings)
        if var_list[count].isdigit():
            loc_game_vars[var] = int(var_list[count])
        else:
            loc_game_vars[var] = var_list[count]
        count += 1
    # Reconstruct field
    for row_num in range(len(field_list)):
        load_row = field_list[row_num].split(',')[:-1]
        for col_num in range(len(load_row)):
            loc_field[row_num][col_num] = load_row[col_num]
    file.close()
    return True


def save_game(loc_game_vars, loc_field):
    # TODO: implement save function
    file = open("save.txt", "w")
    # Store game_vars
    for var in loc_game_vars.values():
        file.write(str(var))
        file.write(',')
    file.write("\n\n")
    # Store field
    for row in loc_field:
        for place in row:
            if place != "":
                file.write(str(place))
            file.write(",")
        file.write("\n")
    file.write('\n')
    print('Game saved.')
    file.close()


# Initialise variables for a new game
def start_game(loc_game_vars, loc_field):
    # TODO: initialise variables
    pass


# Main game loop, displays main menu then changes game state if a game has been started
if __name__ == "__main__":
    while True:
        print("Ngee Ann City")
        print("-------------")
        print("Build it Better!\n")
        while game_vars["game_state"] == "MENU":
            selected_action = show_main_menu()
            if selected_action == 1:
                game_vars["game_state"] = "PLAYING"
                start_game(game_vars, field)
            elif selected_action == 2:
                game_vars["game_state"] = "PLAYING"
                load_game(game_vars, field)
            elif selected_action == 3:
                show_high_scores()
            elif selected_action == 4:
                raise SystemExit

        while game_vars["game_state"] == "PLAYING":
            run_turn(game_vars, field)
        #     # Playing the game
        #     draw_field(loc_game_vars, loc_field)
        #     print("\nOptions:")
        #     print("1. Build a Building")
        #     print("2. See Current Score")
        #     print("3. Save Game")
        #     print("4. Exit to Main Menu")
        #
        #     option = get_input(4)
        #
        #     if option == 1:
        #         # Build a Building
        #         show_building_types()
        #         building_option = buy_building()
        #         row = int(input("Enter row (1-20): ")) - 1
        #         col = int(input("Enter column (1-20): ")) - 1
        #         place_building(field, (row, col), building_option)
        #         game_vars["coins"] -= 1  # Decrement coins after building
        #
        #     elif option == 2:
        #         # See Current Score
        #         current_score = calculate_score()
        #         print(f"Current Score: {current_score}")
        #
        #     elif option == 3:
        #         # Save Game
        #         save_game()
        #
        #     elif option == 4:
        #         # Exit to Main Menu
        #         game_vars["game_over"] = True
        #
        # # End of Game
        # final_score = calculate_score()
        # print(f"Game Over! Final Score: {final_score}")
        #
        # # Update high scores if necessary
        # if final_score > 0:
        #     player_name = input("Congratulations! You made it to the top 10! Enter your name: ")
        #     update_high_scores(final_score, player_name)
        #
        # await_user()
