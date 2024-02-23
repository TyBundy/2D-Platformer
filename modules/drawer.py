# Import statements
import pygame as pyg
pyg.init()
pyg.font.init()

# Custom modules
from classes.globals import Globals
from classes.button import Checkbox, Dropdown

class Fonts:
    back_box_font = pyg.font.SysFont("consolas", 20)
    sidebar_font = pyg.font.SysFont("consolas", 30)
    settings_font = back_box_font
    menu_box_font = pyg.font.SysFont("consolas", 40)
    title_font = pyg.font.SysFont("consolas", 60)

active_dropdown = -1

# Draw the different settings and the items of the active one
def draw_settings(quit=False):
    global active_dropdown
    
    # Draw sidebar items
    for button in Globals.sidebar_buttons:
        if not quit and button.text != "Quit to Menu":
            button.draw()
        elif quit:
            button.draw()
            
        if Globals.debug_active and button.check_mcollision():
            Globals.debug["hovering"] = 1
            Globals.debug["hover_object"] = button
            Globals.debug["hover_tyoe"] = button.type

    # Draw setting items
    for button in Globals.setting_buttons[Globals.current_setting]:
        button.draw()

    if active_dropdown != -1:
        Globals.setting_buttons[Globals.current_setting][active_dropdown].draw_active()
    
# Check for mouse press
def check_settings_mpress(quit=False):
    global active_dropdown
    dont_dropdown = False
    # Check for a dropdown item selected
    if active_dropdown != -1:
        index = Globals.setting_buttons[Globals.current_setting][active_dropdown].check_active()
        if index is not None:
            Globals.setting_buttons[Globals.current_setting][active_dropdown].value = Globals.setting_buttons[Globals.current_setting][active_dropdown].options[index]
            dont_dropdown = True

    active_dropdown = -1
    # Check the sidebar items
    for button in Globals.sidebar_buttons:
        res = False
        if not quit and button.text != "Quit to Menu":
            res = button.check_mcollision()
        elif quit:
            res = button.check_mcollision()
        if res:
            if button.text == "Quit to Menu":
                return "Quit"
            Globals.current_setting = button.text

    # Check the settings item that was clicked
    if Globals.current_setting != "Quit to Menu" and not dont_dropdown:
        for button in Globals.setting_buttons[Globals.current_setting]:
            if button.check_mcollision():
                if isinstance(button, Checkbox):
                    if button.value:
                        button.value = 0
                    else:
                        button.value = 1

                elif isinstance(button, Dropdown):
                    active_dropdown = Globals.setting_buttons[Globals.current_setting].index(button)
                    if button.active:
                        button.active = 0
                    else:
                        button.active = 1