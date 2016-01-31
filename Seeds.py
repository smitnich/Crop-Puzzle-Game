import pygame
from pygame.locals import *
from pygame import font
from TextHandler import get_font
import Globals

font_path = "Base6.ttf"
basic_font = None
seed_count = None
max_count = 9
draw_pos = (432, 236)
## A cache of the numbers upto max_count prerendered:
## this avoids having to regenerate the texture of each number
## when they change
number_sprites = None

selected_seed = -1

def seed_init(count):
    global seed_count
    global number_sprites
    seed_count = [0]*count
    number_sprites = [None]*max_count
    basic_font = get_font()
    for i in range(0, max_count):
        number_sprites[i] = basic_font.render(str(i), False, (0, 0, 0))

def add_seed(index):
    global seed_count
    if seed_count is None:
        return
    if (seed_count[index] < max_count):
        seed_count[index] += 1

def get_selected_seed():
    global selected_seed
    return selected_seed

def can_plant(index):
    global seed_count
    return seed_count[index] > 0

def remove_seed(index):
    global seed_count
    if seed_count is None:
        return
    seed_count[index] -= 1

def draw_seed_interface():
    global selected_seed
    global image_cache
    image_cache = Globals.image_cache
    x = draw_pos[0]
    y = draw_pos[1]
    image_size = Globals.image_size
    for i in range(0, len(seed_count)):
        Globals.screen.blit(image_cache[i],(x,y+i*image_size))
        Globals.screen.blit(number_sprites[seed_count[i]], (x+32, y+i*image_size))
    pos = pygame.mouse.get_pos()
    if (selected_seed != -1):
        Globals.screen.blit(image_cache[selected_seed],pos)


def check_seed_click(pos):
    global selected_seed
    x = pos[0]
    y = pos[1]
    image_size = Globals.image_size
    for i in range(0, len(seed_count)):
        if x >= draw_pos[0] and x <= draw_pos[0] + image_size:
            if y >= draw_pos[1] + i*image_size and y <= draw_pos[1] + (i+1)*image_size:
                if seed_count[i] > 0:
                    selected_seed = i
                    return i
    return -1