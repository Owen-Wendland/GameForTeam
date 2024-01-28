import pygame
import sys
import os
from pygame.locals import *

cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
sys.path.append(cwd + '\\dat')
import constants

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = constants.screenSize[0]
SCREEN_HEIGHT = constants.screenSize[1]
BUTTON_WIDTH = constants.screenSize[0]/2
BUTTON_HEIGHT = constants.screenSize[1]/3
BUTTON_MARGIN = constants.screenSize[1]/12
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Menu")

# Font
font = pygame.font.Font(None, 36)

# Function to display text on a button
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                # Execute code from main.py when the "Start" button is pressed
                os.system('python' + ' "' + str(os.getcwd()) + '\\src\\main.py"')
                #pygame.quit()
                #sys.exit()
                
            elif end_button_rect.collidepoint(event.pos):
                # Close the program when the "End" button is pressed
                pygame.quit()
                sys.exit()

    # Draw the buttons
    screen.fill(WHITE)

    start_button_rect = pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
                                                         SCREEN_HEIGHT // 2 - BUTTON_HEIGHT - BUTTON_MARGIN,
                                                         BUTTON_WIDTH, BUTTON_HEIGHT))
    draw_text("Start", font, WHITE, SCREEN_WIDTH // 2, 
              SCREEN_HEIGHT // 2 - BUTTON_HEIGHT // 2 - BUTTON_MARGIN)

    end_button_rect = pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2,
                                                       SCREEN_HEIGHT // 2 + BUTTON_MARGIN,
                                                       BUTTON_WIDTH, BUTTON_HEIGHT))
    draw_text("End", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + BUTTON_HEIGHT // 2 + BUTTON_MARGIN)

    pygame.display.flip()
