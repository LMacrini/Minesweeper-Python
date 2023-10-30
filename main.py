#Importing Libraries
import pygame
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)
from random import *

pygame.init()

grid_x = 40
grid_y = 20
n_mines_ez = int(grid_x*grid_y / 10)
n_mines = int(grid_x*grid_y / 6)
n_mines_hard = int(grid_x*grid_y / 5)

screen = pygame.display.set_mode([grid_x*32, grid_y*32])

numbers = [pygame.image.load("ressources/"+str(i)+"_tile.png").convert() for i in range(10)]
mine_tile = pygame.image.load("ressources/mine_tile.png").convert()
flag_tile = pygame.image.load("ressources/flag_tile.png").convert()
tile_image = pygame.image.load("ressources/tile.png").convert()
anger = pygame.transform.scale(pygame.image.load("ressources/Angry_Face.png").convert(), (48, 48))
happy = pygame.transform.scale(pygame.image.load("ressources/Happy_Face.png").convert(), (48, 48))

class Tile(pygame.sprite.Sprite):
    def __init__(self, mine):
        self.mine = mine
        self.mines_around = 0
        self.clicked = 0

shuffled_mines = []
for _ in range(grid_x * grid_y - n_mines):
    shuffled_mines.append(Tile(0))
for _ in range(n_mines):
    shuffled_mines.append(Tile(1))
shuffle(shuffled_mines)


field = []
for i in range(grid_y):
    field.append(shuffled_mines[i * grid_x : i * grid_x + grid_x])

for y, column in enumerate(field):
    for x, tile in enumerate(column):
        mines_around = 0
        
        if x > 0:
            if y > 0:
                mines_around += field[y - 1][x - 1].mine
            if y < grid_y - 1:
                mines_around += field[y + 1][x - 1].mine
            mines_around += field[y][x - 1].mine
            
        if x < grid_x - 1:
            if y > 0:
                mines_around += field[y - 1][x + 1].mine
            if y < grid_y - 1:
                mines_around += field[y + 1][x + 1].mine
            mines_around += field[y][x + 1].mine
        
        if y > 0:
            mines_around += field[y - 1][x].mine
        
        if y < grid_y - 1:
            mines_around += field[y + 1][x].mine
        
        if mines_around == 8:
            field[y][x].mine = 0
        
        if field[y][x].mine == 0:
            field[y][x].mines_around = mines_around
            print(mines_around, field[y][x].mines_around)
        
        if field[y][x].mine:
            field[y][x].image = mine_tile
        else:
            field[y][x].image = numbers[mines_around]

# def on_click():
#     if pygame.mouse.get_pressed()[0]:
#         mouse_x, mouse_y = pygame.mouse.get_pos()
#         mouse_x = int(mouse_x / 32)
#         mouse_y = int(mouse_y / 32)
#         field[mouse_y][mouse_x].clicked = 1
    

screen.fill((255, 255, 255))

for y, column in enumerate(field):
    for x, tile in enumerate(column):
        if tile.clicked == 0:
            screen.blit(tile_image, (32*x, 32*y))
        else:
            screen.blit(tile.texture (32*x, 32*y))
            # print(tile.mines_around)
        # if tile == 1:
        #     screen.blit(mine_tile, (32*x, 32*y))
        # else:
        #     screen.blit(tile_image, (32*x, 32*y))

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        if pygame.mouse.get_pressed()[0] == 1 != previous_mouse_state:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x = int(mouse_x / 32)
            mouse_y = int(mouse_y / 32)
            field[mouse_y][mouse_x].clicked = 1
        
        previous_mouse_state = pygame.mouse.get_pressed()[0]

        for y, column in enumerate(field):
            for x, tile in enumerate(column):
                if tile.clicked == 1:
                    screen.blit(tile_image, (32*x, 32*y))
                else:
                    screen.blit(tile.image, (32*x, 32*y))

    pygame.display.flip()

pygame.quit()
