# Import statements
from classes.globals import Colors, Globals
from classes.platform import Platform

class Level:

    def __init__(self):
        self.platforms = []
        self.objects = []

    def draw(self, draw_platforms=True):
        # Background
        Globals.VID_BUFFER.fill(Colors.BLACK)
        
        for platform in self.platforms:
            platform.draw()

        for object in self.objects:
            object.draw()
    