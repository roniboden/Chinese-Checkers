import tkinter
import tkinter.filedialog
import os
import pygame
import sys
import second_interface
import numpy as np
import logging
import datetime
import random
import json
import re

inner_color = (153, 204, 254)   # the button's color when you hover over the button
button_color = (0, 128, 255)     # the button's color 

# Function to load sounds
def load_sound(file_path):
    try:
        return pygame.mixer.Sound(file_path)
    except pygame.error as e:
        print("Cannot load sound:", file_path)
        raise SystemExit(str(e))

def initialize_logging():
    # Get current timestamp to create a unique log file name
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"game_log_{current_time}.log"

    # Configure logging
    logging.basicConfig(filename=log_file_name, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s')


initialize_logging()

def TwoPlayers(players_turns, turn_num, overall_turns, win = False, with_computer=False):
    pygame.init()
    pygame.mixer.init()
    move_sound = load_sound(r"C:\Users\roni2\PycharmProjects\Chinesecheckers\move.mp3") # Load the move sound file
    winner_sound = load_sound(r"C:\Users\roni2\PycharmProjects\Chinesecheckers\applause.mp3") # Load the winner sound file

    # Players first positions
    first_player = players_turns[turn_num][0]
    second_player = players_turns[turn_num][1]

    # Initialize the game matrix and other necessary components
    matrix = np.ones((17, 25))
    matrix *= -1

    # movement indices
    move_index = [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2]]

    # Modify matrix for the star shape
    matrix_index = [1, 2, 3, 4, 13, 12, 11, 10, 9]
    for i in range(9):
        j = 12
        first_time = True
        while matrix_index[i] > 0:
            if (i % 2 == 0) and first_time:
                first_time = False
                matrix[i][j] = matrix[16 - i][j] = 0
                matrix_index[i] -= 1
            else:
                j -= 1
                matrix[i][j] = matrix[i][24 - j] = matrix[16 - i][j] = matrix[16 - i][24 - j] = 0
                matrix_index[i] -= 2
            j -= 1

    # Add players to the game matrix
    def add_player(index):
        player_positions = first_player if index == 1 else second_player
        for pos in player_positions:
            matrix[pos[0]][pos[1]] = index

    add_player(1)
    add_player(2)



    # Function to draw tokens
    def draw_tokens():
        colors = [(240, 230, 230), "red", "green"]
        for i in range(0, 17):
            for j in range(0, 25):
                if matrix[i][j] >= 0:
                    rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                    tokens_rect.append(pygame.draw.rect(screen, colors[int(matrix[i][j])], rect, border_radius=20))


    def valid_moves(coor):
        """This function returns the valid moves for a token"""
        valid_index = []
        for i in range(len(move_index)):

            x = coor[0] + move_index[i][0]
            y = coor[1] + move_index[i][1]
            if -1 < x < 17 and -1 < y < 25:
                if matrix[x][y] == 0:
                    valid_index.append([x, y])
                elif matrix[x][y] != -1:
                    check_path(move_index[i], x, y, valid_index)

        return valid_index

    # possible path
    def check_path(path_coor, x, y, moves_array):
        x2 = x + path_coor[0]
        y2 = y + path_coor[1]
        if [x2, y2] not in moves_array:
            if -1 < x2 < 17 and -1 < y2 < 25:
                if matrix[x2][y2] == 0:
                    moves_array.append([x2, y2])
                    for j in range(len(move_index)):
                        x3 = x2 + move_index[j][0]
                        y3 = y2 + move_index[j][1]
                        if [x3, y3] not in moves_array:
                            if -1 < x3 < 17 and -1 < y3 < 25:
                                if matrix[x3][y3] > 0:
                                    check_path(move_index[j], x3, y3, moves_array)

    # the function that moves the token
    def move(pos, target):
        matrix[target[0]][target[1]] = matrix[pos[0]][pos[1]]
        matrix[pos[0]][pos[1]] = 0

    # the coordinates locations in relation to the grid
    def get_token_coor(x, y):
        grid_width = 0
        grid_heigth = 0
        coor = [int((y - grid_heigth) / 20), int((x - grid_width) / 20)]
        return coor

    # animation that animates the player's possible moves based on the clicked token
    def animation(moves=[], clicked_token=None):
        colors = [(240, 230, 230), "red", "green"]
        moves.append(clicked_token)
        for i in range(0, 17):
            for j in range(0, 25):
                if matrix[i][j] >= 0:
                    rect = pygame.Rect(j * cell_size, i * cell_size, cell_size, cell_size)
                    tokens_rect.append(pygame.draw.rect(screen, colors[int(matrix[i][j])], rect, border_radius=20))
                if [i, j] in moves:
                    test_cercle = pygame.image.load('cercle.png')
                    test_cercle = pygame.transform.scale(test_cercle, (cell_size, cell_size))
                    screen.blit(test_cercle, (j * cell_size, i * cell_size))

    def show_grid():
        """This function shows the grid of the game"""
        for i in range(0, col_num):
            for j in range(0, lines_num):
                rect = pygame.Rect(i * cell_size, j * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, pygame.Color("white"), rect, width=1)


    def WriteText(text, text_pos_x, text_pos_y, text_size, col):
        """This function writes text on the screen"""
        text_font = pygame.font.SysFont(None, text_size)
        text_render = text_font.render(text, True, col)
        screen.blit(text_render, (text_pos_x, text_pos_y))


    def winner():
        """This function checks who's the winner and declares it with applause!"""
        first = True
        second= True
        for i in range(len(first_player)):
            if matrix[first_player[i][0]][first_player[i][1]] != 2:
                second= False
                break
        for i in range(len(second_player)):
            if matrix[second_player[i][0]][second_player[i][1]] != 1:
                first = False
                break
        if second == True:
            WriteText('Player 2 had won!', col_num * cell_size - 370, lines_num * cell_size - 130, 50, 'green')
            winner_sound.play()
            win = True
            return True

        elif first == True :
            WriteText('Player 1 had won!', col_num * cell_size - 370, lines_num * cell_size - 130, 50,'red')
            winner_sound.play()
            win = True
            return True
        else:
            return False

    # creating the game window
    col_num = 25
    lines_num = 25
    cell_size = 20
    screen = pygame.display.set_mode(size=(col_num * cell_size, lines_num * cell_size))
    timer = pygame.time.Clock()
    game_on = True
    tokens_rect = []


    screen.fill(pygame.Color("white"))
    draw_tokens()
    player_index = 1
    is_selecting = False
    player_valid_moves = []
    last_selected_token = []

    # Adding the "return main" button
    def text_objects(text, font):
        textsurface = font.render(text, True, "white")
        return textsurface, textsurface.get_rect()

    def button(msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(textSurf, textRect)


    while game_on:
        first_player_coords = [(i, j) for i in range(17) for j in range(25) if matrix[i][j] == 1]
        second_player_coords = [(i, j) for i in range(17) for j in range(25) if matrix[i][j] == 2]
        # player turn
        if player_index == 2: color = 'green'
        if player_index == 1: color = 'red'
        if (winner() == False):
            WriteText('Player ' + str(player_index) + '\'s Turn', col_num * cell_size - 370, lines_num * cell_size - 100, 50, color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # get a list of all sprites that are under the mouse cursor
                clicked_sprites = [s for s in tokens_rect if s.collidepoint(pos)]

                if clicked_sprites:
                    clicked_token = get_token_coor(clicked_sprites[0].x, clicked_sprites[0].y)
                    if matrix[clicked_token[0], clicked_token[1]] == player_index:
                        if clicked_token == last_selected_token:
                            is_selecting = False
                            last_selected_token = []
                            player_valid_moves = []
                            screen.fill(pygame.Color("white"))
                            animation()

                        else:
                            player_valid_moves = valid_moves(clicked_token)
                            last_selected_token = clicked_token
                            is_selecting = True
                            screen.fill(pygame.Color("white"))
                            animation(player_valid_moves,last_selected_token)

                    elif clicked_token in player_valid_moves:
                        move(last_selected_token, clicked_token)
                        winner()
                        is_selecting = False
                        last_selected_token = []
                        player_valid_moves = []
                        screen.fill(pygame.Color("white"))
                        player_index = (player_index+1) % 3
                        if player_index == 0:
                            player_index += 1


                        move_sound.play()
                        animation()
                        if player_index == 2 and not winner() and with_computer:  # Check if it's the computer's turn
                            # Generate a list of legal moves for the computer
                            computer_moves = []
                            for i in range(17):
                                for j in range(25):
                                    if matrix[i][j] == 2:  # Check if the token belongs to the computer
                                        moves_list = valid_moves([i, j])
                                        for o in moves_list:
                                            computer_moves.append(([i, j], o))

                            # Select a random move for the computer
                            if computer_moves:
                                selected_move = random.choice(computer_moves)
                                move(selected_move[0], selected_move[1])  # Make the selected move
                                winner()  # Check if the computer has won
                                animation()
                                player_index = 1  # Switch back to player 1's turn
                        if player_index == 1:
                            turn_num += 1
                            overall_turns = turn_num
                            players_turns.append([first_player_coords, second_player_coords])

            if turn_num < overall_turns:
                button("move forward", 336, 460, 140, 30, button_color, inner_color,
                   lambda: TwoPlayers(players_turns, turn_num+1, overall_turns, win, with_computer))
                rect2 = pygame.draw.rect(screen, button_color, pygame.Rect(330, 454, 152, 42), 6, 20)

            def return_main_action():
                # Log the game conduct
                logging.info(json.dumps({"game_state": {"num_players": 2, "players_turns":players_turns,
                              "turn_num":turn_num, "overall_turns":overall_turns,"win":win,"with_computer":with_computer}}))
                # Return to second page
                second_interface.second_page()



            def load_log_file(file_path):
                with open(file_path, 'r') as file:
                    log_lines = file.readlines()
                return log_lines

            def extract_game_state_from_log(log_lines):
                # Define a regular expression pattern to match dictionary strings
                pattern = r"\{.*\}"
                for line in log_lines:
                    match = re.search(pattern, line)
                    if match:
                        # Extract the dictionary string
                        dict_string = match.group()
                        str_dict = dict_string.replace("'", '"')

                        # Load the string as a dictionary
                        dict_values = json.loads(str_dict)

                        # Parse the dictionary string into a dictionary
                        try:
                            dict_values = json.loads(dict_string)
                        except json.decoder.JSONDecodeError as e:
                            print(f"Error decoding JSON: {e}")
                            continue
                        # Check if 'game_state' key exists in the dictionary
                        if 'game_state' in dict_values:
                            return dict_values['game_state']

            def load_game(file_path):
                log_lines = load_log_file(file_path)
                game_state = extract_game_state_from_log(log_lines)        # Load the game state from the log file
                if game_state and len(game_state['players_turns'][0]) == 2:
                    TwoPlayers(game_state['players_turns'], 0, game_state['overall_turns'], game_state['win'], game_state['with_computer'])


            # Modify the button call
            button("return main", 26, 460, 140, 30, button_color, inner_color, return_main_action)
            rect3 = pygame.draw.rect(screen, button_color, pygame.Rect(20, 454, 152, 42), 6, 20)
            button("load game", 182, 460, 135, 30, button_color, inner_color,
                   lambda: load_game(prompt_file()))
            rect4 = pygame.draw.rect(screen, button_color, pygame.Rect(176, 454, 146, 42), 6, 20)


        def prompt_file():
            """Create a Tk file dialog and cleanup when finished"""
            top = tkinter.Tk()
            top.withdraw()  # hide window
            file_name = tkinter.filedialog.askopenfilename(parent=top)
            file_path = os.path.abspath(file_name)
            top.destroy()
            return file_path


        pygame.display.update()
        timer.tick(60)


