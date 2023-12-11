# Importing Libraries
import pygame
from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
)
from random import *

grid_x = 40
grid_y = 20
# n_mines_ez = int(grid_x * grid_y / 10)
n_mines = int(grid_x * grid_y / 6)
# n_mines_hard = int(grid_x * grid_y / 5)
n_flags = 0
n_unclicked_tiles = grid_x * grid_y

pygame.init()
screen = pygame.display.set_mode([grid_x * 32, (grid_y + 3) * 32])
screen.fill((59, 76, 98))

numbers = [
    pygame.image.load("resources/" + str(i) + "_tile.png").convert() for i in range(10)
]
digits = [
    pygame.image.load("resources/" + str(i) + "_digit.png").convert() for i in range(11)
]
mine_tile = pygame.image.load("resources/mine_tile.png").convert()
mine_clicked = pygame.image.load("resources/mine_clicked.png").convert()
flag_tile = pygame.image.load("resources/flag_tile.png").convert()
tile_image = pygame.image.load("resources/tile.png").convert()
anger = pygame.transform.scale(
    pygame.image.load("resources/Angry_Face.png").convert(), (48, 48)
)
happy = pygame.transform.scale(
    pygame.image.load("resources/Happy_Face.png").convert(), (48, 48)
)
cool = pygame.transform.scale(
    pygame.image.load("resources/Cool_Face.png").convert(), (48, 48)
)


class Tile(pygame.sprite.Sprite):
    def __init__(self, mine):
        self.mine = mine
        self.mines_around = 0
        self.clicked = 0


running = True
game_state = 1


def generate_field():
    global n_mines
    shuffled_mines = []
    field = []

    for _ in range(grid_x * grid_y - n_mines):
        shuffled_mines.append(Tile(0))
    for _ in range(n_mines):
        shuffled_mines.append(Tile(1))
    shuffle(shuffled_mines)

    for i in range(grid_y):
        field.append(shuffled_mines[i * grid_x : i * grid_x + grid_x])

    for y, column in enumerate(field):
        for x, _ in enumerate(column):
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
                n_mines -= 1

            if field[y][x].mine == 0:
                field[y][x].mines_around = mines_around

            if field[y][x].mine:
                field[y][x].image = mine_tile
            else:
                field[y][x].image = numbers[mines_around]
    return field


field = generate_field()
print(n_mines)


def reveal_tile(x, y):
    global n_unclicked_tiles
    field[y][x].clicked = 1
    n_unclicked_tiles -= 1
    if field[y][x].mines_around != 0:
        return

    if x > 0:
        if field[y][x - 1].mine == 0 and field[y][x - 1].clicked == 0:
            reveal_tile(x - 1, y)
        if y > 0:
            if field[y - 1][x - 1].mine == 0 and field[y - 1][x - 1].clicked == 0:
                reveal_tile(x - 1, y - 1)
        if y < grid_y - 1:
            if field[y + 1][x - 1].mine == 0 and field[y + 1][x - 1].clicked == 0:
                reveal_tile(x - 1, y + 1)

    if x < grid_x - 1:
        if field[y][x + 1].mine == 0 and field[y][x + 1].clicked == 0:
            reveal_tile(x + 1, y)
        if y > 0:
            if field[y - 1][x + 1].mine == 0 and field[y - 1][x + 1].clicked == 0:
                reveal_tile(x + 1, y - 1)
        if y < grid_y - 1:
            if field[y + 1][x + 1].mine == 0 and field[y + 1][x + 1].clicked == 0:
                reveal_tile(x + 1, y + 1)

    if y > 0:
        if field[y - 1][x].mine == 0 and field[y - 1][x].clicked == 0:
            reveal_tile(x, y - 1)
    if y < grid_y - 1:
        if field[y + 1][x].mine == 0 and field[y + 1][x].clicked == 0:
            reveal_tile(x, y + 1)


while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        if pygame.mouse.get_pressed()[0] == 1 != previous_mouse_state[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > grid_x * 32 or mouse_y > grid_y * 32:
                if not (
                    mouse_x < grid_x * 16 - 24
                    or mouse_x > grid_x * 16 + 24
                    or mouse_y < (grid_y + 1) * 32
                    or mouse_y > grid_y * 32 + 80
                ):
                    field = generate_field()
                    game_state = 1
                    n_flags = 0
                break
            if game_state != 1:
                break
            mouse_x = int(mouse_x / 32)
            mouse_y = int(mouse_y / 32)
            if field[mouse_y][mouse_x].clicked != 2:
                if field[mouse_y][mouse_x].mine == 0:
                    reveal_tile(mouse_x, mouse_y)
                else:
                    field[mouse_y][mouse_x].clicked = 1
                    game_state = 0

        if pygame.mouse.get_pressed()[2] == 1 != previous_mouse_state[1]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > grid_x * 32 or mouse_y > grid_y * 32 or game_state != 1:
                break
            mouse_x = int(mouse_x / 32)
            mouse_y = int(mouse_y / 32)
            if field[mouse_y][mouse_x].clicked != 1:
                if field[mouse_y][mouse_x].clicked != 2:
                    field[mouse_y][mouse_x].clicked = 2
                    n_flags += 1
                else:
                    field[mouse_y][mouse_x].clicked = 0
                    n_flags -= 1

        previous_mouse_state = [
            pygame.mouse.get_pressed()[0],
            pygame.mouse.get_pressed()[2],
        ]

        for y, column in enumerate(field):
            for x, tile in enumerate(column):
                if tile.clicked == 1 and tile.mine == 0:
                    screen.blit(tile.image, (32 * x, 32 * y))
                elif tile.clicked == 2:
                    screen.blit(flag_tile, (32 * x, 32 * y))
                elif game_state == 0 and tile.mine == 1:
                    if tile.clicked == 1:
                        screen.blit(mine_clicked, (32 * x, 32 * y))
                    else:
                        screen.blit(mine_tile, (32 * x, 32 * y))
                else:
                    screen.blit(tile_image, (32 * x, 32 * y))

        screen.blit(happy, (grid_x * 16 - 24, (grid_y + 1) * 32))

        if n_unclicked_tiles == n_mines and n_flags == n_mines:
            game_state = 2

        if game_state == 0:
            screen.blit(anger, (grid_x * 16 - 24, (grid_y + 1) * 32))
        elif game_state == 2:
            screen.blit(cool, (grid_x * 16 - 24, (grid_y + 1) * 32))

        if n_flags <= n_mines:
            number_str = str(n_mines - n_flags).zfill(3)
            x_mines = 96 - len(number_str) * 16
            for digit_char in number_str:
                digit_index = int(digit_char)
                screen.blit(digits[digit_index], (x_mines, ((grid_y + 1) * 32) - 16))
                x_mines += 32
        else:
            screen.blit(digits[10], ((x_mines - 32), ((grid_y + 1) * 32) - 16))
            screen.blit(digits[10], ((x_mines - 32 * 2), ((grid_y + 1) * 32) - 16))
            screen.blit(digits[10], ((x_mines - 32 * 3), ((grid_y + 1) * 32) - 16))

    pygame.display.flip()

pygame.quit()
