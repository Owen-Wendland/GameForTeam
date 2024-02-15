import os
import pygame
import pygame_gui
import sys
from pygame_gui.core import ObjectID

pygame.init()

cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
print(cwd + '\\dat')
sys.path.append(cwd + '\\dat')
import constants

WHITE = (255, 255, 255)
BURGANDY = (184, 0, 32)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = constants.screenSize[0], constants.screenSize[1]
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

image = pygame.image.load(cwd + "\\images\\menu1.png")
image = pygame.transform.scale(image,(WIDTH, HEIGHT))

pygame.display.set_caption("Text Input in PyGame")

font = pygame.font.Font(None, WIDTH//16)

manager = pygame_gui.UIManager((constants.screenSize[0], constants.screenSize[1]),cwd + '\\dat\\theme.json')

#creates the textbox, top left is at the first width/height pairing
#then the second width/height pairing is how many pixels it expands from the original point
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH*(1/12), HEIGHT*(37/54)), (WIDTH*(93/320), HEIGHT*(23/125))),
    manager=manager, object_id=('#main_text_entry'))

text_input2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH*(211/480), HEIGHT*(37/54)), (WIDTH*(35/192), HEIGHT*(23/125))),
    manager=manager, object_id=ObjectID(class_id='@text_entry_line',
                                           object_id='#hello_button'))

#text_surface = font.render("Team Number: ", True, BLACK)
#SCREEN.blit(text_surface, (WIDTH//16, HEIGHT//16*1))
#text_surface2 = font.render("Initials: " , True, BLACK)
#SCREEN.blit(text_surface, (WIDTH//16, HEIGHT//16*2))

clock = pygame.time.Clock()

class variables():
    def __init__(self, team, initial):
        self.team = team    
        self.initial = initial

var = variables('','')

def show_user_name():
    if(var.team != '' and var.initial != ''):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

            SCREEN.fill(BURGANDY)

            userNameText = pygame.font.SysFont("bahnschrift", 100).render(f"Team name is: {var.team}", True, "white")
            userNameRect = userNameText.get_rect(center=(WIDTH/2, HEIGHT/2))
            SCREEN.blit(userNameText, userNameRect)

            passWordText = pygame.font.SysFont("bahnschrift", 100).render(f"Your initials are: {var.initial}", True, "white")
            passWordRect = passWordText.get_rect(center=(WIDTH/2, HEIGHT/8*6))
            SCREEN.blit(passWordText, passWordRect)
            
            
            clock.tick(60)

            pygame.display.update()


def get_user_name():
    while True:
        UI_REFRESH_RATE = clock.tick(60)/1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            elif (event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and
                event.ui_object_id == '#main_text_entry'):
                var.team = event.text
                
            elif (event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and
                event.ui_object_id == '#main_text_entry2'):
                var.initial = event.text
                
            elif(event.type == pygame.MOUSEBUTTONDOWN):
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if(int(HEIGHT * (2/3)) < y and y < int(HEIGHT * (7/8))):
                    if(int(WIDTH* (87/128)) < x and x < int(WIDTH * (181/192))):
                        show_user_name()
            
            manager.process_events(event)
        
        manager.update(UI_REFRESH_RATE)
                
        SCREEN.fill("maroon")
        SCREEN.blit(image, (0, 0))
        #SCREEN.blit(text_surface, (WIDTH/8, HEIGHT//16*3))
        #SCREEN.blit(text_surface2, (WIDTH/8, HEIGHT//16*7))
        manager.draw_ui(SCREEN)

        pygame.display.update()
    

get_user_name()