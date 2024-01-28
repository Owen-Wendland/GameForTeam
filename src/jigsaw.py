import math
import pygame
import pymunk
import random
import os
import sys

cwd = os.getcwd()
cwd = str(cwd)
cwd = cwd.replace('src', '')
print(cwd + '\\dat')
sys.path.append(cwd + '\\dat')
import constants

image = pygame.image.load(cwd + "\\testJigsaw.jpg")
imageList = []

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
        def __init__(self, id, rect, color):
            self.id = id
            self.rect = rect
            self.dragging = False
            self.color = color
            self.image_portion = self.get_image_portion()

        def update_position(self, mouse_pos):
            if self.dragging:
                self.rect.x = mouse_pos[0] - self.offset[0]
                self.rect.y = mouse_pos[1] - self.offset[1]
                self.rect.x = max(0, min(self.rect.x, screenSize[0] - self.rect.width))
                self.rect.y = max(0, min(self.rect.y, screenSize[1] - self.rect.height))

        def snap_to_grid(self, grid_size):
            self.rect.x = round(self.rect.x / grid_size) * grid_size
            self.rect.y = round(self.rect.y / grid_size) * grid_size

        def get_image_portion(self):
            x, y, width, height = self.rect.x, self.rect.y, self.rect.width, self.rect.height
            image_portion = pygame.Surface((width, height))
            image_portion.blit(image, (0, 0), (x, y, width, height))
            return image_portion

    def draw_grid(surface, grid_size, color=(100, 100, 100)):
        for x in range(0, screenSize[0], grid_size):
            pygame.draw.line(surface, color, (x, 0), (x, screenSize[1]))
        for y in range(0, screenSize[1], grid_size):
            pygame.draw.line(surface, color, (0, y), (screenSize[0], y))

    # Calculate grid size and number of rows and columns
    grid_size = min(image.get_width() // 9, image.get_height() // 8)
    num_rows = image.get_height() // grid_size
    num_cols = image.get_width() // grid_size

    shapes = []

    for i in range(num_rows):
        for j in range(num_cols):
            rect = pygame.Rect(j * grid_size, i * grid_size, grid_size, grid_size)
            shapes.append(DraggableShape(i * num_cols + j, rect, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

    while RUNNING:
        events = pygame.event.get()
        screen.fill(BACKGROUND)

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
                            shape.snap_to_grid(grid_size)

        mouse_pos = pygame.mouse.get_pos()
        for shape in shapes:
            shape.update_position(mouse_pos)

        draw_grid(screen, grid_size=grid_size)

        for shape in shapes:
            pygame.draw.rect(screen, shape.color, shape.rect)
            screen.blit(shape.image_portion, (shape.rect.x, shape.rect.y))

        pygame.display.update()

        world.step(1 / 120.0)
        clock.tick(120)

    pygame.quit()

if __name__ == "__main__":
    main()
