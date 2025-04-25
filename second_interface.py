import pygame
import two_players_oop
import three_players_oop
import four_players_oop
import six_players_oop
import help


red = [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]  # red
yellow = [[4, 18], [4, 20], [4, 22], [4, 24], [5, 19], [5, 21], [5, 23], [6, 20], [6, 22], [7, 21]]  # yellow
orange = [[12, 18], [12, 20], [12, 22], [12, 24], [11, 19], [11, 21], [11, 23], [10, 20], [10, 22],
                [9, 21]]  # orange
green = [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13],
                [13, 15]]  # green
pink = [[12, 0], [12, 2], [12, 4], [12, 6], [11, 1], [11, 3], [11, 5], [10, 2], [10, 4], [9, 3]]  # pink
blue = [[4, 0], [4, 2], [4, 4], [4, 6], [5, 1], [5, 3], [5, 5], [6, 2], [6, 4], [7, 3]]  # blue


def second_page():
    inner_color = (153, 204, 254)    # the button's color when you hover over the button
    button_color = (0, 128, 255)     # the button's color 
    pygame.init()
    window=pygame.display.set_mode((900,600))
    image = pygame.image.load("background.png")
    image = image.convert()
    choose_font = pygame.font.SysFont("Comic Sans MS", 50)
    text = choose_font.render('Choose number of players', True,(0, 128, 255))
    textRect = text.get_rect()
    textRect.center=(450,400)


    def text_objects(text,font):
        textsurface =font.render(text, True, "white")
        return textsurface , textsurface.get_rect()
    def button(msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(window, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(window, ic, (x, y, w, h))
        button_font = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects(msg, button_font)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        window.blit(textSurf, textRect)
    running= True
    while running:
      events = pygame.event.get()
      window.blit(pygame.transform.scale(image, (900, 600)), (0, 0))
      window.blit(text,textRect)
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running= False

      def start_game_two(with_computer):
          two_object = two_players_oop.TwoChinese([[red,green]],0,0,False,with_computer)
          two_object.main_loop()
      def start_game_three(with_computer):
          three_object = three_players_oop.ThreeChinese([[red,orange,pink]],0,0,False,with_computer)
          three_object.main_loop()
      def start_game_four(with_computer):
          four_object = four_players_oop.FourChinese([[yellow,orange,pink,blue]],0,0,False,with_computer)
          four_object.main_loop()
      def start_game_six(with_computer):
          six_object = six_players_oop.SixChinese([[red,yellow,orange,green,pink,blue]],0,0,False,with_computer)
          six_object.main_loop()

      # Call the method using the object

      button("2", 290, 300, 50, 30, button_color, inner_color, lambda: start_game_two(False))
      button("2c", 290, 250, 50, 30, button_color, inner_color, lambda: start_game_two(True))
      button("3", 360, 300, 50, 30, button_color, inner_color, lambda: start_game_three(False))
      button("3c", 360, 250, 50, 30, button_color, inner_color, lambda: start_game_three(True))
      button("4", 430, 300, 50, 30, button_color, inner_color, lambda: start_game_four(False))
      button("4c", 430, 250, 50, 30, button_color, inner_color, lambda: start_game_four(True))
      button("6", 500, 300, 50, 30, button_color, inner_color, lambda: start_game_six(False))
      button("6c", 500, 250, 50, 30, button_color, inner_color, lambda: start_game_six(True))
      button("Quit", 10, 400, 88, 30, button_color, inner_color, quit)
      button("Help", 10, 450, 88, 30, button_color, inner_color, help.help)

      # Drawing rectangles around the buttons
      button_quit = pygame.draw.rect(window, button_color, pygame.Rect(4, 394, 100, 42), 6, 20)
      button_help = pygame.draw.rect(window, button_color, pygame.Rect(4, 444, 100, 42), 6, 20)
      button_2 = pygame.draw.rect(window, button_color, pygame.Rect(284, 294, 62, 42), 6, 20)
      button_2c = pygame.draw.rect(window, button_color, pygame.Rect(284, 244, 62, 42), 6, 20)
      button_3 = pygame.draw.rect(window, button_color, pygame.Rect(354, 294, 62, 42), 6, 20)
      button_3c = pygame.draw.rect(window, button_color, pygame.Rect(354, 244, 62, 42), 6, 20)
      button_4 = pygame.draw.rect(window, button_color, pygame.Rect(424, 294, 62, 42), 6, 20)
      button_4c = pygame.draw.rect(window, button_color, pygame.Rect(424, 244, 62, 42), 6, 20)
      button_6 = pygame.draw.rect(window, button_color, pygame.Rect(494, 294, 62, 42), 6, 20)
      button_6c = pygame.draw.rect(window, button_color, pygame.Rect(494, 244, 62, 42), 6, 20)
      pygame.display.update()
      pygame.display.flip()

    pygame.quit()





