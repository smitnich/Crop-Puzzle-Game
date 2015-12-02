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
selected_element = [-1, -1]
background = None

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
        if self.moving:
            screen.blit(self.sprite,(x*image_size, (y-1)*image_size+int(anim_progress)))
        else:
            screen.blit(self.sprite,(x*image_size, y*image_size))

    def draw_true(self, x, y):
        global image_size
        screen.blit(self.sprite, (x-image_size/2, y-image_size/2))
    
    def update(self):
        global game_state
        if game_state is not Game_State.animation:
            self.moving = False

class Delete_Request:
    x = 0
    y = 0
    x_length = 0
    y_length = 0
    def __init__(self, _x, _y, _x_length, _y_length):
        self.x = _x
        self.y = _y
        self.x_length = _x_length
        self.y_length = _y_length
        
    def delete(self):
        if self.x_length > 0:
            for i in range(0, self.x_length):
                delete_object(self.x+i, self.y)
        elif self.y_length > 0:
            for i in range(0, self.y_length):
                delete_object(self.x, self.y+i)

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

#Check for any elements that have an empty space below them
def check_drop():
    global gameboard
    global gameboard_size
    drop_found = False
    for tmpy in range(2, gameboard_size+1):
        #Start at the bottom so that elements above will
        #drop down when the ones below them do so
        y = gameboard_size - tmpy
        for x in range(0, gameboard_size):
            obj = Gameboard[x][y]
            if obj is None:
                if y is 0:
                    newobj = random_object()
                    move_element(newobj, x, 0)
                    drop_found = True
                continue
            if Gameboard[x][y+1] is None:
                drop_found = True
                move_element(obj, x, y+1)
                Gameboard[x][y] = None
                if y is 0:
                    newobj = random_object()
                    move_element(newobj, x, 0)
    return drop_found
    
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
    add_elements()
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
    delete_requests = []
    for x in range(0, gameboard_size):
        match_count = 0
        to_match = get_element_index(x,0)
        for y in range(0, gameboard_size):
            if get_element_index(x,y) == to_match and to_match is not -1:
                match_count = match_count+1
            else:
                if match_count >= match_length:
                    match_found = True
                    new_req = Delete_Request(x, y-match_count, 0, match_count)
                    delete_requests.append(new_req)
                match_count = 1
            to_match = get_element_index(x,y)
        if match_count >= match_length:
            match_found = True
            new_req = Delete_Request(x, gameboard_size-match_count, 0, match_count)
            delete_requests.append(new_req)

    delete_requests.extend(check_horiz_adjacency(match_length))
    
    for request in delete_requests:
        request.delete()
    return match_found

def get_element_index(x,y):
    obj = Gameboard[x][y]
    if obj is None:
        return -1
    else:
        return obj.index


def check_horiz_adjacency(match_length):
    global Gameboard
    global gameboard_size
    match_found = False
    delete_requests = []
    for y in range(0, gameboard_size):
        match_count = 0
        to_match = get_element_index(0,y)
        for x in range(0, gameboard_size):
            if get_element_index(x,y) == to_match and to_match is not -1:
                match_count = match_count+1
            else:
                if match_count >= match_length:
                    match_found = True
                    new_req = Delete_Request(x-match_count, y, match_count, 0)
                    delete_requests.append(new_req)
                match_count = 1
            to_match = get_element_index(x,y)
        if match_count >= match_length:
            match_found = True
            new_req = Delete_Request(gameboard_size-match_count, y, match_count, 0)
            delete_requests.append(new_req)

    return delete_requests

def random_object():
    global all_objects
    return Element(random.randrange(0,len(all_objects)))

def cleanup():
    pygame.display.quit()
    sys.exit()

def poll_events():
    global cursor_pos
    global selected_element
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                cleanup()
            elif event.key == K_SPACE:
                check_adjacency(3)
            elif event.key == K_RETURN:
                check_drop()
                set_game_state(Game_State.animation)
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                x,y = pygame.mouse.get_pos()
                x = int(int(x)/image_size)
                y = int(int(y)/image_size)
                selected_element = [x, y]
        elif event.type == MOUSEMOTION:
            cursor_pos = pygame.mouse.get_pos()

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

def do_animations():
    global anim_progress
    anim_progress += 2
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
        if check_drop():
            set_game_state(Game_State.animation)
        elif not check_adjacency(match_length):
            set_game_state(Game_State.ready)

def set_game_state(new_state):
    global game_state
    if new_state < 0 or new_state >= Game_State.last_state:
        return
    game_state = new_state

def get_selected_element():
    global Gameboard
    return Gameboard[selected_element[0]][selected_element[1]]

def draw_background():
    global background
    screen.blit(background, (0, 0))

def main():
    global screen
    global cursor_pos
    global selected_element
    screen = pygame.display.set_mode((1024, 768))
    load_images()
    create_objects()
    random_gameboard()
    Gameboard[5][5] = None 
    while True:
        screen.fill((0,0,0))
        draw_background()
        game_loop()
        for x in range(0,gameboard_size):
            for y in range(0, gameboard_size):
                obj = Gameboard[x][y]
                if selected_element == [x, y]:
                    continue
                elif (obj is not None):
                    obj.update()
                    obj.draw(x, y)
        if selected_element is not (-1, -1):
            get_selected_element().draw_true(cursor_pos[0], cursor_pos[1])
        pygame.display.flip()

main()
