import os
import subprocess
import pygame
import pygame_gui
import sys
import pickle 
from pygame_gui.core import ObjectID
from tkinter import *


pygame.init()

cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
print(cwd + '\\dat')
sys.path.append(cwd + '\\dat')
import constants

#root = Tk()
#root.title("start")
WHITE = (255, 255, 255)
BURGANDY = (184, 0, 32)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = constants.screenSize[0], constants.screenSize[1]
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# Read the Image
#background_image = Image.open(cwd + "\\images\\menu1.png")

# Resize the image using resize() method
#background_image = background_image.resize((WIDTH, HEIGHT))

#background_image = ImageTk.PhotoImage(master=root,image=background_image)

image = pygame.image.load(cwd + "\\images\\menu1.png")
image = pygame.transform.scale(image,(WIDTH, HEIGHT))

pygame.display.set_caption("Text Input in PyGame")

font = pygame.font.Font(None, WIDTH//16)

manager = pygame_gui.UIManager((constants.screenSize[0], constants.screenSize[1]), (cwd + '\\src\\theme.json'))

#creates the textbox, top left is at the first width/height pairing
#then the second width/height pairing is how many pixels it expands from the original point
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH*(1/12), HEIGHT*(37/54)), (WIDTH*(93/320), HEIGHT*(23/125))),
    manager=manager, object_id=ObjectID('#main_text_entry'))

text_input2 = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((WIDTH*(211/480), HEIGHT*(37/54)), (WIDTH*(35/192), HEIGHT*(23/125))),
    manager=manager, object_id=ObjectID('#main_text_entry2'))

text_input.set_text_length_limit(4)
text_input2.set_text_length_limit(3)
clock = pygame.time.Clock()

class variables():
    def __init__(self, team, initial):
        self.team = team    
        self.initial = initial
        self.activated = False
        self.first = True

var = variables('','')

def show_user_name():
    if(var.team != '' and var.initial != ''):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

        SCREEN.fill(BURGANDY)
        #image = pygame.image.load(cwd + "\\images\\menu10.png")
        #image = pygame.transform.scale(image,(WIDTH, HEIGHT))
        SCREEN.blit(image, (0, 0))
        
        clock.tick(60)
        pygame.display.update()
        subprocess.run(["python", cwd + "\\src\\menu.py"])
        pygame.quit()
        sys.exit
    else:
        var.activated = False


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
                if(len(event.text) <= 4):
                    var.team = event.text
                else:
                    var.team = ''
                
            elif (event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and
                event.ui_object_id == '#main_text_entry2'):
                if(len(event.text) <= 3):
                    var.initial = event.text
                else:
                    var.initial = ''
                
            elif(event.type == pygame.MOUSEBUTTONDOWN):
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if(int(HEIGHT * (2/3)) < y and y < int(HEIGHT * (7/8))):
                    if(int(WIDTH* (87/128)) < x and x < int(WIDTH * (181/192))):
                        var.activated = True
            
            manager.process_events(event)
        
        manager.update(UI_REFRESH_RATE)
        if(not(var.activated)):
            SCREEN.fill("maroon")
            SCREEN.blit(image, (0, 0))
            #SCREEN.blit(text_surface, (WIDTH/8, HEIGHT//16*3))
            #SCREEN.blit(text_surface2, (WIDTH/8, HEIGHT//16*7))
            manager.draw_ui(SCREEN)

            pygame.display.update()
        else:
            show_user_name()
    

get_user_name()