# Import statements
import pygame as pyg
import time

# Custom modules
from classes.globals import Colors, Globals, Keybinds, Settings
from classes.level import Level
from classes.platform import Platform
from scripts.player_script import Player

import modules.drawer as drawer

# Local classes
class Fonts:
    fps_font = pyg.font.SysFont("consolas", 20)
    timer_font = pyg.font.SysFont("consolas", 24)

settings_toggled = False
settings_animate_period = 0
settings_delay = 15

# Loads the current world
def load():
    # Set up level
    Globals.level = Level()
    Globals.reset_pos = (160, 40)
    Globals.settings_background = Colors.DARK_GRAY

    # Set up player
    Globals.player = Player(Globals.reset_pos)
    load_level(0)

def load_level(level_id):
    temp_level = Level()
    current_level = Globals.level_data["world-1"][level_id]
    for i in range(len(current_level["platforms"])):
        platform = current_level["platforms"][i]
        temp_level.platforms += [Platform((platform[0], platform[1]), (platform[2], platform[3]), i)]
    Globals.level = temp_level


def gameloop():
    global settings_toggled, settings_animate_period

    frame_counter = 0

    while True:
        if frame_counter == 60:
            frame_counter = 0
            Globals.data["world-times"][Globals.data["current-world"]-1] += 1
        Globals.current_time = time.time()

        # Save the current mouse positon and get the current keys pressed
        Globals.mouse_position = pyg.mouse.get_pos()
        keys = pyg.key.get_pressed()    

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                return "Quit"
            
            elif event.type == pyg.KEYDOWN:
                if event.key == Keybinds.jump or event.key == Keybinds.jump_alt:
                    Globals.player.jump()

                elif event.key == Keybinds.esc:
                    settings_toggled = not settings_toggled
                    settings_animate_period = settings_delay

            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                response = drawer.check_settings_mpress(True)
                if response == "Quit":
                    settings_toggled = False
                    Globals.current_menu = "None"
                    return "Main Menu"
                

        # Check kill/exit buttons
        if keys[pyg.K_F1]:
            return "Force Quit"
        elif keys[pyg.K_F2]:
            settings_toggled = False
            Globals.current_menu = "None"
            return "Main Menu"
        
        # Player movement
        Globals.player.holding_left = False
        Globals.player.holding_right = False

        if keys[Keybinds.left] or keys[Keybinds.left_alt]:
            Globals.player.move(-1)
            Globals.player.holding_left = True
        if keys[Keybinds.right] or keys[Keybinds.right_alt]:
            Globals.player.move(1)
            Globals.player.holding_right = True

        # Adding frames to the frame buffer
        Globals.previous_frames += [time.time()]
        if len(Globals.previous_frames) > 60:
            Globals.previous_frames.pop(0)

        # Update player/level stuff
        Globals.player.wall_jump_delay = max(0, Globals.player.wall_jump_delay-1)
        Globals.player.coyotee_timer = max(0, Globals.player.coyotee_timer-1)
        Globals.player.update(Globals.level)

        Globals.level.draw()
        draw()
        
        settings_animate_period = max(0, settings_animate_period - 1)

        # Tick tock
        Globals.clock.tick(Globals.FPS)
        frame_counter += 1

# Draws stuff to screen
def draw():
    global settings_toggled, settings_animate_period

    # Copy to local variables (makes it cleaner)
    WINDOW = Globals.WINDOW
    WIDTH, HEIGHT = Globals.WIDTH, Globals.HEIGHT

    # Draw player
    Globals.player.draw()

    # Draw fps
    # Index 0 == Display FPS
    if Settings.SETTING_ITEMS["Display"][0]["value"]:
        fps = 0
        try:
            temp_frame_list = []
            for i in range(len(Globals.previous_frames)-1):
                temp_frame_list += [Globals.previous_frames[i+1] - Globals.previous_frames[i]]
            for frame in temp_frame_list:
                fps += 1/frame
            fps += Globals.current_time - Globals.previous_frames[-1]
            fps = round(fps / (len(temp_frame_list) + 1))
        except:
            pass
        text_width, _ = Fonts.fps_font.size(str(fps))
        Globals.VID_BUFFER.blit(Fonts.fps_font.render(str(fps), True, Colors.WHITE), (WIDTH - text_width - 2, 2))

    # Get timer
    # Index 0 == Display timer
    if Settings.SETTING_ITEMS["Game"][0]["value"] == "World Time":
        timer = Globals.data["world-times"][Globals.data["current-world"]-1]

    elif Settings.SETTING_ITEMS["Game"][0]["value"] == "Game Time":
        timer = 0
        for val in Globals.data["world-times"]:
            timer += val

    # Draw timer
    if Settings.SETTING_ITEMS["Game"][0]["value"] != "None":
        timer_parts = [str(timer // 3600), str(timer // 60), str(timer % 60)]
        timer_parts = [("0" if len(timer_parts[i]) == 1 else "") + timer_parts[i] for i in range(len(timer_parts))]
        timer_text = ":".join(timer_parts)

        text_width, text_height = Fonts.timer_font.size(timer_text)
        pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (4, 4, text_width + 4, text_height + 4))
        pyg.draw.rect(Globals.VID_BUFFER, Colors.BLACK, (5, 5, text_width + 2, text_height + 2))
        Globals.VID_BUFFER.blit(Fonts.timer_font.render(timer_text, True, Colors.WHITE), (6, 6))

    # Draw settings menu, if active
    if settings_animate_period or settings_toggled:
        if settings_toggled:
            pyg.draw.rect(Globals.VID_BUFFER, Colors.DARK_GRAY, (0, 0, Globals.WIDTH, Globals.HEIGHT / settings_delay * (settings_delay - settings_animate_period)))
            if settings_animate_period == 0:
                drawer.draw_settings(True)

        else:
            pyg.draw.rect(Globals.VID_BUFFER, Colors.DARK_GRAY, (0, 0, Globals.WIDTH, Globals.HEIGHT - Globals.HEIGHT / settings_delay * (settings_delay - settings_animate_period)))

    WINDOW.blit(pyg.transform.scale(Globals.VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), ((WIDTH - Globals.WINDOW_WIDTH)/2, (HEIGHT - Globals.WINDOW_HEIGHT)/2))
    pyg.display.update()