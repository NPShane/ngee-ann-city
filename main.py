import random
import time

game_vars = {
    "turn": 0,
    "coins": 16,
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
    time.sleep(.5)


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


# Buys a building then places it, returns T/F if successful
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
            if 2 <= len(position) <= 3 and position[0].isalpha() and position[1].isdigit():
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


# Show turn menu and returns selected option
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


# Checks if a given position is valid to be built on
def check_valid_pos(loc_row, loc_col, loc_field):
    pos = loc_field[loc_row][loc_col]
    num_rows, num_cols = len(loc_field), len(loc_field[0])
    # Check within field and empty
    if 0 <= loc_row <= num_rows - 1 and 0 <= loc_col <= num_cols - 1 and pos == '':
        # Override if first turn (can place anywhere)
        if game_vars["turn"] == 1:
            return True
        # Check if there is at least one building surrounding this
        if any(pos != "" for pos in loc_field):
            return True
    return False


# Places down a building, returns T/F depending on success
def place_building(loc_field, position, building_name):
    # Declare local variables needed
    loc_row = ord(position[0]) - 65
    loc_col = int(position[1:]) - 1
    # Check position validity
    pos_valid = check_valid_pos(loc_row, loc_col, loc_field)
    if pos_valid:
        loc_field[loc_row][loc_col] = buildings[building_name]
        return pos_valid


# Show the high scores from file
def show_high_scores():
    scores = load_high_scores()

    if not scores:
        print("No high scores available.")
        return

    print("\nHigh Scores")
    for name, score in scores:
        print(f"{name:15}: {score}")

    await_user()


# Runs 1 entire turn of the game
def run_turn(loc_game_vars, loc_field):
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
            print(f"Current Score: {calculate_score(loc_field, loc_game_vars)}")
        elif selected_option == 3:
            save_game(loc_game_vars, loc_field)
        elif selected_option == 4:
            loc_game_vars["game_state"] = "MENU"
            turn_executed = True

    # CLEANUP PHASE
    # Add coins for each R around a C or I
    for row_index, row in enumerate(loc_field):
        for value_index, value in enumerate(row):
            if value == "C" or value == "I":
                loc_game_vars["coins"] += count_adjacent_buildings(loc_field, row_index, value_index, "R")

    # End the game if either condition is met
    if loc_game_vars["coins"] <= 0 or loc_game_vars["turn"] == 400:
        loc_game_vars["game_state"] = "OVER"

    await_user()


# def calculate_score(loc_field):
#    # (Residential, Industry, Commercial, Park, Road effects)
#    total_score = 0

#    for row in range(len(loc_field)):
#        for col in range(len(loc_field[row])):
#            building = loc_field[row][col]

#            if building == "R":
#                total_score += calculate_residential_score(loc_field, row, col)
#            elif building == "I":
#                total_score += calculate_industry_score(loc_field, row, col)
#            elif building == "C":
#                total_score += calculate_commercial_score(loc_field, row, col)
#            elif building == "O":
#                total_score += calculate_park_score(loc_field, row, col)
#            elif building == "*":
#                total_score += calculate_road_score(loc_field, row, col)

#    return total_score

# def calculate_residential_score(loc_field, row, col):
#    adjacent_buildings = get_adjacent_buildings(loc_field, row, col)
#    industry_nearby = any(building == "I" for building in adjacent_buildings)

#    if industry_nearby:
#        return 1
#    else:
#        residential_count = adjacent_buildings.count("R")
#        commercial_count = adjacent_buildings.count("C")
#        park_count = adjacent_buildings.count("O")
#        return residential_count + 2 * park_count + commercial_count


# def calculate_industry_score(loc_field, row, col):
#    industry_count = sum(1 for row in loc_field for building in row if building == "I")
#    adjacent_residential_count = count_adjacent_buildings(loc_field, row, col, "R")

#    return industry_count + adjacent_residential_count


# def calculate_commercial_score(loc_field, row, col):
#    adjacent_residential_count = count_adjacent_buildings(loc_field, row, col, "R")
#    return adjacent_residential_count


# def calculate_park_score(loc_field, row, col):
#    adjacent_park_count = count_adjacent_buildings(loc_field, row, col, "O")
#    return adjacent_park_count


# def calculate_road_score(loc_field, row, col):
#    connected_road_count = count_connected_roads(loc_field, row)
#    return connected_road_count


# def count_connected_roads(loc_field, row):
#    return loc_field[row].count("*")


# Count the total number of a certain type of building
def count_total_buildings(loc_field, building_type):
    count = 0
    for row in loc_field:
        for cell in row:
            if cell == building_type:
                count += 1
    return count


# Calculates the total score for the current city
def calculate_score(loc_field, loc_game_vars):
    score = 0
    count_ind = count_total_buildings(loc_field, "I")

    # Iterate through each cell in the city
    for row_num, row in enumerate(loc_field):
        for col_num, building in enumerate(row):
            # If residential
            if building == "R":
                adj_buildings = get_adjacent_buildings(loc_field, row_num, col_num)
                for adj_building in adj_buildings:
                    # Score only 1 point if next to an industry
                    if adj_building == "I":
                        score += 1
                        break
                    # If not next to an industry, score based on other adjacent buildings
                    elif adj_building == "R" or adj_building == "C":
                        score += 1
                    elif adj_building == "O":
                        score += 2
            # If industrial, score 1 per ind in city
            elif building == "I":
                score += count_ind
            # If commercial, score 1 per adj com
            elif building == "C":
                adj_buildings = get_adjacent_buildings(loc_field, row_num, col_num)
                for adj_building in adj_buildings:
                    if adj_building == "C":
                        score += 1
            # If park
            elif building == "O":
                adj_buildings = get_adjacent_buildings(loc_field, row_num, col_num)
                for adj_building in adj_buildings:
                    if adj_building == "O":
                        score += 1
            # If road
            elif building == "*":
                score += row.count("*")

    return score


# Finds the 4 buildings around a coordinate
def get_adjacent_buildings(loc_field, row, col):
    num_rows, num_cols = len(loc_field), len(loc_field[0])
    adjacent_buildings = []

    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
            if 0 <= i < num_rows and 0 <= j < num_cols and not (i == row and j == col):
                adjacent_buildings.append(loc_field[i][j])

    return adjacent_buildings


# Count the number of a certain type of building around a coordinate
def count_adjacent_buildings(loc_field, row, col, building_type):
    adjacent_buildings = get_adjacent_buildings(loc_field, row, col)
    return adjacent_buildings.count(building_type)


# Load the game from a save file
def load_game(loc_game_vars, loc_field):
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
    for count, var in enumerate(loc_game_vars):
        # Account for ints and others (strings)
        if var_list[count].isdigit():
            loc_game_vars[var] = int(var_list[count])
        else:
            loc_game_vars[var] = var_list[count]
    loc_game_vars["turn"] -= 1
    # Reconstruct field
    for row_num in range(len(field_list)):
        load_row = field_list[row_num].split(',')[:-1]
        for col_num in range(len(load_row)):
            loc_field[row_num][col_num] = load_row[col_num]
    file.close()
    return True


# Save the game to a save file
def save_game(loc_game_vars, loc_field):
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
    # Initialize game variables
    loc_game_vars["turn"] = 0
    loc_game_vars["coins"] = 16
    loc_game_vars["score"] = 0
    loc_game_vars["game_state"] = "PLAYING"

    # Clear the game field
    for i in range(len(loc_field)):
        for j in range(len(loc_field[0])):
            loc_field[i][j] = ''

    # Choose two initial buildings
    # initial_buildings = random.sample([*buildings], 2)

    # Display initial information
    print("Welcome to Ngee Ann City!")
    print("You are the mayor. Build the happiest and most prosperous city!")
    print(f"Starting with {loc_game_vars['coins']} coins.")

    # Display the initial buildings
    # print("Initial Buildings:")
    # print(f"1. {initial_buildings[0]}")
    # print(f"2. {initial_buildings[1]}")

    # Display the game instructions or any additional information if needed

    await_user()


# End a game and clean up variables
def end_game(loc_game_vars, loc_field):
    score = calculate_score(loc_field, loc_game_vars)
    print(f"Game Over! Your final score is: {score}")

    # Check if the score is high enough for the high score list
    high_scores = load_high_scores()
    if is_high_score(score, high_scores):
        print("Congratulations! You've made it to the high score list!")
        player_name = input("Enter your name: ")
        update_high_scores(score, player_name)

    # Reset game variables and return to the main menu
    reset_game(loc_game_vars, loc_field)


# Helper function for end_game to clean up
def reset_game(loc_game_vars, loc_field):
    loc_game_vars["turn"] = 0
    loc_game_vars["coins"] = 16
    loc_game_vars["score"] = 0
    loc_game_vars["game_state"] = "MENU"

    # Clear the game field
    for i in range(len(loc_field)):
        for j in range(len(loc_field[0])):
            loc_field[i][j] = ''

    await_user()


# Check if the high score should be added in
def is_high_score(score, high_scores):
    return len(high_scores) < 10 or score > high_scores[-1][1]


# Load high scores and return a list of lists
def load_high_scores():
    try:
        with open('high_scores.txt', 'r') as file:
            scores = [line.strip().split() for line in file.readlines()]
            file.close()
        for score_set in scores:
            score_set[1] = int(score_set[1])
        return scores
    except FileNotFoundError:
        return
    except Exception as e:
        print(f"An error occurred while loading high scores: {e}")
        return


# def update_high_scores(score, player_name="Anonymous"):
#    try:
#        with open('high_scores.txt', 'a') as file:
#            file.write(f"{player_name} {score}\n")
#    except Exception as e:
#        print(f"An error occurred while updating high scores: {e}")


# Rewrite high_scores.txt with new player data
def update_high_scores(score, player_name="Anonymous"):
    try:
        scores = load_high_scores()
        scores.append([player_name, score])
        scores.sort(key=lambda x: x[1], reverse=True)
        scores = scores[:10]  # Keep only the top  scores
        with open('high_scores.txt', 'w') as file:
            for name, score in scores:
                file.write(f"{name} {score}\n")
    except Exception as e:
        print(f"An error occurred while updating high scores: {e}")


# Main game loop, displays main menu then changes game state if a game has been started
if __name__ == "__main__":
    while True:
        print("Ngee Ann City")
        print("-------------")
        print("Build it Better!\n")
        while game_vars["game_state"] == "MENU":
            selected_action = show_main_menu()
            if selected_action == 1:
                start_game(game_vars, field)
            elif selected_action == 2:
                load_game(game_vars, field)
            elif selected_action == 3:
                show_high_scores()
            elif selected_action == 4:
                raise SystemExit

        while game_vars["game_state"] == "PLAYING":
            run_turn(game_vars, field)

        if game_vars["game_state"] == "OVER":
            end_game(game_vars, field)
