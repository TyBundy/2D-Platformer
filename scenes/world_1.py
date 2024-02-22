# Import statements
import pygame as pyg
import time

# Custom modules
from classes.globals import Colors, Globals, Keybinds
from classes.level import Level
from classes.platform import Platform
from classes.collectable import Goal
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
    load_level(Globals.data["current-level"])
    Globals.settings_background = Colors.DARK_GRAY

    # Set up player
    pos = Globals.reset_pos
    if Globals.data["player-position"] != [0, 0]:
        pos = Globals.data["player-position"]
    Globals.player = Player(pos)

# Loads a level based on the current world and the id passed in
def load_level(level_id):
    temp_level = Level()
    current_level = Globals.level_data["world-" + str(Globals.data["current-world"] + 1)][level_id]

    # Load platforms/objects from the level data
    for i in range(len(current_level["platforms"])):
        platform = current_level["platforms"][i]
        type = platform[4]

        if type == "flag":
            temp_level.objects += [Goal((platform[0], platform[1]), (platform[2], platform[3]), i, type)]
        else:
            temp_level.platforms += [Platform((platform[0], platform[1]), (platform[2], platform[3]), i, type)]

    Globals.level = temp_level
    Globals.reset_pos = current_level["reset-position"]

def gameloop():
    global settings_toggled, settings_animate_period
    frame_counter = 0

    while True:
        # Update the timer for the world/level that you're in
        if frame_counter == Globals.FPS:
            frame_counter = 0
            if not settings_toggled:
                Globals.data["world-times"][Globals.data["current-world"]][Globals.data["current-level"]] += 1

        Globals.current_time = time.time()

        # Save the current mouse positon and get the current keys pressed
        Globals.mouse_position = pyg.mouse.get_pos()
        keys = pyg.key.get_pressed()    

        events = pyg.event.get()
        for event in events:
            if event.type == pyg.QUIT:
                return "Quit"
            
            elif event.type == pyg.KEYDOWN:
                if event.key == Keybinds.jump or event.key == Keybinds.jump_alt:
                    Globals.player.jump()

                # Kill keys
                elif event.key == pyg.K_F1:
                    return "Force Quit"
                elif event.key == pyg.K_F2:
                    settings_toggled = False
                    Globals.current_menu = "None"
                    return "Main Menu"

                # Open/close settings
                elif event.key == Keybinds.esc:
                    settings_toggled = not settings_toggled
                    settings_animate_period = settings_delay

                # Respawn player
                elif event.key == Keybinds.respawn:
                    Globals.player.killed()

                # For debugging only
                elif event.key == pyg.K_EQUALS:
                    Globals.data["current-level"] += 1
                    # Set level to 0 if it's the last level
                    if Globals.data["current-level"] == len(Globals.level_data["world-" + str(Globals.data["current-world"] + 1)]):
                        Globals.data["current-level"] = 0
                    load_level(Globals.data["current-level"])
                    Globals.player.x, Globals.player.y = Globals.reset_pos


            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                response = drawer.check_settings_mpress(True)
                if response == "Quit":
                    settings_toggled = False
                    Globals.current_menu = "None"
                    return "Main Menu"
        
        # Player movement
        Globals.player.holding_left = False
        Globals.player.holding_right = False
        Globals.player.walking = False
        Globals.player.ducking = False

        if keys[Keybinds.left] or keys[Keybinds.left_alt]:
            Globals.player.move(-1)
            Globals.player.holding_left = True
        if keys[Keybinds.right] or keys[Keybinds.right_alt]:
            Globals.player.move(1)
            Globals.player.holding_right = True
        if keys[Keybinds.duck] or keys[Keybinds.duck_alt]:
            Globals.player.ducking = True
        if keys[Keybinds.walk] or keys[Keybinds.walk_alt]:
            Globals.player.walking = True

        # Adding frames to the frame buffer
        Globals.previous_frames += [time.time()]
        if len(Globals.previous_frames) > Globals.FPS:
            Globals.previous_frames.pop(0)

        # Update player/level stuff
        val = Globals.player.update(Globals.level)
        # If player touched the flag, increment level
        if val == "flag":
            Globals.data["current-level"] += 1
            # Set level to 0 if it's the last level
            if Globals.data["current-level"] == len(Globals.level_data["world-" + str(Globals.data["current-world"] + 1)]):
                Globals.data["current-level"] = 0
            load_level(Globals.data["current-level"])
            Globals.player.x, Globals.player.y = Globals.reset_pos
            Globals.player.pause_timer = 15

        Globals.data["player-position"] = [Globals.player.x, Globals.player.y]

        Globals.level.draw(False)
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
    if Globals.setting_buttons["Display"][0].value:
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
        Globals.current_framerate = fps
        text_width, _ = Fonts.fps_font.size(str(fps))
        Globals.VID_BUFFER.blit(Fonts.fps_font.render(str(fps), True, Colors.WHITE), (WIDTH - text_width - 2, 2))

    # Get timer
    if Globals.setting_buttons["Game"][0].value == "World Time":
        timer = 0
        for val in Globals.data["world-times"][Globals.data["current-world"]]:
            timer += val        

    elif Globals.setting_buttons["Game"][0].value == "Game Time":
        timer = 0
        for world in Globals.data["world-times"]:
            for val in world:
                timer += val

    # Draw timer
    if Globals.setting_buttons["Game"][0].value != "None":
        timer_parts = [str(timer // 3600), str(timer // 60 % 60), str(timer % 60)]
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
                drawer.draw_settings(quit=True)
        else:
            pyg.draw.rect(Globals.VID_BUFFER, Colors.DARK_GRAY, (0, 0, Globals.WIDTH, Globals.HEIGHT - Globals.HEIGHT / settings_delay * (settings_delay - settings_animate_period)))

    WINDOW.blit(pyg.transform.scale(Globals.VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), ((WIDTH - Globals.WINDOW_WIDTH)/2, (HEIGHT - Globals.WINDOW_HEIGHT)/2))
    pyg.display.update()