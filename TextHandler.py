import Globals
from pygame import font

font_path = "Base6.ttf"
basic_font = None

def Init():
    global font_path
    global basic_font
    global rendered_text
    font.init()
    basic_font = font.Font(font_path, 32)
    rendered_text = None

def RenderText(text, x, y):
    global basic_font
    global rendered_text
    if Globals.update_score or rendered_text is None:
        rendered_text = basic_font.render(text, False, (0, 0, 0))
    Globals.screen.blit(rendered_text, (x, y))
    Globals.update_score = False


def Deinit():
    font.quit()