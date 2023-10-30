import pygame
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)
from random import *

# class Tile(pygame.sprite.Sprite):
#     def __init__(self, mine):
#         self.mine = mine
#         self.image = pygame.Surface((8,8))
#         self.image.fill(WHITE)
#         if mine:
#             self.image

grid_x = 16
grid_y = 16
n_mines = randint(10, (grid_x - 3) * (grid_y - 3))

shuffled_mines = [0] * (grid_x * grid_y - n_mines) + [1] * (n_mines)
shuffle(shuffled_mines)

field = []
for i in range(grid_y):
    field.append(shuffled_mines[i * grid_x : i * grid_x + grid_x])


field =[[1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0],[1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0],[1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0],[0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],[0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1],[0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],[1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0],[0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0],[0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1],[0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0],[1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1],[1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],[1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0],[1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0],[1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1],[0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1]]

for y, column in enumerate(field):
    for x, tile in enumerate(column):
        mines_around = 0
        if x > 0:
            if y > 0:
                mines_around += field[y - 1][x - 1]
            if y < grid_y - 1:
                mines_around += field[y + 1][x - 1]
            mines_around += field[y][x - 1]
        if x < grid_x - 1:
            if y > 0:
                mines_around += field[y - 1][x + 1]
            if y < grid_y - 1:
                mines_around += field[y + 1][x + 1]
            mines_around += field[y][x - 1]
        if y > 0:
            mines_around += field[y - 1][x]
        if y < grid_x - 1:
            mines_around += field[y + 1][x]
        if mines_around == 9:
            field[x][y] = 0
print("\n")
for i in field:
    print(i)

pygame.init()

screen = pygame.display.set_mode([512, 512])

numbers = [pygame.image.load("ressources/"+str(i)+"_tile.png").convert() for i in range(10)]
mine_tile = pygame.image.load("ressources/Mine_Bomb.png").convert()
flag_tile = pygame.image.load("ressources/flag_tile.png").convert()
tile_image = pygame.image.load("ressources/tile.png").convert()
anger = pygame.transform.scale(pygame.image.load("ressources/Angry_Face.png").convert(), (48, 48))
happy = pygame.transform.scale(pygame.image.load("ressources/Happy_Face.png").convert(), (48, 48))

def on_click():
    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
    

screen.fill((255, 255, 255))

for y, column in enumerate(field):
    for x, tile in enumerate(column):
        screen.blit(tile_image, (32*x, 32*y))
        if tile == 1:
            screen.blit(mine_tile, (32*x+4, 32*y+4))

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    

    # for y, column in enumerate(field):
    #     for x, tile in enumerate(column):
    #         screen.blit(back_tile, (4*x*i, 4*y*i))
    #         if tile == 1:
    #             screen.blit(inners[0], (4*x*i+4, 4*x*i+4))

    pygame.display.flip()

pygame.quit()
