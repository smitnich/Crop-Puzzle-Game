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
    global seed_sprite
    global growth_time
    global current_turn
    global poof_sprite
    global current_ticks
    image_size = 64
    margin = (64, 64)
    match_length = 3
    sprite_paths = ['gfx/Eggplant.gif', 'gfx/GreenPepper.gif', 'gfx/Onion.gif',
                    'gfx/Potato.gif', 'gfx/Corn.gif', 'gfx/Cabbage.gif']
    image_cache = []
    poof_sprite = None
    all_objects = None
    selected_element = [-1, -1]
    background = None
    do_quit = False
    update_score = True
    cursor_pos = [0, 0]
    game_state = Game_State.ready
    anim_progress = 0.0
    seed_sprite = None
    growth_time = 3
    current_turn = 0
    current_ticks = 0
