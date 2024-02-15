# Import statements
from classes.globals import Colors, Globals
from classes.platform import Platform

class Level:

    def __init__(self):
        self.platforms = []

    def draw(self):
        # Background
        Globals.VID_BUFFER.fill(Colors.BLACK)
        
        for platform in self.platforms:
            platform.draw()
    