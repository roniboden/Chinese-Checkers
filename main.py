import pygame
import sys
import argparse
import second_interface
import help
import os


# Define your ArgumentParser
parser = argparse.ArgumentParser(description="Hello! You may use this script to play a game of Chinese Checkers. "
          "You can play with 2, 3, 4, 5, or 6 players. You can also play with computer players by pressing 2c for example."
          " To play the game, you need to click on the 'Play Game' button. "
          "To quit the game, you need to click on the 'Quit' button. " 
          "To see the game instructions, you can click on the 'Help' button.")

# Parse the arguments
args = parser.parse_args()

def first_page():
    inner_color = (153, 204, 254)  # the button's color when you hover over the button
    button_color = (0, 128, 255)  # the button's color 

    pygame.init()

    os.environ['SDL_VIDEO_CENTERED'] = '1'

    window = pygame.display.set_mode((900, 600))

    image = pygame.image.load("background.png")
    image = image.convert()


    def text_objects(text,font):
        textsurface = font.render(text, True, "white")
        return textsurface, textsurface.get_rect()
    def button(msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(window, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(window, ic, (x, y, w, h))
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        window.blit(textSurf, textRect)
    running = True
    while running:
        window.blit(pygame.transform.scale(image, (900, 600)), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        button("Play Game", 380, 400, 150, 50, button_color, inner_color, lambda: second_interface.second_page())
        button("Quit", 10, 400, 88, 30, button_color, inner_color, quit)
        button("Help", 10, 450, 88, 30, button_color, inner_color, help.help)
        rect = pygame.draw.rect(window, button_color, pygame.Rect(374, 394, 162, 62), 6, 20)
        rect2 = pygame.draw.rect(window, button_color, pygame.Rect(4, 394, 100, 42), 6, 20)
        rect3 = pygame.draw.rect(window, button_color, pygame.Rect(4, 444, 100, 42), 6, 20)
        pygame.display.update()
        pygame.display.flip()


    pygame.quit()
first_page()



# If --help was provided, argparse will automatically print the help message and halt the program.
# If --help was not provided, you can call your main function.
if not ('--help' in sys.argv or '-h' in sys.argv):
    first_page()