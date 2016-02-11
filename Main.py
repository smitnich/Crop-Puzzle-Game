import pygame
import random
import sys
import Score
import TextHandler
from pygame.locals import *
import Gameboard
import Globals
import Seeds
import Graphic_Element

from enum import IntEnum

seed_sprite = None

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
    growth_turn = -1
    grown = True
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
        if not self.grown:
            Globals.screen.blit(Globals.seed_sprite, (x,y))
        else:
            Globals.screen.blit(self.sprite,(x,y))
        if self.highlighted:
            self.draw_box((trueX, trueY))

    def draw_true(self, x, y):
        Globals.screen.blit(self.sprite, (x-Globals.image_size/2, y-Globals.image_size/2))

    def grow(self):
        if self.growth_turn > 0 and Globals.current_turn >= self.growth_turn:
            self.grown = True

    def is_index(self,index):
        return self.index == index and self.grown

    def draw_box(self, pos):
        image_size = Globals.image_size
        rectangle = (pos[0]*image_size+Globals.margin[0], pos[1]*image_size+Globals.margin[1], image_size, image_size)
        pygame.draw.rect(Globals.screen, (255, 255, 255), rectangle, 1)

    def update(self):
        if Globals.game_state is not Globals.Game_State.animation:
            self.moving = False
    
    def make_poof(self, x, y):
        from Graphic_Element import make_graphic_element
        image_size = Globals.image_size
        x = x*image_size+Globals.margin[0]
        y = y*image_size+Globals.margin[1]
        make_graphic_element(Globals.poof_sprite, x, y, get_ticks() + 200)

def make_element(index):
    return Element(index)

def create_objects():
    Globals.all_objects = []
    for i in range(0, len(Globals.sprite_paths)):
        Globals.all_objects.append(Element(i))

def random_object():
    return Element(random.randrange(0,len(Globals.all_objects)))

def cleanup():
    pygame.display.quit()
    sys.exit()

def coord_distance(coord1, coord2):
    return abs(coord1[0]-coord2[0])+abs(coord1[1] - coord2[1])

def poll_events():
    global selected_seed
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
                selected_seed = Seeds.get_selected_seed()
                if selected_seed != -1:
                    if (Seeds.can_plant(selected_seed)):
                        pos = mouse_to_coord(pygame.mouse.get_pos())
                        if (pos[0] < 0 or pos[0] > Gameboard.Gameboard_size or
                            pos[1] < 0 or pos[1] > Gameboard.Gameboard_size):
                            Seeds.selected_seed = -1
                        else:
                            Gameboard.plant_seed(pos, Seeds.get_selected_seed())
                            Seeds.remove_seed(selected_seed)
                    Seeds.selected_seed = -1
                else:
                    try_swap()
                    Seeds.check_seed_click(pygame.mouse.get_pos())
        elif event.type == MOUSEMOTION:
            cursor_pos = pygame.mouse.get_pos()

def mouse_to_coord(pos):
    image_size = Globals.image_size
    margin = Globals.margin
    x = pos[0]
    y = pos[1]
    x = int(int(x - margin[0]) / image_size)
    y = int(int(y - margin[1]) / image_size)
    return (x,y)

def try_swap():
    global cursor_pos
    margin = Globals.margin
    image_size = Globals.image_size
    x,y = pygame.mouse.get_pos()
    x = int(int(x - margin[0]) / image_size)
    y = int(int(y - margin[1]) / image_size)
    if not (x < 0 or x >= Gameboard.Gameboard_size or y < 0 or y >= Gameboard.Gameboard_size):
        if (Globals.selected_element == [x, y]):
            Globals.selected_element = (-1, -1)
        elif Globals.selected_element == (-1, -1):
            Globals.selected_element = [x, y]
        else:
            if coord_distance(Globals.selected_element, [x, y]) <= 1:
                Gameboard.swap_elements(Globals.selected_element, [x, y])
                old_swap = ([x,y], Globals.selected_element)
                ## if we didn't get a match, undo this swap
                if not Gameboard.check_adjacency(3):
                    Gameboard.swap_elements(old_swap[0], old_swap[1])
                    return
                Gameboard.check_drop()
                set_game_state(Globals.Game_State.animation)
                Globals.selected_element = (-1, -1)

def update_board():
    Globals.game_state = Game_State.update

def load_images():
    #We use light gray as the transparency color currently
    transparent = (200, 200, 200)
    for path in Globals.sprite_paths:
        surf = process_image(path)
        Globals.image_cache = Globals.image_cache + [surf]
    ## Don't process the background since it isn't transparent or 64 by 64
    Globals.background = pygame.image.load("gfx/background.jpg")
    Globals.seed_sprite = process_image("gfx/seed.png")
    Globals.poof_sprite = process_image("gfx/Poof.png")

def process_image(path):
    transparent = (200, 200, 200)
    img = pygame.transform.scale(pygame.image.load(path), (64, 64))
    img.set_colorkey(transparent)
    return img

def stop_moving():
    for row in Gameboard.Gameboard:
        for obj in row:
            if obj is not None:
                obj.moving = False

def do_animations():
    Globals.anim_progress += 8
    if Globals.anim_progress >= Globals.image_size:
        Globals.anim_progress = 0.0
        stop_moving()
        set_game_state(Globals.Game_State.update)

def reset_board():
    Score.Reset_Combo()
    Gameboard.random_Gameboard()

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
            Score.Reset_Combo()
            Globals.current_turn += 1
            if not Gameboard.check_availible_moves():
                Graphic_Element.make_graphic_element(
                    TextHandler.Render_TextBox("Shuffling Board",(255,255,255)), 250, 250, get_ticks() + 1000)
                reset_board()

def set_game_state(new_state):
    if new_state < 0 or new_state >= Globals.Game_State.last_state:
        return
    Globals.game_state = new_state

def get_selected_element():
    return Gameboard.Gameboard[Globals.selected_element[0]][Globals.selected_element[1]]

def draw_background():
    Globals.screen.blit(Globals.background, (0, 0))

def update_ticks():
    Globals.current_ticks = pygame.time.get_ticks()

def get_ticks():
    return Globals.current_ticks

def draw_score():
    score = Score.Get_Score()
    x_off = Globals.margin[0]*2 + Globals.image_size*Gameboard.Gameboard_size
    y_off = Globals.margin[1]
    TextHandler.RenderScore(str(score), x_off, y_off)
    combo = Score.Get_Combo()
    x_off = Globals.margin[0]*2 + Globals.image_size*Gameboard.Gameboard_size
    y_off = Globals.margin[1]+64
    TextHandler.RenderCombo(("x" + str(combo)), x_off, y_off)
    Globals.update_score = False


def Main():
    from Graphic_Element import draw_graphic_elements
    if __name__ != "__main__":
        return
    global current_ticks
    global cursor_pos
    Globals.init()
    Globals.screen = pygame.display.set_mode((Globals.screenX, Globals.screenY))
    TextHandler.Init()
    pygame.init()
    load_images()
    create_objects()
    Gameboard.random_Gameboard()
    Score.Reset_Score()
    Globals.selected_element = (-1, -1)
    Gameboard.check_availible_moves()
    Seeds.seed_init(len(Globals.all_objects))
    while not Globals.do_quit:
        update_ticks()
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
        Seeds.draw_seed_interface()
        draw_graphic_elements(get_ticks())
        pygame.display.flip()
        
    pygame.display.quit()
    
Main()
