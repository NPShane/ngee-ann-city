import random
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


field = [[None for _ in range(20)] for _ in range(20)]


def draw_field():
    num_rows = len(field)
    num_cols = len(field[0])
    # Print column numbers and top line
    print('     ')
    for i in range(len(field[0])):
        print(f'{i + 1:6}', end='')
    print('\n  +' + '-----+' * num_cols)
    # Print each row
    for row_num in range(num_rows):
        # Print line that shows names and row alphabets
        print(f" {chr(row_num + 65)}|", end='')
        for col_num in range(num_cols):
            print('     |', end='')
        # Print line that shows unit health
        print(f"\n  |", end='')
        for col_num in range(num_cols):
            print('     |', end='')
        # Close off row with last line
        print('\n  +' + '-----+' * num_cols)

    print("  Coins: " + "Points: " + "Turn: ")

    await_user()

    show_building_types()

    await_user()

    building_given()

    await_user()


def show_building_types():
    # Print options
    print("Build a Building - Building Types Available")
    print("-------------------------------------------")
    print("Commercial - Cost: 1 coin")
    print("Industry - Cost: 1 coin")
    print("Park - Cost: 1 coin")
    print("Residential - Cost: 1 coin")
    print("Road - Cost: 1 coin")


def building_given():
    buildingList = ["Commercial", "Industry", "Park", "Residential", "Road"]
    random_building = random.sample(buildingList, 2)
    # print(random_building) # For debugging purposes

    print("You have been offered")
    print("---------------------")
    print("[1]", random_building[0])
    print("[2]", random_building[1])
    print()
    print("Choose your option (1 or 2):")
    option = get_input(2)
    return option


def show_building_menu(game_vars):
    # Print options
    print("1. Buy unit     2. End turn     3. Upgrade unit")
    print("4. Save game    5. Quit")
    # Get what user wants to do
    option = get_input(5)
    return option


def place_unit(field, position, unit_name):
    # Declare local variables needed for both defenders and monsters
    pos_validity = False
    row_num = ord(position[0]) - 65
    col_num = int(position[-1]) - 1
    num_rows = len(field)
    num_cols = len(field[0])
    ## Check if coordinates within the board
    # if row_num <= num_rows and row_num >= 0:
    #    if col_num <= num_cols and col_num >= 0:
    #        # Check if position is empty
    #        if field[row_num][col_num] == None:
    # Check if a building exists

    # if unit_name in defenders:
    #    if col_num < 3 or unit_name == 'MINE':
    #        # Initalise defender and set it on the field
    #        unit = {}
    #        unit['name'] = defenders[unit_name]['name']
    #        unit['short_name'] = defenders[unit_name]['short_name']
    #        unit['maxHP'] = defenders[unit_name]['maxHP']
    #        unit['HP'] = defenders[unit_name]['maxHP']
    #        unit['min_damage'] = defenders[unit_name]['min_damage']
    #        unit['max_damage'] = defenders[unit_name]['max_damage']
    #        unit['price'] = defenders[unit_name]['price'] + 3
    #        # Special case: cannons need to keep track of when they fire
    #        if unit['short_name'] == 'CANON':
    #            if game_vars['turn'] % 2 == 0:
    #                unit['fire_cycle'] = 'even'
    #            else:
    #                unit['fire_cycle'] = 'odd'
    #        field[row_num][col_num] = unit
    #        pos_validity = True
    #        # Immediately activate unit if needed
    #        if unit_name == 'HEAL':
    #            defender_attack('Heal/Repair', field, row_num, col_num)
    # else: # Initalise monster and set it on the field
    #    unit = {}
    #    unit['name'] = monsters[unit_name]['name']
    #    unit['short_name'] = monsters[unit_name]['short_name']
    #    unit['maxHP'] = monsters[unit_name]['maxHP']
    #    unit['HP'] = monsters[unit_name]['maxHP']
    #    unit['min_damage'] = monsters[unit_name]['min_damage']
    #    unit['max_damage'] = monsters[unit_name]['max_damage']
    #    unit['reward'] = monsters[unit_name]['reward']
    #    field[row_num][col_num] = unit
    #    pos_validity = True
    return pos_validity


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
                game_playing = draw_field()
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

# -----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
# -----------------------------------------
# def save_game():
# file = open('save.txt', 'w')
# Store game_vars
# for var in game_vars.values():
# file.write(str(var))
# file.write(',')
# file.write('\n\n')
# Then store field
# for row in field:
# for unit in row:
# if unit:
# for attribute in unit.values():
# file.write(str(attribute))
# file.write(',')
# else:
# file.write('None')
# file.write(';')
# file.write('\n')
# file.write('\n')
# Then save player settings
# for setting in player_defined_vars.values():
# file.write(str(setting[0]))
# file.write(',')
# print("Game saved.")
# file.close()

# -----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
# -----------------------------------------
# def load_game(game_vars):
# try:
# file = open('save.txt')
# except FileNotFoundError:
# print('No save file to load from.')
# return False
# file_list = file.read().split('\n\n')
# setting_list = file_list.pop().split(',')[:-1]
# field_list = file_list.pop().split('\n')
# var_list = file_list.pop().split(',')[:-1]
# Load in game_vars from save
# count = 0
# for var in game_vars:
# if var_list[count].isdigit():
# game_vars[var] = int(var_list[count])
# elif var_list[count] == 'False':
# game_vars[var] = False
# elif var_list[count] == 'True':
# game_vars[var] = True
# count += 1
# Ready vars for use
# game_vars['turn'] -= 1
# for i in range(game_vars['danger_level']-1):
# for monster in monsters.values():
# monster['maxHP'] += 1
# monster['min_damage'] += 1
# monster['max_damage'] += 1
# monster['reward'] += 1
# Load in player settings and change other stuff using them
# count = 0
# for var in player_defined_vars:
# player_defined_vars[var][0] = int(setting_list[count])
# count += 1
# global field
# field = []
# for row in range(player_defined_vars['board_width'][0]):
# field.append([])
# for column in range(player_defined_vars['board_length'][0]):
# field[row].append(None)
# Load in field from save
# for row_num in range(len(field_list)):
# load_row = field_list[row_num].split(';')[:-1]
# for col_num in range(len(load_row)):
# load_space = load_row[col_num].split(',')
# if load_space[0] != 'None':
# unit = {}
# unit['name'] = load_space[0]
# unit['short_name'] = load_space[1]
# unit['maxHP'] = int(load_space[2])
# unit['HP'] = int(load_space[3])
# unit['min_damage'] = int(load_space[4])
# unit['max_damage'] = int(load_space[5])
# if unit['short_name'] in defenders:
# unit['price'] = int(load_space[6])
# if unit['short_name'] == 'CANON':
# unit['fire_cycle'] = load_space[7]
# else:
# unit['reward'] = int(load_space[6])
# field[row_num][col_num] = unit
# else:
# field[row_num][col_num] = None
# file.close()
# return True
