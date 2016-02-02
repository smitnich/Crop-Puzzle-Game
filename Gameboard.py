import Score
import Globals
import sys
import random
import Seeds

Gameboard_size = 10
Gameboard = [[0 for x in range(Gameboard_size)] for x in range(Gameboard_size)]
seed_size = 5

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
        global seed_size
        Score.Add_Match(self.x_length + self.y_length)
        if (self.x_length + self.y_length >= seed_size):
            Seeds.add_seed(get_element_index(self.x, self.y))
        if self.x_length > 0:
            for i in range(0, self.x_length):
                delete_object(self.x + i, self.y)
        elif self.y_length > 0:
            for i in range(0, self.y_length):
                delete_object(self.x, self.y + i)
        ## Grow any seeds on the board
        grow_seeds()

def check_max_count(in_list):
    max_count = 0
    max_id = -1
    ids = list(o.index for o in in_list)
    for i in range(0, len(Globals.all_objects)):
        count = ids.count(i)
        if count > max_count:
            max_count = count
            max_id = i
    return max_count, max_id

def check_swap_horiz(x, y, id, length):
    for i in range(0, length):
        obj = Gameboard[x + i][y]
        if (obj.index != id):
            ##Check left of the first element
            if i == 0 and x > 0 and Gameboard[x - 1][y].is_index(id):
                return True, x+i-1, y
            elif y > 0 and x + i < Gameboard_size and Gameboard[x + i][y - 1].is_index(id):
                return True, x+i, y-1
            elif y + 1 < Gameboard_size and x + i < Gameboard_size and Gameboard[x + i][y + 1].is_index(id):
                return True, x+i, y+1
            elif i == length - 1 and x + i + 1 < Gameboard_size and Gameboard[x + i + 1][y].is_index(id):
                return True, x+i+1, y
    return False, -1, -1 

def check_swap_vert(x, y, id, length):
    for i in range(0, length):
        obj = Gameboard[x][y + i]
        if (obj.index != id):
            ##Check above the first element
            if i == 0 and y > 0 and Gameboard[x][y - 1].is_index(id):
                return True, x, y-1
            elif x > 0 and y + i < Gameboard_size and Gameboard[x - 1][y + i].is_index(id):
                return True, x+i, y-1
            elif x + 1 < Gameboard_size and y + i < Gameboard_size and Gameboard[x + 1][y + i].is_index(id):
                return True, x+i, y+1
            elif i == length - 1 and y + i + 1 < Gameboard_size and Gameboard[x][y + i + 1].is_index(id):
                return True, x+i+1, y
    return False, -1, -1 

def check_availible_moves():
    try:
        global Gameboard_size
        match_length = Globals.match_length
        offset = match_length - 1
        ##Check if it is possible to make a horizontal line by moving one tile
        for y in range(0, Gameboard_size):
            break
            l = list((Gameboard[0][y], Gameboard[1][y]))
            for x in range(offset, Gameboard_size):
                l.append(Gameboard[x][y])
                max_count, id = check_max_count(l)
                if (max_count == match_length - 1):
                    res, xPos, yPos = check_swap_horiz(x - offset, y, id, match_length)
                    if res:
                        return True
                l.pop(0)

        ##Check if it possible to make a vertical line by moving one tile
        for x in range(0, Gameboard_size):
            l = list((Gameboard[x][0], Gameboard[x][1]))
            for y in range(offset, Gameboard_size):
                l.append(Gameboard[x][y])
                max_count, id = check_max_count(l)
                if (max_count == match_length - 1):
                    res, xPos, yPos = check_swap_vert(x , y - offset, id, match_length)
                    if res:
                        return True
                l.pop(0)

    except:
        print("Unexpected error:", sys.exc_info()[0])


def move_element(obj, x, y):
    global Gameboard_size
    if (x < 0) or (y < 0) or x > (Gameboard_size) or (y > Gameboard_size):
        return
    if Gameboard[x][y] is not None:
        print(x,y," is not None")
        return
    Gameboard[x][y] = obj
    if obj is not None:
        obj.moving = True

def random_Gameboard():
    from Main import random_object
    global Gameboard_size
    global Gameboard
    global image_size
    for x in range(0, Gameboard_size):
        for y in range(0, Gameboard_size):
            obj = random_object()
            Gameboard[x][y] = obj
    ## Don't let any matches exist when the board is created
    check_adjacency(3)
    fill_empty_spaces(3)

def plant_seed(pos, index):
    global Gameboard
    from Main import make_element
    if not Seeds.can_plant(index):
        return
    x = pos[0]
    y = pos[1]
    obj = make_element(index)
    obj.time_to_grow = Globals.growth_time
    Gameboard[x][y] = obj

#Check for any elements that have an empty space below them
def check_drop():
    from Main import random_object
    global Gameboard
    global Gameboard_size
    drop_found = False
    for tmpy in range(2, Gameboard_size + 1):
        #Start at the bottom so that elements above will
        #drop down when the ones below them do so
        y = Gameboard_size - tmpy
        for x in range(0, Gameboard_size):
            obj = Gameboard[x][y]
            if obj is None:
                if y is 0:
                    newobj = random_object()
                    move_element(newobj, x, 0)
                    drop_found = True
                continue
            if Gameboard[x][y + 1] is None:
                drop_found = True
                move_element(obj, x, y + 1)
                Gameboard[x][y] = None
                if y is 0:
                    newobj = random_object()
                    move_element(newobj, x, 0)
    return drop_found

def delete_object(x,y):
    global Gameboard
    global Gameboard_size
    if (x > Gameboard_size or y > Gameboard_size or x < 0 or y < 0):
        return
    Gameboard[x][y] = None

def swap_elements(first, second):
    global Gameboard_size
    global Gameboard
    global selected_element
    if first == second:
        return
    obj1 = Gameboard[first[0]][first[1]]
    obj2 = Gameboard[second[0]][second[1]]
    Gameboard[second[0]][second[1]] = obj1
    Gameboard[first[0]][first[1]] = obj2
    selected_element = (-1, -1)

def check_adjacency(match_length):
    global Gameboard
    global Gameboard_size
    match_found = False
    delete_requests = []
    for x in range(0, Gameboard_size):
        match_count = 0
        to_match = get_element_index(x,0)
        for y in range(0, Gameboard_size):
            if get_element_index(x,y) == to_match and to_match is not -1:
                match_count = match_count + 1
            else:
                if match_count >= match_length:
                    match_found = True
                    new_req = Delete_Request(x, y - match_count, 0, match_count)
                    delete_requests.append(new_req)
                match_count = 1
            to_match = get_element_index(x,y)
        if match_count >= match_length:
            match_found = True
            new_req = Delete_Request(x, Gameboard_size - match_count, 0, match_count)
            delete_requests.append(new_req)

    horiz_matches = check_horiz_adjacency(match_length)
    if len(horiz_matches) > 0:
        match_found = True
    delete_requests.extend(horiz_matches)

    for request in delete_requests:
        request.delete()
    return match_found

## Check if placing an object with this index at location x, y would lead to a new match
## being created
def check_adjacent_count(index, x, y, match_length):
    c = 0
    c_max = 0
    ## The distance we need to check in each direction
    l = match_length - 1

    for i in range(max(0, x - l), min(Gameboard_size, x + l)):
        if (Gameboard[i][y] == index):
            c = c + 1
        else:
            if c > c_max:
                c_max = c
            c = 0
    if c > c_max:
        c_max = c

    c = 0

    for i in range(max(0, y - l), min(Gameboard_size, y + l)):
        if (Gameboard[x][i] == index):
            c = c + 1
        else:
            if c > c_max:
                c_max = c
            c = 0
    if c > c_max:
        c_max = c
    return c_max

def fill_empty_space(match_length, x, y):
    from Main import make_element
    random_order = list(range(0, len(Globals.sprite_paths)))
    random.shuffle(random_order)
    for r in random_order:
        if (check_adjacent_count(r, x, y, match_length) < match_length):
            Gameboard[x][y] = make_element(r)
            return True
    return False

def fill_empty_spaces(match_length):
    for x in range(0, Gameboard_size):
        for y in range(0, Gameboard_size):
            if Gameboard[x][y] is None:
                fill_empty_space(match_length, x, y)

def get_element_index(x,y):
    obj = Gameboard[x][y]
    if obj is None:
        return -1
    else:
        return obj.index

def grow_seeds():
    global Gameboard
    global Gameboard_size
    for x in range(0, Gameboard_size):
        for y in range(0, Gameboard_size):
            if (Gameboard[x][y] is not None):
                Gameboard[x][y].grow()

def check_horiz_adjacency(match_length):
    global Gameboard
    global Gameboard_size
    global match_found
    match_found = False
    delete_requests = []
    for y in range(0, Gameboard_size):
        match_count = 0
        to_match = get_element_index(0,y)
        for x in range(0, Gameboard_size):
            if get_element_index(x,y) == to_match and to_match is not -1:
                match_count = match_count + 1
            else:
                if match_count >= match_length:
                    match_found = True
                    new_req = Delete_Request(x - match_count, y, match_count, 0)
                    delete_requests.append(new_req)
                match_count = 1
            to_match = get_element_index(x,y)
        if match_count >= match_length:
            match_found = True
            new_req = Delete_Request(Gameboard_size - match_count, y, match_count, 0)
            delete_requests.append(new_req)

    return delete_requests
