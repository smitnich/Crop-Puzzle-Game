import pygame
import random
import sys
import Score
import TextHandler
from pygame.locals import *
import Gameboard
import Globals

from enum import IntEnum

class Game_State(IntEnum):
    ready = 1
    animation = 2
    update = 3
    last_state = 4

class Element:
    index = 0
    moving = False
    sprite = None
    highlighted = False
    def __init__(self, _index):
        self.index = _index
        self.sprite = Globals.image_cache[self.index]

    def draw(self,x,y):
        margin = Globals.margin
        image_size = Globals.image_size
        trueX = x
        trueY = y
        if self.moving:
            x = x*image_size+margin[0]
            y = (y-1)*image_size+int(Globals.anim_progress)+margin[1]
        else:
            x = x*image_size+margin[0]
            y = y*image_size+margin[1]
        Globals.screen.blit(self.sprite,(x,y))
        if self.highlighted:
            self.draw_box((trueX, trueY))

    def draw_true(self, x, y):
        Globals.screen.blit(self.sprite, (x-Globals.image_size/2, y-Globals.image_size/2))

    def draw_box(self, pos):
        image_size = Globals.image_size
        rectangle = (pos[0]*image_size+Globals.margin[0], pos[1]*image_size+Globals.margin[1], image_size, image_size)
        pygame.draw.rect(Globals.screen, (255, 255, 255), rectangle, 1)

    def update(self):
        if Globals.game_state is not Globals.Game_State.animation:
            self.moving = False

def create_objects():
    obj1 = Element(0)
    obj2 = Element(1)
    obj3 = Element(2)
    obj4 = Element(3)
    Globals.all_objects = [obj1, obj2, obj3, obj4]

def random_object():
    return Element(random.randrange(0,len(Globals.all_objects)))

def cleanup():
    pygame.display.quit()
    sys.exit()

def coord_distance(coord1, coord2):
    return abs(coord1[0]-coord2[0])+abs(coord1[1] - coord2[1])

def poll_events():
    global cursor_pos
    margin = Globals.margin
    image_size = Globals.image_size
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                cleanup()
            elif event.key == K_SPACE:
                Gameboard.check_adjacency(3)
            elif event.key == K_RETURN:
                Gameboard.check_drop()
                set_game_state(Globals.Game_State.animation)
        elif event.type == QUIT:
            Globals.do_quit = True
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x,y = pygame.mouse.get_pos()
                x = int(int(x-margin[0])/image_size)
                y = int(int(y-margin[1])/image_size)
                if not (x < 0 or x >= Gameboard.Gameboard_size or y < 0 or y >= Gameboard.Gameboard_size):
                    if (Globals.selected_element == [x, y]):
                        Globals.selected_element = (-1, -1)
                    elif Globals.selected_element == (-1, -1):
                        Globals.selected_element = [x, y]
                    else:
                        if coord_distance(Globals.selected_element, [x, y]) <= 1:
                            Gameboard.swap_elements(Globals.selected_element, [x, y])
                        Globals.selected_element = (-1, -1)
        elif event.type == MOUSEMOTION:
            cursor_pos = pygame.mouse.get_pos()

def update_board():
    Globals.game_state = Game_State.update

def load_images():
    #We use pink as the transparency color currently
    transparent = (255, 0, 220)
    for path in Globals.sprite_paths:
        Globals.image_cache = Globals.image_cache + [pygame.image.load(path).convert()]
    for img in Globals.image_cache:
        img.set_colorkey(transparent)
    Globals.background = pygame.image.load("gfx/background.jpg")

def stop_moving():
    for row in Gameboard.Gameboard:
        for obj in row:
            if obj is not None:
                obj.moving = False

def do_animations():
    Globals.anim_progress += 4
    if Globals.anim_progress >= Globals.image_size:
        Globals.anim_progress = 0.0
        stop_moving()
        set_game_state(Globals.Game_State.update)

def game_loop():
    if Globals.game_state == Globals.Game_State.ready:
        poll_events()
    elif Globals.game_state == Globals.Game_State.animation:
        do_animations()
    elif Globals.game_state == Globals.Game_State.update:
        if Gameboard.check_drop():
            set_game_state(Globals.Game_State.animation)
        elif not Gameboard.check_adjacency(Globals.match_length):
            set_game_state(Globals.Game_State.ready)

def set_game_state(new_state):
    if new_state < 0 or new_state >= Globals.Game_State.last_state:
        return
    Globals.game_state = new_state

def get_selected_element():
    return Gameboard.Gameboard[Globals.selected_element[0]][Globals.selected_element[1]]

def draw_background():
    Globals.screen.blit(Globals.background, (0, 0))

def draw_score():
    score = Score.Get_Score()
    x_off = Globals.margin[0]*2 + Globals.image_size*Gameboard.Gameboard_size
    y_off = Globals.margin[1]
    TextHandler.RenderText(str(score), x_off, y_off)

def Main():
    if __name__ != "__main__":
        return
    global cursor_pos
    Globals.init()
    Globals.screen = pygame.display.set_mode((1024, 768))
    TextHandler.Init()
    load_images()
    create_objects()
    Gameboard.random_Gameboard()
    Score.Reset_Score()
    Globals.selected_element = (-1, -1)
    Gameboard.check_availible_moves()
    while not Globals.do_quit:
        Globals.screen.fill((0,0,0))
        draw_background()
        game_loop()
        for x in range(0, Gameboard.Gameboard_size):
            for y in range(0, Gameboard.Gameboard_size):
                obj = Gameboard.Gameboard[x][y]                    
                if (obj is not None):
                    obj.update()
                    obj.draw(x, y)
        if not Globals.selected_element == (-1, -1):
            element = get_selected_element()
            if element is not None:
                element.draw_box(Globals.selected_element)
        draw_score()
        pygame.display.flip()
    pygame.display.quit()
    
Main()
