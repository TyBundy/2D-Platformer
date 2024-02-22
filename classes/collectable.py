import pygame as pyg
pyg.init()

from classes.globals import Globals, Colors

class Goal:
    def __init__(self, location, size, id, type):
        self.x, self.y = location
        self.width, self.height = size
        self.type = type
        self.id = id

        self.sprites = [pyg.image.load("resources/tiles/" + self.type + "/flag0.png")]

    def draw(self):
        font = pyg.font.SysFont("consolas", 20)

        Globals.VID_BUFFER.blit(self.sprites[0], (self.x, Globals.HEIGHT - self.y - 50))
            
        # Index 0 == Show Tile IDs
        if Globals.setting_buttons["Debug"][0].value:
            Globals.VID_BUFFER.blit(font.render(str(self.id), True, Colors.WHITE), (self.x + 8, Globals.HEIGHT - self.y - 25))