import pygame
import random
import sys
from pygame.locals import *
from enum import IntEnum
import gameboard
all_objects = None

image_size = 48

margin = (64, 64)
match_length = 3
sprite_paths = ['gfx/fire.png', 'gfx/ice.png', 'gfx/boulder.png', 'gfx/robot.png']
image_cache = []
selected_element = [-1, -1]
background = None

do_quit = False

class Game_State(IntEnum):
    ready = 1
    animation = 2
    update = 3
    last_state = 4

cursor_pos = [0, 0]

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
        global margin
        if self.moving:
            x = x*image_size+margin[0]
            y = (y-1)*image_size+int(anim_progress)+margin[1]
        else:
            x = x*image_size+margin[0]
            y = y*image_size+margin[1]
        screen.blit(self.sprite,(x,y))

    def draw_true(self, x, y):
        global image_size
        global margin
        screen.blit(self.sprite, (x-image_size/2, y-image_size/2))
    
    def update(self):
        global game_state
        if game_state is not Game_State.animation:
            self.moving = False

def create_objects():
    global all_objects
    obj1 = Element(0)
    obj2 = Element(1)
    obj3 = Element(2)
    obj4 = Element(3)
    all_objects = [obj1, obj2, obj3, obj4]

def random_object():
    global all_objects
    return Element(random.randrange(0,len(all_objects)))

def cleanup():
    pygame.display.quit()
    sys.exit()

def poll_events():
    global cursor_pos
    global selected_element
    global do_quit
    global match_length
    global gameboard_size
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                cleanup()
            elif event.key == K_SPACE:
                gameboard.check_adjacency(3)
            elif event.key == K_RETURN:
                gameboard.check_drop()
                set_game_state(Game_State.animation)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                x,y = pygame.mouse.get_pos()
                x = int(int(x-margin[0])/image_size)
                y = int(int(y-margin[1])/image_size)
                if selected_element[0] == x and selected_element[1] == y:
                    selected_element = (-1, -1)
                    continue
                if not (x < 0 or x >= gameboard.gameboard_size or y < 0 or y >= gameboard.gameboard_size):
                    gameboard.swap_elements([x, y], selected_element)
                update_board()
        elif event.type == QUIT:
            do_quit = True
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x,y = pygame.mouse.get_pos()
                x = int(int(x-margin[0])/image_size)
                y = int(int(y-margin[1])/image_size)
                if not (x < 0 or x >= gameboard.gameboard_size or y < 0 or y >= gameboard.gameboard_size):
                    selected_element = [x, y]
        elif event.type == MOUSEMOTION:
            cursor_pos = pygame.mouse.get_pos()

def update_board():
    global game_state
    game_state = Game_State.update

def load_images():
    global image_cache
    global sprite_paths
    global background
    #We use pink as the transparency color currently
    transparent = (255, 0, 220)
    for path in sprite_paths:
        image_cache = image_cache + [pygame.image.load(path).convert()]
    for img in image_cache:
        img.set_colorkey(transparent)
    background = pygame.image.load("gfx/background.jpg")

def stop_moving():
    for row in gameboard.Gameboard:
        for obj in row:
            if obj is not None:
                obj.moving = False

def do_animations():
    global anim_progress
    global match_length
    anim_progress += 4
    if anim_progress >= image_size:
        anim_progress = 0.0
        stop_moving()
        set_game_state(Game_State.update)

def game_loop():
    global game_state
    global match_length
    if game_state == Game_State.ready:
        poll_events()
    elif game_state == Game_State.animation:
        do_animations()
    elif game_state == Game_State.update:
        if gameboard.check_drop():
            set_game_state(Game_State.animation)
        elif not gameboard.check_adjacency(match_length):
            set_game_state(Game_State.ready)

def set_game_state(new_state):
    global game_state
    if new_state < 0 or new_state >= Game_State.last_state:
        return
    game_state = new_state

def get_selected_element():
    return gameboard.Gameboard[selected_element[0]][selected_element[1]]

def draw_background():
    global background
    screen.blit(background, (0, 0))

def main():
    global screen
    global cursor_pos
    global selected_element
    global do_quit
    screen = pygame.display.set_mode((1024, 768))
    load_images()
    create_objects()
    gameboard.random_gameboard()
    selected_element = (-1, -1)
    while not do_quit:
        screen.fill((0,0,0))
        draw_background()
        game_loop()
        for x in range(0, gameboard.gameboard_size):
            for y in range(0, gameboard.gameboard_size):
                obj = gameboard.Gameboard[x][y]
                if selected_element == [x, y]:
                    continue
                elif (obj is not None):
                    obj.update()
                    obj.draw(x, y)
        if not selected_element == (-1, -1):
            get_selected_element().draw_true(cursor_pos[0], cursor_pos[1])
        pygame.display.flip()
    pygame.display.quit()
    
main()
