import tkinter
import tkinter.filedialog
import os
import time
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
timer = pygame.time.Clock()
screen = pygame.display.set_mode(size=(25 * 20, 25 * 20))



class ThreeChinese:
    def __init__(self, players_turns, turn_num, overall_turns, win = False, with_computer = False):
        pygame.mixer.init()
        self.players_turns = players_turns
        self.inner_color = (153, 204, 254)  # the button's color when you hover over the button
        self.button_color = (0, 128, 255)  # the button's color
        self.tokens_rect = []
        self.matrix = np.ones((17, 25)) * -1
        self.modify_matrix_for_star_shape()
        self.cell_size = 20
        self.col_num = 25
        self.lines_num = 25
        self.turn_num = turn_num
        self.overall_turns = overall_turns
        self.win = win
        self.with_computer = with_computer
        self.player_index = 1
        self.is_selecting = False
        self.player_valid_moves = []
        self.last_selected_token = []
        self.move_index = [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2]]
        self.first_aim = [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]]
        self.second_aim = [[4, 0], [4, 2], [4, 4], [4, 6], [5, 1], [5, 3], [5, 5], [6, 2], [6, 4], [7, 3]]
        self.third_aim = [[4, 18], [4, 20], [4, 22], [4, 24], [5, 19], [5, 21], [5, 23], [6, 20], [6, 22], [7, 21]]


    def modify_matrix_for_star_shape(self):
        matrix_index = [1, 2, 3, 4, 13, 12, 11, 10, 9]
        for i in range(9):
            j = 12
            first_time = True
            while matrix_index[i] > 0:
                if (i % 2 == 0) and first_time:
                    first_time = False
                    self.matrix[i][j] = self.matrix[16 - i][j] = 0
                    matrix_index[i] -= 1
                else:
                    j -= 1
                    self.matrix[i][j] = self.matrix[i][24 - j] = self.matrix[16 - i][j] = self.matrix[16 - i][
                        24 - j] = 0
                    matrix_index[i] -= 2
                j -= 1


    def initialize_logging(self):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file_name = f"game_log_{current_time}.log"
        logging.basicConfig(filename=log_file_name, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s: %(message)s')

    def add_player(self, index):
        self.first_player = self.players_turns[self.turn_num][0]
        self.second_player = self.players_turns[self.turn_num][1]
        self.third_player = self.players_turns[self.turn_num][2]
        if index == 1:
            for i in range(len(self.first_player)):
                self.matrix[self.first_player[i][0]][self.first_player[i][1]] = index
        if index == 2:
            for i in range(len(self.second_player)):
                self.matrix[self.second_player[i][0]][self.second_player[i][1]] = index
        if index == 3:
            for i in range(len(self.third_player)):
                self.matrix[self.third_player[i][0]][self.third_player[i][1]] = index

    def draw_tokens(self):
        """This function draws the tokens on the board"""
        colors = [(240, 230, 230), "red", "yellow", "orange"]
        for i in range(0, 17):
            for j in range(0, 25):
                if self.matrix[i][j] >= 0:
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                    self.tokens_rect.append(
                        pygame.draw.rect(screen, colors[int(self.matrix[i][j])], rect, border_radius=20))

    def valid_moves(self, coor):
        """This function returns the valid moves for a token"""
        valid_index = []
        for i in range(len(self.move_index)):
            x = coor[0] + self.move_index[i][0]
            y = coor[1] + self.move_index[i][1]
            if -1 < x < 17 and -1 < y < 25:
                if self.matrix[x][y] == 0:
                    valid_index.append([x, y])
                elif self.matrix[x][y] != -1:
                    self.check_path(self.move_index[i], x, y, valid_index)
        return valid_index

    def check_path(self, path_coor, x, y, moves_array):
        x2 = x + path_coor[0]
        y2 = y + path_coor[1]
        if [x2, y2] not in moves_array:
            if -1 < x2 < 17 and -1 < y2 < 25:
                if self.matrix[x2][y2] == 0:
                    moves_array.append([x2, y2])
                    for j in range(len(self.move_index)):
                        x3 = x2 + self.move_index[j][0]
                        y3 = y2 + self.move_index[j][1]
                        if [x3, y3] not in moves_array:
                            if -1 < x3 < 17 and -1 < y3 < 25:
                                if self.matrix[x3][y3] > 0:
                                    self.check_path(self.move_index[j], x3, y3, moves_array)

    def move(self, pos, target):
        """This function moves the token from the current position to the target position"""
        self.matrix[target[0]][target[1]] = self.matrix[pos[0]][pos[1]]
        self.matrix[pos[0]][pos[1]] = 0

    def get_token_coor(self, x, y):
        """This function returns the coordinates of the token in relation to the grid"""
        grid_width = 0
        grid_heigth = 0
        coor = [int((y - grid_heigth) / 20), int((x - grid_width) / 20)]
        return coor


    def animation(self, moves=[], clicked_token=None):
        """This function animates the player's moves on the board"""
        self.colors = [(240, 230, 230), "red", "yellow", "orange"]
        moves.append(clicked_token)

        # Draw the game board and circles
        for i in range(0, 17):
            for j in range(0, 25):
                if self.matrix[i][j] >= 0:
                    # Draw tokens
                    rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                    self.tokens_rect.append(pygame.draw.rect(screen, self.colors[int(self.matrix[i][j])], rect, border_radius=20))

                if [i, j] in moves:
                    # Draw circles
                    circle_image = pygame.image.load('circle.png')
                    circle_image = pygame.transform.scale(circle_image, (self.cell_size+3, self.cell_size+3))
                    screen.blit(circle_image, (j * self.cell_size-2, i * self.cell_size-2))

    def show_grid(self):
        """This function shows the grid of the game"""
        for i in range(0, self.col_num):
            for j in range(0, self.lines_num):
                rect = pygame.Rect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)
                # Draw semi-transparent rectangles with RGBA color
                pygame.draw.rect(screen, pygame.Color(255, 255, 255, 128), rect, width=1)

    def winner(self):
        """This function checks who's the winner and declares it with applause!"""
        second = True
        first = True
        third = True
        for i in range(len(self.first_aim)):
            if self.matrix[self.first_aim[i][0]][self.first_aim[i][1]] != 1:
                first = False
                break
        for i in range(len(self.second_aim)):
            if self.matrix[self.second_aim[i][0]][self.second_aim[i][1]] != 2:
                second = False
                break
        for i in range(len(self.third_aim)):
            if self.matrix[self.third_aim[i][0]][self.third_aim[i][1]] != 3:
                third = False
                break

        if first:
            self.write_text('Player 1 had won!', self.col_num * self.cell_size - 370, self.lines_num * self.cell_size - 100, 50, 'red')
            self.winner_sound.play()
            self.win = True
            return True
        elif second:
            self.write_text('Player 2 had won!', self.col_num * self.cell_size - 370, self.lines_num * self.cell_size - 100, 50, 'yellow')
            self.winner_sound.play()
            self.win = True
            return True
        elif third:
            self.write_text('Player 3 had won!', self.col_num * self.cell_size - 370, self.lines_num * self.cell_size - 100, 50, 'orange')
            self.winner_sound.play()
            self.win = True
            return True
        else:
            return False

    def write_text(self, text, text_pos_x, text_pos_y, text_size, col):
        text_font = pygame.font.SysFont(None, text_size)
        text_render = text_font.render(text, True, col)
        screen.blit(text_render, (text_pos_x, text_pos_y))

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))

            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))
        small_text = pygame.font.SysFont("comicsansms", 20)
        text_surf, text_rect = self.text_objects(msg, small_text)
        text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(text_surf, text_rect)

    def text_objects(self, text, font):
        text_surface = font.render(text, True, "white")
        return text_surface, text_surface.get_rect()


    def load_sound(self, file_path):
        try:
            return pygame.mixer.Sound(file_path)
        except pygame.error as e:
            print("Cannot load sound:", file_path)
            raise SystemExit(str(e))



    def main_loop(self):
        self.move_sound = self.load_sound(r"C:\Users\roni2\PycharmProjects\Chinesecheckers\move.mp3")  # Load the move sound file
        self.winner_sound = self.load_sound(
            r"C:\Users\roni2\PycharmProjects\Chinesecheckers\applause.mp3")  # Load the winner sound file
        screen = pygame.display.set_mode(size=(self.col_num * self.cell_size, self.lines_num * self.cell_size))
        timer = pygame.time.Clock()
        self.add_player(1)
        self.add_player(2)
        self.add_player(3)
        self.show_grid()
        self.player_index = 1
        #self.turn_num = 0
        #self.draw_tokens()
        screen.fill(pygame.Color("white"))  # Clear the screen
        game_on = True


        while game_on:

            # Draw the game components
            #self.show_grid()
            self.animation()
            self.buttons()


            first_player_coords = [(i, j) for i in range(17) for j in range(25) if self.matrix[i][j] == 1]
            second_player_coords = [(i, j) for i in range(17) for j in range(25) if self.matrix[i][j] == 2]
            third_player_coords = [(i, j) for i in range(17) for j in range(25) if self.matrix[i][j] == 3]

            if self.player_index == 1:
                color = 'red'
            elif self.player_index == 2:
                color = 'yellow'
            elif self.player_index == 3:
                color = 'orange'

            if not self.winner():
                self.write_text(f'Player {self.player_index}\'s Turn', self.col_num * self.cell_size - 370, self.lines_num * self.cell_size - 100, 50, color)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.win:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in self.tokens_rect if s.collidepoint(pos)]

                    if clicked_sprites:
                        clicked_token = self.get_token_coor(clicked_sprites[0].x, clicked_sprites[0].y)
                        if self.matrix[clicked_token[0], clicked_token[1]] == self.player_index:
                            if clicked_token == self.last_selected_token:
                                self.is_selecting = False
                                self.last_selected_token = []
                                self.player_valid_moves = []
                                screen.fill(pygame.Color("white"))
                                self.animation()
                            else:
                                self.player_valid_moves = self.valid_moves(clicked_token)
                                self.last_selected_token = clicked_token
                                self.is_selecting = True
                                screen.fill(pygame.Color("white"))
                                self.animation(self.player_valid_moves, self.last_selected_token)

                        elif clicked_token in self.player_valid_moves:
                            self.move(self.last_selected_token, clicked_token)
                            self.winner()
                            self.is_selecting = False
                            self.last_selected_token = []
                            self.player_valid_moves = []
                            screen.fill(pygame.Color("white"))
                            self.player_index = (self.player_index + 1) % 4
                            if self.player_index == 0:
                                self.player_index += 1
                            self.move_sound.play()
                            self.animation()

                            if self.player_index == 3 and not self.winner() and self.with_computer:
                                computer_moves = []
                                for i in range(17):
                                    for j in range(25):
                                        if self.matrix[i][j] == 3:
                                            moves_list = self.valid_moves([i, j])
                                            for o in moves_list:
                                                computer_moves.append(([i, j], o))

                                if computer_moves:
                                    selected_move = random.choice(computer_moves)
                                    self.move(selected_move[0], selected_move[1])
                                    self.winner()
                                    self.animation()
                                    self.player_index = 1

                            if self.player_index == 1:
                                self.turn_num += 1
                                self.overall_turns = self.turn_num
                                self.players_turns.append([first_player_coords, second_player_coords, third_player_coords])
            pygame.display.update()
            timer.tick(60)

    def move_forward(self):
        sleep = time.sleep(1)
        load_next_turn = ThreeChinese(self.players_turns, self.turn_num + 1, self.overall_turns, self.win,
                                             self.with_computer)
        load_next_turn.main_loop()


    def buttons(self):
        if self.turn_num < self.overall_turns:
            self.button("move forward", 300, 460, 140, 30, self.button_color, self.inner_color,
                        lambda: self.move_forward())
            rect2 = pygame.draw.rect(screen, self.button_color, pygame.Rect(294, 454, 152, 42), 6, 20)

        self.button("return main", 26, 460, 140, 30, self.button_color, self.inner_color, self.return_main_action)
        rect3 = pygame.draw.rect(screen, self.button_color, pygame.Rect(20, 454, 152, 42), 6, 20)
        self.button("load game", 182, 460, 135, 30, self.button_color, self.inner_color,
                    lambda: self.load_game(self.prompt_file()))
        rect4 = pygame.draw.rect(screen, self.button_color, pygame.Rect(176, 454, 146, 42), 6, 20)


    def prompt_file(self):
        top = tkinter.Tk()
        top.withdraw()  # hide window
        file_name = tkinter.filedialog.askopenfilename(parent=top)
        file_path = os.path.abspath(file_name)
        top.destroy()
        return file_path


    def load_log_file(self, file_path):
        with open(file_path, 'r') as file:
            log_lines = file.readlines()
        return log_lines

    def extract_game_state_from_log(self, log_lines):
        pattern = r"\{.*\}"
        for line in log_lines:
            match = re.search(pattern, line)
            if match:
                dict_string = match.group()
                str_dict = dict_string.replace("'", '"')
                try:
                    dict_values = json.loads(str_dict)
                except json.decoder.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    continue
                if 'game_state' in dict_values:
                    return dict_values['game_state']
    def load_game(self,file_path):
        log_lines = self.load_log_file(file_path)
        game_state = self.extract_game_state_from_log(log_lines)  # Load the game state from the log file
        if game_state and len(game_state['players_turns'][0]) == 3:
            print(game_state)
            turn = ThreeChinese(game_state['players_turns'], 0, game_state['overall_turns'], game_state['win'],
                       game_state['with_computer'])
            turn.main_loop()


    def return_main_action(self):
        logging.info(json.dumps({"game_state": {"num_players": 3, "players_turns": self.players_turns,
                                                "turn_num": self.turn_num, "overall_turns": self.overall_turns, "win": self.win,
                                                "with_computer": self.with_computer}}))
        second_interface.second_page()


pygame.display.update()
timer.tick(60)
