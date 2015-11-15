import pygame
import random
import sys
from pygame.locals import *
from enum import IntEnum

all_objects = None

gameboard_size = 10
image_size = 48

match_length = 3
sprite_paths = ['gfx/boulder.png', 'gfx/fire.png', 'gfx/ice.png']
image_cache = []
Gameboard = [[0 for x in range(gameboard_size)] for x in range(gameboard_size)] 

class Game_State(IntEnum):
    ready = 1
    animation = 2
    update = 3
    last_state = 4

game_state = Game_State.ready
anim_progress = 0.0

class Element:
    index = 0
    moving = False
    sprite = None
    def __init__(self, _index):
        self.index = _index
        self.sprite = image_cache[self.index]

    def draw(self,x,y):
        global anim_progress
        if self.moving:
            screen.blit(self.sprite,(x*image_size, (y-1)*image_size+int(anim_progress)))
        else:
            screen.blit(self.sprite,(x*image_size, y*image_size))

    def update(self):
        global game_state
        if game_state is not Game_State.animation:
            self.moving = False

def move_element(obj, x, y):
    global gameboard_size
    if (x < 0) or (y < 0) or x > (gameboard_size) or (y > gameboard_size):
        return
    if Gameboard[x][y] is not None:
        print(x,y," is not None")
        return
    Gameboard[x][y] = obj
    if obj is not None:
        obj.moving = True

def random_gameboard():
    global gameboard_size
    global Gameboard
    for x in range (0, gameboard_size):
        for y in range (0, gameboard_size):
            obj = random_object()
            Gameboard[x][y] = obj
            obj.x = x*image_size
            obj.y = y*image_size

def drop_column(x, y, count):
    global gameboard_size
    if x < 0 or y < 0 or x > gameboard_size or y > gameboard_size:
        return
    for i in range(0,count):
        delete_object(x,y+i)
    if Gameboard[x][y] is not None:
        return
    for i in range(y-1, -count, -1):
        move_element(Gameboard[x][i],x,i+count)
        delete_object(x,i)
    for i in range(0, count):
        obj = random_object()
        move_element(obj,x,i)
    set_game_state(Game_State.animation)
            
def delete_object(x,y):
    global Gameboard
    global gameboard_size
    if (x > gameboard_size or y > gameboard_size or x < 0 or y < 0):
        return
    Gameboard[x][y] = None

def create_objects():
    global all_objects
    obj1 = Element(0)
    obj2 = Element(1)
    obj3 = Element(2)
    all_objects = [obj1, obj2, obj3]

def check_adjacency(match_length):
    global Gameboard
    global gameboard_size
    match_found = False
    for x in range(0, gameboard_size):
        match_count = 0
        to_match = Gameboard[x][0].index
        for y in range(0, gameboard_size):
            if Gameboard[x][y].index == to_match:
                match_count = match_count+1
            else:
                if match_count >= match_length:
                    match_found = True
                    drop_column(x, y-match_count, match_count)
                match_count = 1
            to_match = Gameboard[x][y].index
        if match_count >= match_length:
            match_found = True
            drop_column(x, gameboard_size-match_count, match_count)
    return match_found
    

def random_object():
    global all_objects
    return Element(random.randrange(0,len(all_objects)))

def cleanup():
    pygame.display.quit()
    sys.exit()

def poll_events():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                cleanup()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x,y = pygame.mouse.get_pos()
                x = int(int(x)/image_size)
                y = int(int(y)/image_size)
                drop_column(x, y, 1)

def load_images():
    global image_cache
    global sprite_paths
    for path in sprite_paths:
        image_cache = image_cache + [pygame.image.load(path)]

def do_animations():
    global anim_progress
    anim_progress += 1
    if anim_progress >= image_size:
        anim_progress = 0.0
        set_game_state(Game_State.update)

def game_loop():
    global game_state
    global match_length
    if game_state == Game_State.ready:
        poll_events()
    elif game_state == Game_State.animation:
        do_animations()
    elif game_state == Game_State.update:
        if not check_adjacency(match_length):
            set_game_state(Game_State.ready)

def set_game_state(new_state):
    global game_state
    if new_state < 0 or new_state >= Game_State.last_state:
        return
    game_state = new_state

def main():
    global screen
    screen = pygame.display.set_mode((1024, 768))
    load_images()
    create_objects()
    random_gameboard()
    while True:
        screen.fill((0,0,0))
        game_loop()
        for x in range(0,gameboard_size):
            for y in range(0, gameboard_size):
                obj = Gameboard[x][y]
                if (obj is not None):
                    obj.update()
                    obj.draw(x, y)
        pygame.display.flip()

main()
