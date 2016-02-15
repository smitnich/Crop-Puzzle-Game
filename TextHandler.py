import Globals
from pygame import font

font_path = "Base6.ttf"
basic_font = None
font_color = (255, 255, 255)

def Init():
    global font_path
    global basic_font
    global rendered_text
    global huge_font
    font.init()
    basic_font = font.Font(font_path, 32)
    huge_font = font.Font(font_path, 64)
    rendered_text = None

def RenderScore(text, x, y):
    global basic_font
    global rendered_text
    if Globals.update_score or rendered_text is None:
        rendered_text = basic_font.render(text, True, font_color)
    Globals.screen.blit(rendered_text, (x, y))

def RenderCombo(text, x, y):
    global basic_font
    global rendered_combo
    if Globals.update_score or rendered_combo is None:
        rendered_combo = basic_font.render(text, True, font_color)
    Globals.screen.blit(rendered_combo, (x, y))

def get_font():
    global basic_font
    return basic_font

def Deinit():
    font.quit()

def Render_TextBox(text, textColor):
    global huge_font
    text_box = huge_font.render(text, True, textColor)
    return text_box