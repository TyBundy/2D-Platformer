# Import statements
import pygame as pyg
pyg.init()
pyg.font.init()

from classes.globals import Colors, Globals

class Platform:
    def __init__(self, location, size, id=0):
        self.x, self.y = location
        self.width, self.height = size
        self.type = "steel"
        self.id = id

        self.sprites = [pyg.image.load("resources/tiles/" + self.type + "/single.png")]

    def draw(self):
        font = pyg.font.SysFont("consolas", 20)

        total_x = self.width // 40
        total_y = self.height // 40
        for y in range(total_y):
            for x in range(total_x):
                Globals.VID_BUFFER.blit(self.sprites[0], (self.x + x * 40, Globals.HEIGHT - self.y - self.height + y * 40))
            
        # Index 0 == Show Tile IDs
        if Globals.setting_buttons["Debug"][0].value:
            text_width, text_height = font.size(str(self.id))
            Globals.VID_BUFFER.blit(font.render(str(self.id), True, Colors.WHITE), (self.x + (self.width - text_width)/2, Globals.HEIGHT - self.y - (self.height + text_height)/2))