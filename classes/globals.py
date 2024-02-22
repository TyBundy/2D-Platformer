import pygame as pyg
pyg.font.init()

# Just colors

class Colors:
    BLACK = (25, 25, 25)
    LIGHT_GRAY = (100, 100, 100)
    MEDIUM_GRAY = (70, 70, 70)
    DARK_GRAY = (40, 40, 40)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)

class Keybinds:
    # Movement keys
    left = pyg.K_a
    left_alt = pyg.K_LEFT
    right = pyg.K_d
    right_alt = pyg.K_RIGHT
    jump = pyg.K_SPACE
    jump_alt = pyg.K_w
    walk = pyg.K_LCTRL
    walk_alt = pyg.K_RCTRL
    duck = pyg.K_s
    duck_alt = pyg.K_DOWN
    respawn = pyg.K_BACKSPACE

    # Control keys
    esc = pyg.K_ESCAPE
    enter = pyg.K_RETURN

class Settings:
    SETTING_MENUS = []

    SETTING_ITEMS = {}

x = None
# +-------- Constants --------+
# Window:           The current pygame window
# WIDTH, HEIGHT:    The width and height of the active screen
# VID_BUFFER:       A buffer image that gets drawn to the actual window, allows resolution scaling
# Player_speed:     The speed at which the player moves
# Gravity:          The constant gravity value
# Max_fall_speed:   The maximum speed at which the player falls
# Jump_force:       The force of a player jump
# Frictions:        A dictionary of the different friction forces
# FPS:              The maximum frames per second
# Clock:            Pygame clock object
# +---------------------------+
# +-------- Variables --------+
# Current_time:     The current time from time.time()
# Player:           Player object
# Level:            Current level object
# Current_scene:    The currently active scene
# Current menu:     The current menu that is open
# Current_setting:  The current setting that is open
# +---------------------------+
    
class Globals:
    WINDOW = None
    WIDTH, HEIGHT = 0, 0
    WINDOW_WIDTH, WINDOW_HEIGHT = 0, 0

    frictions = {
        "normal": 1.5
    }

    player_speed = 7
    jump_force = 13
    max_fall_speed = 20
    gravity = 0.5

    FPS = 60
    current_framerate = 0
    current_time = 0
    clock = pyg.time.Clock()
    VID_BUFFER = pyg.Surface((1920, 1080))
    PLATFORM_BUFFER = pyg.Surface((1920, 1080))
    reset_pos = [0, 0]
    mouse_position = [0,0]
    previous_frames = []
    sidebar_buttons = []
    setting_buttons = {}

    data = {}
    level_data = {}

    player = None
    level = None
    current_scene = None
    current_menu = "None"
    current_setting = "Game"

    settings_background = Colors.BLACK

