import pygame as pyg
pyg.font.init()

# Import statements
from classes.globals import Globals

def center_text(text, font, color, location):
    width, height = font.size(text)
    Globals.VID_BUFFER.blit(font.render(text, True, color), ((location[0] - width/2), (location[1] - height/2)))

def left_text(text, font, color, location):
    _, height = font.size(text)
    Globals.VID_BUFFER.blit(font.render(text, True, color), ((location[0]), (location[1] - height/2)))
    
def upleft_text(text, font, color, location):
    Globals.VID_BUFFER.blit(font.render(text, True, color), location)