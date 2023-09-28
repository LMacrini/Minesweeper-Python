import pygame
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)
from random import *

Grid_x = 8
Grid_y = 8
N_Mines = randint(10, (Grid_x - 1) * (Grid_y - 1))

shuffled_mines = [0] * (Grid_x * Grid_y - N_Mines) + [1] * (N_Mines)
shuffle(shuffled_mines)

field = []
for i in range(Grid_y):
    field.append(shuffled_mines[i * Grid_x : i * Grid_x + Grid_x])

for i in field:
    print(i)

pygame.init()

screen = pygame.display.set_mode([500, 500])


running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    pygame.display.flip()

pygame.quit()
