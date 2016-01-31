import pygame
from pygame.locals import *
from pygame import font
from TextHandler import get_font
import Globals

font_path = "Base6.ttf"
basic_font = None
seed_count = None
max_count = 9
## A cache of the numbers upto max_count prerendered:
## this avoids having to regenerate the texture of each number
## when they change
number_sprites = None

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

def can_plant(index):
    global seed_count
    return seed_count[index] > 0

def remove_seed(index):
    global seed_count
    if seed_count is None:
        return
    seed_count[index] -= 1

def draw_seed_count(pos):
    image_cache = Globals.image_cache
    x = pos[0]
    y = pos[1]
    image_size = Globals.image_size
    for i in range(0, len(seed_count)):
        Globals.screen.blit(image_cache[i],(x,y+i*image_size))
        Globals.screen.blit(number_sprites[seed_count[i]], (x+32, y+i*image_size))
