# Import statements
import pygame as pyg
pyg.init()
pyg.font.init()

from classes.globals import Colors, Globals
import modules.text_display as text_display 

class Fonts:
    debug_font = pyg.font.SysFont("consolas", 14)

# Draws the debug menu
def draw_debug_menu():
    width, height = 200, 200
    box_x, box_y = 10, Globals.WINDOW_HEIGHT - 210
    pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (box_x, box_y, width, height))
    pyg.draw.rect(Globals.VID_BUFFER, Colors.DARK_GRAY, (box_x + 2, box_y + 2, width-4, height-4))

    debug_list = [
        "Screen Size: " + str(Globals.WINDOW_WIDTH) + "x" + str(Globals.WINDOW_HEIGHT),
        "Mouse Pos: " + str(Globals.mouse_position),
        "Hovering: " + ("True" if Globals.debug["hovering"] else "False")
    ]

    # Display properties of hovered object
    if Globals.debug["hovering"]:
        object = Globals.debug["hover_object"]
        x, y = int(object.x), int(object.y)
        ow, oh = int(object.width), int(object.height)

        debug_list += ["X/Y: (" + str(x) + ", " + str(y) + ")"]
        debug_list += ["W/H: (" + str(ow) + ", " + str(oh) + ")"]
        debug_list += ["Left: " + str(int(x - ow/2)) + " | Top: " + str(int(y - oh/2))]
        debug_list += ["Text: " + object.text]
        debug_list += ["Type: " + object.type]

    # Display text
    vert_offset = 4
    for item in debug_list:
        text_display.upleft_text(item, Fonts.debug_font, Colors.WHITE, (box_x + 5, box_y + vert_offset))
        vert_offset += 15
