gameboard_size = 10
Gameboard = [[0 for x in range(gameboard_size)] for x in range(gameboard_size)]

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
    import main
    global gameboard_size
    global Gameboard
    global image_size
    for x in range (0, gameboard_size):
        for y in range (0, gameboard_size):
            obj = main.random_object()
            Gameboard[x][y] = obj
            obj.x = x*main.image_size
            obj.y = y*main.image_size

#Check for any elements that have an empty space below them
def check_drop():
    import main
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
                    newobj = main.random_object()
                    move_element(newobj, x, 0)
                    drop_found = True
                continue
            if Gameboard[x][y+1] is None:
                drop_found = True
                move_element(obj, x, y+1)
                Gameboard[x][y] = None
                if y is 0:
                    newobj = main.random_object()
                    move_element(newobj, x, 0)
    return drop_found

def delete_object(x,y):
    global Gameboard
    global gameboard_size
    if (x > gameboard_size or y > gameboard_size or x < 0 or y < 0):
        return
    Gameboard[x][y] = None

def swap_elements(first, second):
    global gameboard_size
    global Gameboard
    global selected_element
    import main
    if first == second:
        return
    obj1 = Gameboard[first[0]][first[1]]
    obj2 = Gameboard[second[0]][second[1]]
    Gameboard[second[0]][second[1]] = obj1
    Gameboard[first[0]][first[1]] = obj2
    main.selected_element = (-1, -1)

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

    horiz_matches = check_horiz_adjacency(match_length)
    if len(horiz_matches) > 0:
        match_found = True
    delete_requests.extend(horiz_matches)

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