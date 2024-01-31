import math
import pygame
import pymunk
import random
import os
import sys


cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src','')
print(cwd + '\\dat')
sys.path.append(cwd + '\\dat')
import constants



def main():
    pygame.init()


    BACKGROUND = (150, 150, 150)
    world = pymunk.Space()
    world.gravity = (0, 1000)
    world.damping = .4


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
            
    percent = text('freesansbold.ttf', '0', screenSize[0]/2, screenSize[1]/9, 128)
            
    def draw_grid(surface, grid_size, color=(100, 100, 100)):
        for x in range(0, screenSize[0], grid_size):
            pygame.draw.line(surface, color, (x, 0), (x, screenSize[1]))
        for y in range(0, screenSize[1], grid_size):
            pygame.draw.line(surface, color, (0, y), (screenSize[0], y))
    
    def check_all_squares_position(shapeList, grid_size):
        amountCorrect = 0
        for shape in shapeList:
            shapeRect = shape.rect
            i = shape.id
            if i >= 48:
                targetRect = (pygame.Rect(((i - 48) * grid_size + (grid_size * 2), grid_size * 4 + (grid_size * 2), grid_size, grid_size)))
            elif i >= 36:
                targetRect = (pygame.Rect(((i - 36) * grid_size + (grid_size * 2), grid_size * 3 + (grid_size * 2), grid_size, grid_size)))
            elif i >= 24:
                targetRect = (pygame.Rect(((i - 24) * grid_size + (grid_size * 2), grid_size * 2 + (grid_size * 2), grid_size, grid_size)))
            elif i >= 12:
                targetRect = (pygame.Rect(((i - 12) * grid_size + (grid_size * 2), grid_size + (grid_size * 2), grid_size, grid_size)))
            elif i >= 0:
                targetRect = (pygame.Rect((i * grid_size + (grid_size * 2), grid_size * 2, grid_size, grid_size)))
           
            if shapeRect == targetRect:
                shape.isCorrect = 1
            else:
                shape.isCorrect = 0
            amountCorrect += shape.isCorrect
        percent.reWrite(str(round((100 * amountCorrect)/60)) + '%')

    grid_size = int(screenSize[0] / 16)  # Adjust this factor as needed
    print(cwd + "\\large.png")
    image = pygame.image.load(cwd + "\\test.jpg")
    image = pygame.transform.scale(image,(grid_size * 12, grid_size * 5))
    image2 = pygame.image.load(cwd + "\\gradient.jpg")
    image2 = pygame.transform.scale(image2,(grid_size * 12, grid_size * 5))
    bimage = pygame.image.load(cwd + "\\background.png")
    bimage = pygame.transform.scale(bimage,(grid_size * 16, grid_size * 9))

    shapes = []
    
    for i in range(60):
        shapes.append(DraggableShape(i,pygame.Rect(50, 50, grid_size, grid_size), grid_size, (random.randint(0,255), random.randint(0,255), random.randint(0,255))))


    while RUNNING:
        events = pygame.event.get()
        screen.fill(BACKGROUND)
        check_all_squares_position(shapes, grid_size)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False
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
        draw_grid(screen, grid_size=grid_size)


        for shape in shapes:
            pygame.draw.rect(screen, shape.color, shape.rect)
        #print(shapes[0].rect.x)
        for shape in shapes:
            try:
                i = shape.id  # Use shape.id directly
                #if i >= 59:
                #    a = image.subsurface(pygame.Rect(((i - 59) * grid_size, grid_size * 5, grid_size, grid_size)))
                if i >= 48:
                    a = image2.subsurface(pygame.Rect(((i - 48) * grid_size, grid_size * 4, grid_size, grid_size)))
                elif i >= 36:
                    a = image2.subsurface(pygame.Rect(((i - 36) * grid_size, grid_size * 3, grid_size, grid_size)))
                elif i >= 24:
                    a = image2.subsurface(pygame.Rect(((i - 24) * grid_size, grid_size * 2, grid_size, grid_size)))
                elif i >= 12:
                    a = image2.subsurface(pygame.Rect(((i - 12) * grid_size, grid_size, grid_size, grid_size)))
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
                if i >= 48:
                    a = image.subsurface(pygame.Rect(((i - 48) * grid_size, grid_size * 4, grid_size, grid_size)))
                elif i >= 36:
                    a = image.subsurface(pygame.Rect(((i - 36) * grid_size, grid_size * 3, grid_size, grid_size)))
                elif i >= 24:
                    a = image.subsurface(pygame.Rect(((i - 24) * grid_size, grid_size * 2, grid_size, grid_size)))
                elif i >= 12:
                    a = image.subsurface(pygame.Rect(((i - 12) * grid_size, grid_size, grid_size, grid_size)))
                elif i >= 0:
                    a = image.subsurface(pygame.Rect((i * grid_size, 0, grid_size, grid_size)))
                screen.blit(a, (shape.rect.x, shape.rect.y))
            except Exception as e:
                print(f"Error blitting image onto shape {shape.id}: {e}")
        percent.draw()
        pygame.display.update()


        world.step(1 / 120.0)
        clock.tick(120)


    pygame.quit()


if __name__ == "__main__":
    main()