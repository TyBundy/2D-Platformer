# Import statements
import pygame as pyg
pyg.init()
pyg.font.init()

# Custom modules
from classes.globals import Colors, Globals, Keybinds

import modules.text_display as text_display
import modules.collider as collider
import modules.drawer as drawer

class Fonts:
    back_box_font = pyg.font.SysFont("consolas", 20)
    sidebar_font = pyg.font.SysFont("consolas", 30)
    menu_box_font = pyg.font.SysFont("consolas", 40)
    title_font = pyg.font.SysFont("consolas", 60)


# Loads the main menu scene
def load():
    pass


def draw():
    WINDOW = Globals.WINDOW
    WIDTH, HEIGHT = Globals.WIDTH, Globals.HEIGHT

    Globals.VID_BUFFER.fill(Colors.BLACK)

    # Display settings menu
    if Globals.current_menu == "Settings": 
        Draw_Button("Back", (100, 50), (100, 50), Fonts.back_box_font)

        drawer.draw_settings()

    # Display main menu
    else:
        text_display.center_text("2D Platformer Game", Fonts.title_font, Colors.WHITE, (WIDTH/2, 100))

        # Menu buttons
        if Globals.data["game-exists"]:
            Draw_Button("New Game", (WIDTH/2, HEIGHT/2-120), (800, 80))
            Draw_Button("Continue Game", (WIDTH/2, HEIGHT/2), (800, 80))
            Draw_Button("Settings", (WIDTH/2, HEIGHT/2+120), (800, 80))
            Draw_Button("Exit", (WIDTH/2, HEIGHT/2+240), (800, 80))
        else:
            Draw_Button("New Game", (WIDTH/2, HEIGHT/2-60), (800, 80))
            Draw_Button("Settings", (WIDTH/2, HEIGHT/2+60), (800, 80))
            Draw_Button("Exit", (WIDTH/2, HEIGHT/2+180), (800, 80))


    WINDOW.blit(pyg.transform.scale(Globals.VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), ((WIDTH - Globals.WINDOW_WIDTH)/2, (HEIGHT - Globals.WINDOW_HEIGHT)/2))
    pyg.display.update()

# Main menu control loop
def gameloop():    
    while True:
        # Check for normal events
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                return "Quit"
            
            # Check for mouse click
            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                response = check_mouse_press()
                if response is not None:
                    return response
            
            elif event.type == pyg.KEYDOWN:
                if event.key == Keybinds.esc:
                    Globals.current_menu = "None"

                elif event.key == Keybinds.enter and Globals.current_menu == "None":
                    if Globals.data["game-exists"]:
                        return "Continue Game"
                    else:
                        return "New Game"
            
        # Save the current mouse positon and get the current keys pressed
        Globals.mouse_position = pyg.mouse.get_pos()
        keys = pyg.key.get_pressed()        

        # Check kill button
        if keys[pyg.K_F1]:
            return "Force Quit"

        draw()

        Globals.clock.tick(Globals.FPS)

# Checks what things were pressed
def check_mouse_press():
    # Check settings buttons
    if Globals.current_menu == "Settings":
        if Check_Button((100, 50), (80, 30)):
            Globals.current_menu = "None"

        drawer.check_settings_mpress()
        
    # Check main menu buttons
    else:
        # Four buttons if a game exists
        if Globals.data["game-exists"]:
            if Check_Button((Globals.WINDOW_WIDTH/2, Globals.WINDOW_HEIGHT/2-120), (800, 80)):
                Globals.data["game-exists"] = 1
                Globals.data["current-world"] = 1
                return "New Game"
            
            if Check_Button((Globals.WINDOW_WIDTH/2, Globals.WINDOW_HEIGHT/2), (800, 80)):
                return "Continue Game"

            elif Check_Button((Globals.WINDOW_WIDTH/2, Globals.WINDOW_HEIGHT/2+120), (800, 80)):
                Globals.current_menu = "Settings"
                
            elif Check_Button((Globals.WINDOW_WIDTH/2, Globals.WINDOW_HEIGHT/2+240), (800, 80)):
                return "Exit"
            
        # Three otherwise (no "continue game" option)
        else:
            if Check_Button((Globals.WINDOW_WIDTH/2, Globals.WINDOW_HEIGHT/2-60), (800, 80)):
                Globals.data["game-exists"] = 1
                Globals.data["current-world"] = 1
                return "New Game"
                
            elif Check_Button((Globals.WINDOW_WIDTH/2, Globals.WINDOW_HEIGHT/2+60), (800, 80)):
                Globals.current_menu = "Settings"
                
            elif Check_Button((Globals.WINDOW_WIDTH/2, Globals.WINDOW_HEIGHT/2+180), (800, 80)):
                return "Exit"

# Checks if a mouse click happened on the given button
def Check_Button(location, size):
    return collider.collides_rect((location[0] - size[0]/2 + 2, location[1] - size[1]/2 + 2, size[0], size[1]), Globals.mouse_position)

# Draws the menu buttons
def Draw_Button(text, location, size, font=Fonts.menu_box_font):
    if collider.collides_rect((location[0] - size[0]/2 + 2, location[1] - size[1]/2 + 2, size[0], size[1]), Globals.mouse_position):
        size = [size[i] * 1.1 for i in range(len(size))]

    pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (location[0] - size[0]/2 + 2, location[1] - size[1]/2 + 2, size[0], size[1]), border_radius=10)
    pyg.draw.rect(Globals.VID_BUFFER, Colors.DARK_GRAY, (location[0] - size[0]/2, location[1] - size[1]/2, size[0], size[1]), border_radius=10)

    text_display.center_text(text, font, Colors.WHITE, (location[0], location[1]))