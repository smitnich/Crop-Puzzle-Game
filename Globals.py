from enum import IntEnum

class Game_State(IntEnum):
    ready = 1
    animation = 2
    update = 3
    game_over = 4
    last_state = 5

def init():
    global image_size, margin, match_length,sprite_paths,image_cache,all_objects,selected_element
    global background,do_quit,update_score,cursor_pos,game_state,anim_progress,seed_sprite
    global growth_time,current_turn,poof_sprite,current_ticks,screenX,screenY,clock,start_time
    global do_new_game
    image_size = 64
    margin = (16, 16)
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
    screenX = 800
    screenY = 600
    clock = None
    start_time = 0
    do_new_game = True