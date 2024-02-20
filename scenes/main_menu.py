# Import statements
import pygame as pyg
pyg.init()
pyg.font.init()

# Custom modules
from classes.globals import Colors, Globals, Keybinds
from classes.button import MenuButton, SidebarButton, Checkbox, Dropdown

import modules.text_display as text_display
import modules.drawer as drawer

class Fonts:
    back_box_font = pyg.font.SysFont("consolas", 20)
    settings_font = back_box_font
    menu_box_font = pyg.font.SysFont("consolas", 40)
    title_font = pyg.font.SysFont("consolas", 60)

buttons = []

# Loads the main menu scene
def load():
    global buttons
    # Store all of the menu's buttons
    buttons = [[
            MenuButton("New Game", (Globals.WIDTH/2, Globals.HEIGHT/2-60), (800, 80), Fonts.menu_box_font),
            MenuButton("Settings", (Globals.WIDTH/2, Globals.HEIGHT/2+60), (800, 80), Fonts.menu_box_font),
            MenuButton("Exit", (Globals.WIDTH/2, Globals.HEIGHT/2+180), (800, 80), Fonts.menu_box_font)],
        [
            MenuButton("New Game", (Globals.WIDTH/2, Globals.HEIGHT/2-120), (800, 80), Fonts.menu_box_font),
            MenuButton("Continue Game", (Globals.WIDTH/2, Globals.HEIGHT/2), (800, 80), Fonts.menu_box_font),
            MenuButton("Settings", (Globals.WIDTH/2, Globals.HEIGHT/2+120), (800, 80), Fonts.menu_box_font),
            MenuButton("Exit", (Globals.WIDTH/2, Globals.HEIGHT/2+240), (800, 80), Fonts.menu_box_font)],
        MenuButton("Back",(100, 50), (100, 50), Fonts.back_box_font)
    ]
    # Populate the sidebar menus
    for i in range(len(Globals.data["setting-menus"])):
        Globals.sidebar_buttons += [SidebarButton(Globals.data["setting-menus"][i], (100, 150 + i * 50), (0, 0), Fonts.settings_font)]

    # Populate the setting menus with check/dropboxes
    for menu in Globals.data["setting-items"]:
        temp_buttons = []
        # Loop through the menu's items
        for i in range(len(Globals.data["setting-items"][menu])):
            item = Globals.data["setting-items"][menu][i]

            # Item is a checkbox
            if item["type"] == "Checkbox":
                temp_buttons += [Checkbox(item["name"], (270, 150 + i * 40), (0, 0), Fonts.settings_font, item["value"])]
            # Item is a dropdown
            elif item["type"] == "Dropdown":
                temp_buttons += [Dropdown(item["name"], (270, 150 + i * 40), (0, 0), Fonts.settings_font, item["value"], item["active"], item["options"])]

        Globals.setting_buttons[menu] = temp_buttons

# Draws the main menu
def draw():
    global buttons
    WINDOW = Globals.WINDOW
    WIDTH, HEIGHT = Globals.WIDTH, Globals.HEIGHT

    Globals.VID_BUFFER.fill(Colors.BLACK)

    # Display settings menu
    if Globals.current_menu == "Settings": 
        buttons[2].draw()
        drawer.draw_settings()

    # Display main menu
    else:
        text_display.center_text("The Adventures of Sprite", Fonts.title_font, Colors.WHITE, (WIDTH/2, 100))

        # Menu buttons
        for button in buttons[Globals.data["game-exists"]]:
            button.draw()

    # Display image buffer to screen
    WINDOW.blit(pyg.transform.scale(Globals.VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), ((WIDTH - Globals.WINDOW_WIDTH)/2, (HEIGHT - Globals.WINDOW_HEIGHT)/2))
    pyg.display.update()

# Main menu control loop
def gameloop():    
    while True:
        # Save the current mouse positon
        Globals.mouse_position = pyg.mouse.get_pos()

        # Check for normal events
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                return "Quit"
            
            # Check for mouse click
            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                response = check_mouse_press()
                if response is not None:
                    return response
            
            # Check for key press
            elif event.type == pyg.KEYDOWN:
                if event.key == Keybinds.esc:
                    Globals.current_menu = "None"

                # Check quit keys
                elif event.key == pyg.K_F1:
                    return "Force Quit"
                
                elif event.key == pyg.K_F2:
                    return "Quit"

                # Check enter key
                elif event.key == Keybinds.enter and Globals.current_menu == "None":
                    if Globals.data["game-exists"]:
                        return "Continue Game"
                    else:
                        Globals.data["game-exists"] = 1
                        Globals.data["current-world"] = 1
                        Globals.data["world-times"] = [0, 0, 0, 0]
                        Globals.data["player-position"] = [0, 0]
                        return "New Game"
            
        draw()
        Globals.clock.tick(Globals.FPS)

# Checks what things were pressed
def check_mouse_press():
    global buttons

    # Check settings buttons
    if Globals.current_menu == "Settings":
        if buttons[2].check_mcollision():
            Globals.current_menu = "None"

        drawer.check_settings_mpress()
        return
        
    # Loop through the main menu buttons to check if they were clicked
    for button in buttons[Globals.data["game-exists"]]:
        if button.check_mcollision():
            # Check which button was clicked
            if button.text == "New Game":
                Globals.data["game-exists"] = 1
                Globals.data["current-world"] = 1
                Globals.data["world-times"] = [0, 0, 0, 0]
                return "New Game"
            
            elif button.text == "Continue Game":
                return "Continue Game"
            
            elif button.text == "Settings":
                Globals.current_menu = "Settings"
                
            elif button.text == "Exit":
                return "Exit"