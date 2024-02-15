import pygame
import sys
# Initialize Pygame
pygame.init()
# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Text Input")
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Define font
font = pygame.font.Font(None, 32)
# Define text input areas
teamnum_rect = pygame.Rect(100, 200, 200, 50)
initials_rect = pygame.Rect(100, 300, 200, 50)
# Define variables to store text input
teamnum = ""
initials = ""
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within the teamnum input area
            if teamnum_rect.collidepoint(event.pos):
                # Open text input box for teamnum
                teamnum = input("Enter team number: ")
            # Check if the mouse click is within the initials input area
            elif initials_rect.collidepoint(event.pos):
                # Open text input box for initials
                initials = input("Enter initials: ")
    # Clear the screen
    screen.fill(WHITE)
    # Draw input areas
    pygame.draw.rect(screen, BLACK, teamnum_rect, 2)
    pygame.draw.rect(screen, BLACK, initials_rect, 2)
    # Render text on screen
    text_surface = font.render("Team Number: " + teamnum, True, BLACK)
    screen.blit(text_surface, (100, 170))
    text_surface = font.render("Initials: " + initials, True, BLACK)
    screen.blit(text_surface, (100, 270))
    # Update the display
    pygame.display.flip()
# Quit Pygame
pygame.quit()
sys.exit()