# Import statements
import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg
import json
import os

# Custom modules
from classes.globals import Globals, Settings

# Scenes
import scenes.main_menu as main_menu
import scenes.world_1 as world_1

worlds = [
    world_1
]

# Main function, runs on program start
def Main():
    os.system("cls")

    # Set up display
    pyg.init()
    info_object = pyg.display.Info()
    Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT = info_object.current_w, info_object.current_h
    Globals.WIDTH, Globals.HEIGHT = (1920, 1080)
    Globals.WINDOW = pyg.display.set_mode((Globals.WIDTH, Globals.HEIGHT))
    pyg.display.set_caption("2D Platformer (Def not final title)")


    # Set up data
    try:
        Globals.data = json.load(open("data/player_data.json", "r"))
    except FileNotFoundError:
        Globals.data = json.load(open("data/default_data.json", "r"))
    Globals.level_data = json.load(open("data/level_data.json", "r"))
    Settings.SETTING_ITEMS = Globals.data["setting-items"]
    Settings.SETTING_MENUS = Globals.data["setting-menus"]

    # Set up scenes
    Globals.current_scene = main_menu
    Globals.current_scene.load()

    return_val = Globals.current_scene.gameloop()
    while True:
        Globals.current_setting = "Game"
        # Exit with saving
        if return_val == "Force Quit":
            return
        
        # Exit the game
        elif return_val in ["Quit", "Exit"]:
            with open("data/player_data.json", "w") as outfile:
                outfile.write(json.dumps(Globals.data, indent=4))
            return
        
        # Go back to the main menu
        elif return_val == "Main Menu":
            Globals.current_scene = main_menu
            Globals.current_scene.load()
            return_val = Globals.current_scene.gameloop()

        # Start playing
        elif return_val in ["New Game", "Continue Game"]:
            Globals.current_scene = worlds[Globals.data["current-world"] - 1]
            Globals.current_scene.load()
            return_val = Globals.current_scene.gameloop()

if __name__ == "__main__":
    Main()