import math
import subprocess
import pygame
import pymunk
import random
import os
import sys
import pickle
import time as t


cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
print(cwd + '\\dat')
sys.path.append(cwd + '\\dat')
import constants


def main():
    pygame.init()
    pygame.time.Clock
    
    BACKGROUND = (150, 150, 150)
    world = pymunk.Space()
    world.gravity = (0, 1000)
    world.damping = .4

    lasttime = True
    screenSize = constants.screenSize
    print(screenSize)


    global RUNNING
    RUNNING = True


    screen = pygame.display.set_mode((screenSize[0] * 2, screenSize[1] * 2))
    clock = pygame.time.Clock()
    pygame.display.set_mode(screenSize, pygame.FULLSCREEN)


    class DraggableShape:
        def __init__(self, id, rect, grid_size, color):
            self.id = id
            self.isCorrect = 0
            self.rect = rect
            self.dragging = False
            self.grid_size = grid_size
            self.color = color
            self.connectedTop = False
            self.connectedBottom = False
            self.connectedLeft = False
            self.connectedRight = False

        def update_position(self, mouse_pos):
            if self.dragging:
                self.rect.x = mouse_pos[0] - self.offset[0]
                self.rect.y = mouse_pos[1] - self.offset[1]
                self.rect.x = max(0, min(self.rect.x, screenSize[0] - self.rect.width))
                self.rect.y = max(0, min(self.rect.y, screenSize[1] - self.rect.height))
            


        def check_collision(self, other_shapes):
            for shape in other_shapes:
                if shape != self and self.rect.colliderect(shape.rect):
                    return True
            return False


        def find_closest_non_occupied_square(self, other_shapes):
            orig_x, orig_y = self.rect.x, self.rect.y
            min_distance = float('inf')
            closest_x, closest_y = orig_x, orig_y


            for x in range(0, screenSize[0], self.grid_size):
                for y in range(0, screenSize[1], self.grid_size):
                    self.rect.x, self.rect.y = x, y
                    if not self.check_collision(other_shapes):
                        distance = math.sqrt((orig_x - x)**2 + (orig_y - y)**2)
                        if distance < min_distance:
                            min_distance = distance
                            closest_x, closest_y = x, y


            self.rect.x, self.rect.y = orig_x, orig_y
            return closest_x, closest_y
            #return closest_x, closest_y


        def snap_to_grid(self, other_shapes):
            if self.check_collision(other_shapes):
                closest_x, closest_y = self.find_closest_non_occupied_square(other_shapes)
                self.rect.x, self.rect.y = closest_x, closest_y
            else:
                self.rect.x = round(self.rect.x / self.grid_size) * self.grid_size
                self.rect.y = round(self.rect.y / self.grid_size) * self.grid_size

    class text():
        def __init__(self, textFont, textWritten, x, y, size):
            self.x = x
            self.y = y
            self.color = (255,255,255)
            self.font = pygame.font.Font(textFont, size)
            self.textWritten = textWritten
            self.text = self.font.render(self.textWritten, True, self.color)
            self.currPercent = 0
            
            self.location = self.text.get_rect(center = (self.x, self.y))
            
        def reWrite(self, textWritten):
            self.textWritten = textWritten
            self.text = self.font.render(self.textWritten, True, self.color)
            self.location = self.text.get_rect(center = (self.x, self.y))
            
        def draw(self):
            screen.blit(self.text, self.location)
            
    percent = text('freesansbold.ttf', '0', screenSize[0]/2, screenSize[1]/9, screenSize[0]//16)
            
    '''def draw_grid(surface, grid_size, color=(100, 100, 100)):
        for x in range(0, screenSize[0], grid_size):
            pygame.draw.line(surface, color, (x, 0), (x, screenSize[1]))
        for y in range(0, screenSize[1], grid_size):
            pygame.draw.line(surface, color, (0, y), (screenSize[0], y))'''
    
    def check_all_squares_position(shapeList, grid_size,solve):
        amountCorrect = 0
        for shape in shapeList:
            shapeRect = shape.rect
            i = shape.id
            if i >= (gridSize2*4):
                targetRect = (pygame.Rect(((i - (gridSize2*4)) * grid_size + (grid_size * 2), grid_size * 4 + (grid_size * 1), grid_size, grid_size)))
            elif i >= (gridSize2*3):
                targetRect = (pygame.Rect(((i - (gridSize2*3)) * grid_size + (grid_size * 2), grid_size * 3 + (grid_size * 1), grid_size, grid_size)))
            elif i >= (gridSize2*2):
                targetRect = (pygame.Rect(((i - (gridSize2*2)) * grid_size + (grid_size * 2), grid_size * 2 + (grid_size * 1), grid_size, grid_size)))
            elif i >= gridSize2:
                targetRect = (pygame.Rect(((i - (gridSize2*1)) * grid_size + (grid_size * 2), grid_size * 1 + (grid_size * 1), grid_size, grid_size)))
            elif i >= 0:
                targetRect = (pygame.Rect(((i - (gridSize2*0)) * grid_size + (grid_size * 2), grid_size * 0 + (grid_size * 1), grid_size, grid_size)))
            if(solve):
                shape.rect = targetRect
            #if the shape is in the correct position 
            if shapeRect == targetRect:
                shape.isCorrect = 1
            else:
                shape.isCorrect = 0
            amountCorrect += shape.isCorrect
        return(round((100 * amountCorrect)/(gridSize2*gridSize1)))
    
    
    '''def checkSquareConnected():
        for shape in shapes:
            for i in range(5):
                try:
                    if i == 1 and shape.id < 12:
                        targetId = shape.id - 12
                        targetRect = (shape.rect.x, shape.rect.y - grid_size)
                        shapeRect = (shapes[targetId].rect.x, shapes[targetId].rect.y)
                        if targetRect == shapeRect:
                            shape.connectedTop = True
                            #print(shapes[targetId].rect)
                            
                    if i == 2 and shape.id < 36:
                        targetId = shape.id + 12
                        targetRect = (shape.rect.x, shape.rect.y + grid_size)
                        shapeRect = (shapes[targetId].rect.x, shapes[targetId].rect.y)
                        if targetRect == shapeRect:
                            shape.connectedBottom = True
                            #print(shapes[targetId].rect)
                        
                    if i == 3 and shape.id % 12 != 0:
                        targetId = shape.id - 1
                        targetRect = (shape.rect.x - grid_size, shape.rect.y)
                        shapeRect = (shapes[targetId].rect.x, shapes[targetId].rect.y)
                        if targetRect == shapeRect:
                            shape.connectedLeft = True
                            #print(shapes[targetId].rect)
                            print('left')
                        
                    if i == 4 and (shape.id + 1) % 12 != 0:
                        targetId = shape.id + 1
                        targetRect = (shape.rect.x + grid_size, shape.rect.y)
                        shapeRect = (shapes[targetId].rect.x, shapes[targetId].rect.y)
                        if targetRect == shapeRect:
                            shape.connectedRight = True
                            #print(shapes[targetId].rect)
                except:
                    print(targetId)'''

    grid_size = int(screenSize[0] / 8.8888888888888888)  # Adjust this factor as needed
    gridSize2 = 5
    gridSize1 = 3
    print(cwd + "\\images\\large.png")
    print(os.listdir(cwd + "\\images"))
    image = pygame.image.load(cwd + "\\images\\large.png")
    image = pygame.transform.scale(image,(grid_size * gridSize2, grid_size * gridSize1))
    image2 = pygame.image.load(cwd + "\\images\\naturegradient.png")
    image2 = pygame.transform.scale(image2,(screenSize[0], screenSize[1]))
    bimage = pygame.image.load(cwd + "\\images\\background3.png")
    bimage = pygame.transform.scale(bimage,(screenSize[0], screenSize[1]))
    oimage = pygame.image.load(cwd + "\\images\\large.png")
    oimage = pygame.transform.scale(oimage,(grid_size * 4, grid_size * 2))
    obimage = pygame.image.load(cwd + "\\images\\naturegradient.png")
    obimage = pygame.transform.scale(obimage,(grid_size * 4, grid_size * 2))

    shapes = []
    
    for i in range(gridSize2 * gridSize1):
        shapes.append(DraggableShape(i,pygame.Rect(50, 50, grid_size, grid_size), grid_size, (random.randint(0,255), random.randint(0,255), random.randint(0,255))))

    solve = False
    
    while RUNNING:
        #checkSquareConnected()
        events = pygame.event.get()
        screen.fill(BACKGROUND)
        percentCompleted = check_all_squares_position(shapes, grid_size, solve)
        time = pygame.time.get_ticks()//1000
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False
                if event.key == pygame.K_p:
                    solve = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for shape in shapes:
                        if shape.rect.collidepoint(event.pos):
                            shape.dragging = True
                            shape.offset = (event.pos[0] - shape.rect.x, event.pos[1] - shape.rect.y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for shape in shapes:
                        if shape.dragging:
                            shape.dragging = False
                            shape.snap_to_grid(shapes)


        mouse_pos = pygame.mouse.get_pos()
        for shape in shapes:
            shape.update_position(mouse_pos)

        screen.blit(bimage, (0, 0))
        screen.blit(obimage, (0, grid_size * 7))
        screen.blit(oimage, (0,grid_size * 7))
        #draw_grid(screen, grid_size=grid_size)


       # for shape in shapes:
        #    pygame.draw.rect(screen, shape.color, shape.rect)
            
        for shape in shapes:
            try:
                i = shape.id  # Use shape.id directly
                #if i >= 59:
                #    a = image.subsurface(pygame.Rect(((i - 50) * grid_size, grid_size * 5, grid_size, grid_size)))
                if i >= (gridSize2*4):
                    a = image2.subsurface(pygame.Rect(((i - (gridSize2*4)) * grid_size, grid_size * 4, grid_size, grid_size)))
                elif i >= (gridSize2*3):
                    a = image2.subsurface(pygame.Rect(((i - (gridSize2*3)) * grid_size, grid_size * 3, grid_size, grid_size)))
                elif i >= (gridSize2*2):
                    a = image2.subsurface(pygame.Rect(((i - (gridSize2*2)) * grid_size, grid_size * 2, grid_size, grid_size)))
                elif i >= (gridSize2*1):
                    a = image2.subsurface(pygame.Rect(((i - (gridSize2*1)) * grid_size, grid_size * 1, grid_size, grid_size)))
                elif i >= 0:
                    a = image2.subsurface(pygame.Rect(((i - (gridSize2*0)) * grid_size, grid_size * 0, grid_size, grid_size)))
                screen.blit(a, (shape.rect.x, shape.rect.y))
            except Exception as e:
                print(f"Error blitting image onto shape {shape.id}: {e}")
        
        for shape in shapes:
            try:
                i = shape.id  # Use shape.id directly
                #if i >= 59:
                #    a = image.subsurface(pygame.Rect(((i - 59) * grid_size, grid_size * 5, grid_size, grid_size)))
                if i >= (gridSize2*4):
                    a = image.subsurface(pygame.Rect(((i - (gridSize2*4)) * grid_size, grid_size * 4, grid_size, grid_size)))
                elif i >= (gridSize2*3):
                    a = image.subsurface(pygame.Rect(((i - (gridSize2*3)) * grid_size, grid_size * 3, grid_size, grid_size)))
                elif i >= (gridSize2*2):
                    a = image.subsurface(pygame.Rect(((i - (gridSize2*2)) * grid_size, grid_size * 2, grid_size, grid_size)))
                elif i >= gridSize2:
                    a = image.subsurface(pygame.Rect(((i - gridSize2) * grid_size, grid_size, grid_size, grid_size)))
                elif i >= 0:
                    a = image.subsurface(pygame.Rect((i * grid_size, 0, grid_size, grid_size)))
                screen.blit(a, (shape.rect.x, shape.rect.y))
            except Exception as e:
                print(f"Error blitting image onto shape {shape.id}: {e}")
        #checkSquareConnected()
        percent.draw()
        if(percentCompleted == 100 and lasttime):
            percent.font = pygame.font.Font('freesansbold.ttf', screenSize[0]//18)
            percent.reWrite(f'YOU WON AFTER {time} SECONDS!')
            print(f'YOU WON AFTER {time} SECONDS!')
            with open(cwd + "\\dat\\currentPerson.pkl", 'rb') as f:
                x = pickle.load(f)
            score = (1+ 1.05 **(-time+50))
            x['points'] = x['points'] + round(score*260)
            print(x['points'])
            with open(cwd + "\\dat\\currentPerson.pkl", "wb") as f:
                f.truncate(0)
                pickle.dump(x, f)
            with open(cwd + "\\dat\\currentPerson.pkl", 'rb') as f:
                x = pickle.load(f)
            print(x)
            
            screen.blit(bimage, (0, 0))
            screen.blit(obimage, (0, grid_size * 7))
            screen.blit(oimage, (0,grid_size * 7))
            #draw_grid(screen, grid_size=grid_size)


        # for shape in shapes:
            #    pygame.draw.rect(screen, shape.color, shape.rect)
                
            for shape in shapes:
                try:
                    i = shape.id  # Use shape.id directly
                    #if i >= 59:
                    #    a = image.subsurface(pygame.Rect(((i - 50) * grid_size, grid_size * 5, grid_size, grid_size)))
                    if i >= (gridSize2*4):
                        a = image2.subsurface(pygame.Rect(((i - (gridSize2*4)) * grid_size, grid_size * 4, grid_size, grid_size)))
                    elif i >= (gridSize2*3):
                        a = image2.subsurface(pygame.Rect(((i - (gridSize2*3)) * grid_size, grid_size * 3, grid_size, grid_size)))
                    elif i >= (gridSize2*2):
                        a = image2.subsurface(pygame.Rect(((i - (gridSize2*2)) * grid_size, grid_size * 2, grid_size, grid_size)))
                    elif i >= gridSize2:
                        a = image2.subsurface(pygame.Rect(((i - gridSize2) * grid_size, grid_size, grid_size, grid_size)))
                    elif i >= 0:
                        a = image2.subsurface(pygame.Rect((i * grid_size, 0, grid_size, grid_size)))
                    screen.blit(a, (shape.rect.x, shape.rect.y))
                except Exception as e:
                    print(f"Error blitting image onto shape {shape.id}: {e}")
            
            for shape in shapes:
                try:
                    i = shape.id  # Use shape.id directly
                    #if i >= 59:
                    #    a = image.subsurface(pygame.Rect(((i - 59) * grid_size, grid_size * 5, grid_size, grid_size)))
                    if i >= (gridSize2*4):
                        a = image.subsurface(pygame.Rect(((i - (gridSize2*4)) * grid_size, grid_size * 4, grid_size, grid_size)))
                    elif i >= (gridSize2*3):
                        a = image.subsurface(pygame.Rect(((i - (gridSize2*3)) * grid_size, grid_size * 3, grid_size, grid_size)))
                    elif i >= (gridSize2*2):
                        a = image.subsurface(pygame.Rect(((i - (gridSize2*2)) * grid_size, grid_size * 2, grid_size, grid_size)))
                    elif i >= gridSize2:
                        a = image.subsurface(pygame.Rect(((i - gridSize2) * grid_size, grid_size, grid_size, grid_size)))
                    elif i >= 0:
                        a = image.subsurface(pygame.Rect((i * grid_size, 0, grid_size, grid_size)))
                    screen.blit(a, (shape.rect.x, shape.rect.y))
                except Exception as e:
                    print(f"Error blitting image onto shape {shape.id}: {e}")
                    
            percent.font = pygame.font.Font('freesansbold.ttf', screenSize[0]//18)
            percent.reWrite(f'YOU WON AFTER {time} SECONDS!')
            percent.draw()
            pygame.display.update()
            clock.tick(120)
            t.sleep(5)
            lasttime = False

            RUNNING = False
            
        elif(lasttime):
            percent.reWrite((str(percentCompleted)+'% correct, '+ str(time) + ' secs'))
        pygame.display.update()

        '''for shape in shapes:
            try:
                if(shape.connectedTop):
                        targetId = shape.id - 12
                        shapes[targetId].rect.x = shape.rect.x
                        shapes[targetId].rect.y = shape.rect.y - grid_size
                if(shape.connectedBottom):
                        targetId = shape.id + 12
                        shapes[targetId].rect.x = shape.rect.x
                        shapes[targetId].rect.y = shape.rect.y + grid_size
                if(shape.connectedLeft):
                        targetId = shape.id - 1
                        shapes[targetId].rect.x = shape.rect.x - grid_size
                        shapes[targetId].rect.y = shape.rect.y 
                if(shape.connectedRight):
                        targetId = shape.id + 1
                        shapes[targetId].rect.x = shape.rect.x + grid_size
                        shapes[targetId].rect.y = shape.rect.y 
            except:
                print(targetId)'''
        world.step(1 / 120.0)
        clock.tick(120)
    
    percent.font = pygame.font.Font('freesansbold.ttf', screenSize[0]//18)
    percent.reWrite(f'YOU WON AFTER {time} SECONDS!')
    subprocess.run(["python", cwd + "\\src\\sort10.py"])
    pygame.quit()


if __name__ == "__main__":
    main()
