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

pygame.init()

inner_color = (153, 204, 254)  # the button's color when you hover over the button
button_color = (0, 128, 255)     # the button's color


# Function to load sounds
def load_sound(file_path):
    """This function loads the sound file from the given path and makes sure it can be loaded."""
    try:
        return pygame.mixer.Sound(file_path)
    except pygame.error as e:
        print("Cannot load sound:", file_path)
        raise SystemExit(str(e))


def initialize_logging():
    """This function initializes the logging module to log game conduct."""
    # Get current timestamp to create a unique log file name
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"game_log_{current_time}.log"

    # Configure logging
    logging.basicConfig(filename=log_file_name, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s')



initialize_logging()
pygame.mixer.init()
move_sound = load_sound(r"C:\Users\roni2\PycharmProjects\Chinesecheckers\move.mp3")  # Load the move sound file
winner_sound = load_sound(
    r"C:\Users\roni2\PycharmProjects\Chinesecheckers\applause.mp3")  # Load the winner sound file



class ThreePlayers:
    def __init__(self, players_turns, turn_num, overall_turns, win, with_computer):
        self.players_turns = players_turns
        self.turn_num = turn_num
        self.overall_turns = overall_turns
        self.win = win
        self.with_computer = with_computer
        self.cell_size = 20
        self.col_num = 25
        self.lines_num = 25
        self.move_index = [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2]]
        self.screen = pygame.display.set_mode(size=(self.col_num * self.cell_size, self.lines_num * self.cell_size))
        self.tokens_rect = []
        initialize_logging()
        self.matrix, self.first_player, self.second_player, self.third_player, self.first_aim, self.second_aim, self.third_aim = self.build_matrix()
        pygame.mixer.init()
        self.move_sound = load_sound(r"C:\Users\roni2\PycharmProjects\Chinesecheckers\move.mp3")  # Load the move sound file
        self.winner_sound = load_sound(
            r"C:\Users\roni2\PycharmProjects\Chinesecheckers\applause.mp3")  # Load the winner sound file
        pygame.init()


    def build_matrix(self):
        first_player = self.players_turns[self.turn_num][0]
        second_player = self.players_turns[self.turn_num][1]
        third_player = self.players_turns[self.turn_num][2]


        # Initialize the game matrix and other necessary components
        matrix = np.ones((17, 25))
        matrix *= -1


        # Aims of the players
        first_aim = [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]]
        second_aim = [[4, 0], [4, 2], [4, 4], [4, 6], [5, 1], [5, 3], [5, 5], [6, 2], [6, 4], [7, 3]]
        third_aim = [[4, 18], [4, 20], [4, 22], [4, 24], [5, 19], [5, 21], [5, 23], [6, 20], [6, 22], [7, 21]]

        # movement indices


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
        return matrix, first_player, second_player, third_player, first_aim, second_aim, third_aim

    def add_player(self, index):
        """This function adds the players to the game matrix"""
        matrix, first_player, second_player, third_player, first_aim, second_aim, third_aim = self.build_matrix()
        if index == 1:
            for i in range(len(first_player)):
                matrix[first_player[i][0]][first_player[i][1]] = index
        if index == 2:
            for i in range(len(second_player)):
                matrix[second_player[i][0]][second_player[i][1]] = index
        if index == 3:
            for i in range(len(third_player)):
                matrix[third_player[i][0]][third_player[i][1]] = index
        self.add_player(1)
        self.add_player(2)
        self.add_player(3)

    def draw_tokens(self):
        """This function draws the tokens on the board"""
        colors = [(240, 230, 230), "red", "yellow", "orange"]
        matrix, first_player, second_player, third_player, first_aim, second_aim, third_aim = self.build_matrix()
        for i in range(0, 17):
            for j in range(0, 25):
                if matrix[i][j] >= 0:
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                    self.tokens_rect.append(pygame.draw.rect(self.screen, colors[int(matrix[i][j])], rect, border_radius=20))


    def valid_moves(self,coor):
        """This function returns the valid moves for a token"""
        matrix, first_player, second_player, third_player, first_aim, second_aim, third_aim = self.build_matrix()
        valid_index = []
        for i in range(len(self.move_index)):

            x = coor[0] + self.move_index[i][0]
            y = coor[1] + self.move_index[i][1]
            if -1 < x < 17 and -1 < y < 25:
                if matrix[x][y] == 0:
                    valid_index.append([x, y])
                elif matrix[x][y] != -1:
                    self.check_path(self.move_index[i], x, y, valid_index)

        return valid_index

    def check_path(self,path_coor, x, y, moves_array):
        """This function checks the path of the token"""
        matrix, first_player, second_player, third_player, first_aim, second_aim, third_aim = self.build_matrix()
        x2 = x + path_coor[0]
        y2 = y + path_coor[1]
        if [x2, y2] not in moves_array:
            if -1 < x2 < 17 and -1 < y2 < 25:
                if matrix[x2][y2] == 0:
                    moves_array.append([x2, y2])
                    for j in range(len(self.move_index)):
                        x3 = x2 + self.move_index[j][0]
                        y3 = y2 + self.move_index[j][1]
                        if [x3, y3] not in moves_array:
                            if -1 < x3 < 17 and -1 < y3 < 25:
                                if matrix[x3][y3] > 0:
                                    self.check_path(self.move_index[j], x3, y3, moves_array)

    def move(self,pos, target):
        """This function moves the token from the current position to the target position"""
        matrix, first_player, second_player, third_player, first_aim, second_aim, third_aim = self.build_matrix()
        matrix[target[0]][target[1]] = matrix[pos[0]][pos[1]]
        matrix[pos[0]][pos[1]] = 0

    def get_token_coor(self, x, y):
        """This function returns the coordinates of the token in relation to the grid"""
        grid_width = 0
        grid_heigth = 0
        coor = [int((y - grid_heigth) / 20), int((x - grid_width) / 20)]
        return coor

    def animation(self, moves=[], clicked_token=None):
        """This function animates the player's moves on the board"""
        matrix, first_player, second_player, third_player, first_aim, second_aim, third_aim = self.build_matrix()
        colors = [(240, 230, 230), "red", "yellow", "orange"]
        moves.append(clicked_token)
        for i in range(0, 17):
            for j in range(0, 25):
                if matrix[i][j] >= 0:
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                    self.tokens_rect.append(pygame.draw.rect(self.screen, colors[int(matrix[i][j])], rect, border_radius=20))
                if [i, j] in moves:
                    test_cercle = pygame.image.load('cercle.png')
                    test_cercle = pygame.transform.scale(test_cercle, (self.cell_size, self.cell_size))
                    self.screen.blit(test_cercle, (j * self.cell_size, i * self.cell_size))

    def show_grid(self):
        """This function shows the grid of the game"""
        for i in range(0, self.col_num):
            for j in range(0, self.lines_num):
                rect = pygame.Rect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, pygame.Color("white"), rect, width=1)

    def WriteText(self,text, text_pos_x, text_pos_y, text_size, col):
        """This function writes text on the screen"""
        text_font = pygame.font.SysFont(None, text_size)
        text_render = text_font.render(text, True, col)
        self.screen.blit(text_render, (text_pos_x, text_pos_y))

    def winner(self):
        """This function checks who's the winner and declares it with applause!"""
        matrix, first_player, second_player, third_player, first_aim, second_aim, third_aim = self.build_matrix()
        second = True
        first = True
        third = True
        for i in range(len(first_aim)):
            if matrix[first_aim[i][0]][first_aim[i][1]] != 1:
                first = False
                break
        for i in range(len(second_aim)):
            if matrix[second_aim[i][0]][second_aim[i][1]] != 2:
                second = False
                break
        for i in range(len(third_aim)):
            if matrix[third_aim[i][0]][third_aim[i][1]] != 3:
                third = False
                break

        if first == True:
            self.WriteText('Player 1 had won!', self.col_num * self.cell_size - 370, self.lines_num * self.cell_size - 100, 50, 'red')
            winner_sound.play()
            return True
        elif (second == True):
            self.WriteText('Player 2 had won!', self.col_num * self.cell_size - 370, self.lines_num * self.cell_size - 100, 50, 'yellow')
            winner_sound.play()
            return True
        elif (third == True):
            self.WriteText('Player 3 had won!', self.col_num * self.cell_size - 370, self.lines_num * self.cell_size - 100, 50, 'orange')
            winner_sound.play()
            return True
        else:
            return False



    # Adding the "return main" button
    def text_objects(self,text, font):
        textsurface = font.render(text, True, "white")
        return textsurface, textsurface.get_rect()

    def button(self,msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.screen, ic, (x, y, w, h))
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(textSurf, textRect)

    turn_num = 0
    game_on = True

    def run_game(self):
        while self.game_on:
            timer = pygame.time.Clock()
            self.screen.fill(pygame.Color("white"))
            self.draw_tokens()
            player_index = 1
            is_selecting = False
            player_valid_moves = []
            last_selected_token = []
            matrix, first_player, second_player, third_player, first_aim, second_aim, third_aim = self.build_matrix()
            first_player_coords = [(i, j) for i in range(17) for j in range(25) if matrix[i][j] == 1]
            second_player_coords = [(i, j) for i in range(17) for j in range(25) if matrix[i][j] == 2]
            third_player_coords = [(i, j) for i in range(17) for j in range(25) if matrix[i][j] == 3]
            if player_index == 1: color = 'red'
            if player_index == 2: color = 'yellow'
            if player_index == 3: color = 'orange'
            # player turn
            if (self.winner() == False):
                self.WriteText('Player ' + str(player_index) + '\'s Turn', self.col_num * self.cell_size - 370,
                          self.lines_num * self.cell_size - 100,
                          50, color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # get a list of all sprites that are under the mouse cursor
                    clicked_sprites = [s for s in self.tokens_rect if s.collidepoint(pos)]

                    if clicked_sprites:
                        clicked_token = self.get_token_coor(clicked_sprites[0].x, clicked_sprites[0].y)
                        if matrix[clicked_token[0], clicked_token[1]] == player_index:
                            if clicked_token == last_selected_token:
                                is_selecting = False
                                last_selected_token = []
                                player_valid_moves = []
                                self.screen.fill(pygame.Color("white"))
                                self.animation()
                            else:
                                player_valid_moves = self.valid_moves(clicked_token)
                                last_selected_token = clicked_token
                                is_selecting = True
                                self.screen.fill(pygame.Color("white"))
                                self.animation(player_valid_moves, last_selected_token)
                        elif clicked_token in player_valid_moves:
                            self.move(last_selected_token, clicked_token)
                            self.winner()
                            is_selecting = False
                            last_selected_token = []
                            player_valid_moves = []
                            self.screen.fill(pygame.Color("white"))
                            player_index = (player_index + 1) % 4
                            if player_index == 0:
                                player_index += 1

                            move_sound.play()
                            self.animation()
                if player_index == 3 and not self.winner() and self.with_computer:  # Check if it's the computer's turn
                    # Generate a list of legal moves for the computer
                    computer_moves = []
                    for i in range(17):
                        for j in range(25):
                            if matrix[i][j] == 3:  # Check if the token belongs to the computer
                                moves_list = self.valid_moves([i, j])
                                for o in moves_list:
                                    computer_moves.append(([i, j], o))

                    # Select a random move for the computer
                    if computer_moves:
                        selected_move = random.choice(computer_moves)
                        self.move(selected_move[0], selected_move[1])  # Make the selected move
                        self.winner()  # Check if the computer has won
                        # move_sound.play()
                        self.animation()
                        player_index = 1
                        if player_index == 1:
                            self.turn_num += 1
                            overall_turns = self.turn_num
                            self.players_turns.append([first_player_coords, second_player_coords, third_player_coords])


        def return_main_action():
            # Log the game conduct
            logging.info(json.dumps({"game_state": {"num_players": 3, "players_turns": self.players_turns,
                                                    "turn_num": self.turn_num, "overall_turns": overall_turns, "win": self.win,
                                                    "with_computer": self.with_computer}}))
            # Return to second page
            second_interface.second_page()

        if self.turn_num < overall_turns:
            self.button("move forward", 300, 460, 140, 30, button_color, inner_color,
                   lambda: ThreePlayers(self.players_turns, self.turn_num + 1, overall_turns, self.win, self.with_computer))
            rect2 = pygame.draw.rect(self.screen, button_color, pygame.Rect(294, 454, 152, 42), 6, 20)
        self.button("return main", 26, 460, 140, 30, button_color, inner_color, return_main_action)
        rect3 = pygame.draw.rect(self.screen, button_color, pygame.Rect(20, 454, 152, 42), 6, 20)
        self.button("load game", 182, 460, 135, 30, button_color, inner_color,
               lambda: load_game(prompt_file()))
        rect4 = pygame.draw.rect(self.screen, button_color, pygame.Rect(176, 454, 146, 42), 6, 20)

        def prompt_file():
            """Create a Tk file dialog and cleanup when finished"""
            top = tkinter.Tk()
            top.withdraw()  # hide window
            file_name = tkinter.filedialog.askopenfilename(parent=top)
            file_path = os.path.abspath(file_name)
            top.destroy()
            return file_path

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
            game_state = extract_game_state_from_log(log_lines)  # Load the game state from the log file
            if game_state and len(game_state['players_turns'][0]) == 3:
                ThreePlayers(game_state['players_turns'], 0, game_state['overall_turns'], game_state['win'],
                           game_state['with_computer'])

        pygame.display.update()
        timer.tick(60)