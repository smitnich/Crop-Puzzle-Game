import pygame
import random
from pygame.locals import *

all_objects = None

class Element:
    x = 0
    y = 0
    id = 0
    sprite = None
    def __init__(self, sprite):
        self.sprite = pygame.image.load(sprite)

    def draw(self):
        screen.blit(self.sprite,(self.x,self.y))

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y


def create_objects():
    global all_objects
    obj1 = Element('gfx/boulder.png')
    obj2 = Element('gfx/fire.png')
    obj3 = Element('gfx/ice.png')
    obj1.x = 50
    obj2.x = 100
    obj3.x = 150
    all_objects = [obj1, obj2, obj3]

def random_object():
    global all_objects
    return random.choice(all_objects)

screen = pygame.display.set_mode((1024, 768))
create_objects()

while True:
    for obj in all_objects:
        obj.draw();
    pygame.display.flip()
