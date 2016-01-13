from enum import IntEnum

class Game_State(IntEnum):
    ready = 1
    animation = 2
    update = 3
    last_state = 4

def init():
    global image_size
    global margin
    global match_length
    global sprite_paths
    global image_cache
    global all_objects
    global selected_element
    global background
    global do_quit
    global update_score
    global cursor_pos
    global game_state
    global anim_progress
    image_size = 48
    margin = (64, 64)
    match_length = 3
    sprite_paths = ['gfx/fire.png', 'gfx/ice.png', 'gfx/boulder.png', 'gfx/robot.png']
    image_cache = []
    all_objects = None
    selected_element = [-1, -1]
    background = None
    do_quit = False
    update_score = True
    cursor_pos = [0, 0]
    game_state = Game_State.ready
    anim_progress = 0.0
