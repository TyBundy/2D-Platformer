# Import statements
import pygame as pyg
pyg.init()
pyg.font.init()

# Custom modules
from classes.globals import Colors, Globals, Settings

import modules.collider as collider
import modules.text_display as text_display
import modules.util as util

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
    for i in range(len(Settings.SETTING_MENUS) - 1 + quit):
        Draw_Sidebar_Item(Settings.SETTING_MENUS[i], (100, 150 + i * 50))

    for i in range(len(Settings.SETTING_ITEMS[Globals.current_setting])):
        item = Settings.SETTING_ITEMS[Globals.current_setting][i]
        if item["type"] == "Checkbox":
            draw_checkbox(item, (270, 150 + i * 40))

        elif item["type"] == "Dropdown":
            draw_dropdown(item, (270, 150 + i * 40))

    if active_dropdown != -1:
        draw_active_dropdown(Settings.SETTING_ITEMS[Globals.current_setting][active_dropdown], (270, 150 + active_dropdown * 40))
    
# Check for mouse press
def check_settings_mpress(quit=False):
    global active_dropdown
    dont_dropdown = False
    # Check for a dropdown item selected
    if active_dropdown != -1:
        index = check_active_dropdown(Settings.SETTING_ITEMS[Globals.current_setting][active_dropdown], (270, 150 + active_dropdown * 40))
        if index is not None:
            Settings.SETTING_ITEMS[Globals.current_setting][active_dropdown]["value"] = Settings.SETTING_ITEMS[Globals.current_setting][active_dropdown]["options"][index]
            dont_dropdown = True

    active_dropdown = -1
    # Check the sidebar items
    for i in range(len(Settings.SETTING_MENUS) - 1 + quit):
        if Check_Button((140, 150 + i * 50), (100, 35)):
            if Settings.SETTING_MENUS[i] == "Quit to Menu":
                return "Quit"

            Globals.current_setting = Settings.SETTING_MENUS[i]

    # Check the settings item that was clicked
    if Globals.current_setting != "Quit to Menu" and not dont_dropdown:
        for j in range(len(Settings.SETTING_ITEMS[Globals.current_setting])):
            item = Settings.SETTING_ITEMS[Globals.current_setting][j]
            if item["type"] == "Checkbox":
                if check_checkbox(item, (270, 150 + j * 40)):
                    if item["value"]:
                        Settings.SETTING_ITEMS[Globals.current_setting][j]["value"] = 0
                    else:
                        Settings.SETTING_ITEMS[Globals.current_setting][j]["value"] = 1

            elif item["type"] == "Dropdown":
                if check_dropdown(item, (270, 150 + j * 40)):
                    active_dropdown = j
                    if item["active"]:
                        Settings.SETTING_ITEMS[Globals.current_setting][j]["active"] = 0
                    else:
                        Settings.SETTING_ITEMS[Globals.current_setting][j]["active"] = 1

                
# Draws the setting's sidebar items
def Draw_Sidebar_Item(text, location, font=Fonts.back_box_font):
    text_width, text_height = font.size(text)
    
    # Check mouse collision
    if collider.collides_rect((location[0] - 10, location[1] - text_height/2 - 5, 100, 35), Globals.mouse_position):
        pyg.draw.rect(Globals.VID_BUFFER, Colors.MEDIUM_GRAY, (location[0], location[1] + text_height/2, text_width, 2))

    # Check if it's the active setting
    if text == Globals.current_setting:
        pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (location[0], location[1] + text_height/2, text_width, 2))
    
    text_display.left_text(text, font, Colors.WHITE, (location[0], location[1]))

# Checks if a mouse click happened on the given button
def Check_Button(location, size):
    return collider.collides_rect((location[0] - size[0]/2 + 2, location[1] - size[1]/2 + 2, size[0], size[1]), Globals.mouse_position)

# Draw checkboxes
def draw_checkbox(item, location):
    text_width, text_height = Fonts.settings_font.size(item["name"])

    text_display.left_text(item["name"], Fonts.settings_font, Colors.WHITE, location)

    pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (location[0] + text_width + 20, location[1] - 11, 20, 20))
    pyg.draw.rect(Globals.VID_BUFFER, Colors.GREEN if item["value"] else Colors.DARK_GRAY, (location[0] + text_width + 21, location[1] - 10, 18, 18))
    
# Checks if a checkbox was clicked
def check_checkbox(item, location):
    text_width, text_height = Fonts.settings_font.size(item["name"])
    return collider.collides_rect((location[0] + text_width + 20, location[1] - 11, 20, 20), Globals.mouse_position)


# Draw dropdowns
def draw_dropdown(item, location):
    text_width, _ = Fonts.settings_font.size(item["name"])

    text_display.left_text(item["name"], Fonts.settings_font, Colors.WHITE, location)

    active_option = item["value"]
    active_width, active_height = Fonts.settings_font.size(active_option)

    # Draw text box
    pyg.draw.rect(Globals.VID_BUFFER, Globals.settings_background, (location[0] + text_width + 22, location[1] - active_height/2 - 2, active_width + 24, active_height * len(item["options"]) + 4))
    pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (location[0] + text_width + 20, location[1] - active_height/2 - 2, active_width + 24, active_height + 4))
    pyg.draw.rect(Globals.VID_BUFFER, Colors.DARK_GRAY, (location[0] + text_width + 22, location[1] - active_height/2, active_width + 20, active_height))
    text_display.left_text(active_option, Fonts.settings_font, Colors.WHITE, (location[0] + text_width + 24, location[1]))

    # Draw dropdown arrow
    pyg.draw.line(Globals.VID_BUFFER, Colors.WHITE, (location[0] + text_width + active_width + 30, location[1] - 4), (location[0] + text_width + active_width + 34, location[1] + 4))
    pyg.draw.line(Globals.VID_BUFFER, Colors.WHITE, (location[0] + text_width + active_width + 38, location[1] - 4), (location[0] + text_width + active_width + 34, location[1] + 4))

# Checks if a dropdown was clicked
def check_dropdown(item, location):
    text_width, _ = Fonts.settings_font.size(item["name"])
    
    active_option = item["value"]
    active_width, active_height = Fonts.settings_font.size(active_option)
    return collider.collides_rect((location[0] + text_width + 20, location[1] - active_height/2 - 2, active_width + 24, active_height + 4), Globals.mouse_position)

# Draw checkboxes
def draw_active_dropdown(item, location):
    text_width, _ = Fonts.settings_font.size(item["name"])

    text_display.left_text(item["name"], Fonts.settings_font, Colors.WHITE, location)

    num_options = len(item["options"])
    active_width = 0

    for i in range(num_options):
        option = item["options"][i]
        temp_w, active_height = Fonts.settings_font.size(option)
        if active_width < temp_w:
            active_width = temp_w

    # Draw text box
    pyg.draw.rect(Globals.VID_BUFFER, Globals.settings_background, (location[0] + text_width + 22, location[1] - active_height/2 - 2, active_width + 24, active_height + 4))
    pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (location[0] + text_width + 20, location[1] - active_height/2 - 2, active_width + 8, 4 + (active_height * num_options)))
    pyg.draw.rect(Globals.VID_BUFFER, Colors.DARK_GRAY, (location[0] + text_width + 22, location[1] - active_height/2, active_width + 4, (active_height * num_options)))

    for i in range(num_options):
        active_option = item["options"][i]
        text_display.left_text(active_option, Fonts.settings_font, Colors.WHITE, (location[0] + text_width + 24, location[1] + active_height * i))

# Checks if a dropdown was clicked
def check_active_dropdown(item, location):
    text_width, _ = Fonts.settings_font.size(item["name"])
    
    num_options = len(item["options"])
    active_width = 0

    for i in range(num_options):
        option = item["options"][i]
        temp_w, active_height = Fonts.settings_font.size(option)
        if active_width < temp_w:
            active_width = temp_w
    
    for i in range(num_options):
        if collider.collides_rect((location[0] + text_width + 24, location[1] - active_height/2-2 + active_height * i, active_width + 24, active_height + 4), Globals.mouse_position):
            return i