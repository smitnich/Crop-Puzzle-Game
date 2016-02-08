## A class which contains a sprite to displayed at a location,
## for a specifed amount of milliseconds
import Globals
all_graphic_elements = []

class Graphic_Element:
    death_time = -1
    pos = (0,0)
    sprite = None
    def draw(self):
        Globals.screen.blit( self.sprite, self.pos)
    def should_die(self, ticks):
        return ticks >= self.death_time and self.death_time != -1

def draw_graphic_elements(time):
    global all_graphic_elements
    all_graphic_elements[:] = [x for x in all_graphic_elements if not x.should_die(time)]
    for e in all_graphic_elements:
        e.draw()

def make_graphic_element(_sprite, x, y, _death_time):
    global all_graphic_elements
    e = Graphic_Element()
    e.death_time = _death_time
    e.pos = (x, y)
    e.sprite = _sprite
    all_graphic_elements.append(e)
