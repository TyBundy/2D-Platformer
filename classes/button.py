import pygame as pyg
pyg.init()
pyg.font.init()

from classes.globals import Colors
from classes.globals import Globals

import modules.collider as collider
import modules.text_display as text_display

class Button:
    def __init__(self, text, pos, size, font):
        self.x, self.y = pos
        self.width, self.height = size
        self.text = text
        self.font = font

class MenuButton(Button):
    def __init__(self, text, pos, size, font):
        super().__init__(text, pos, size, font)
        self.type = "MenuButton"

    def draw(self):
        """Draws the button"""
        size = [self.width, self.height]
        if self.check_mcollision():
            size = [size[i] * 1.1 for i in range(len(size))]

        pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (self.x - size[0]/2 + 2, self.y - size[1]/2 + 2, size[0], size[1]), border_radius=10)
        pyg.draw.rect(Globals.VID_BUFFER, Colors.DARK_GRAY, (self.x - size[0]/2, self.y - size[1]/2, size[0], size[1]), border_radius=10)

        text_display.center_text(self.text, self.font, Colors.WHITE, (self.x, self.y))

    def check_mcollision(self):
        """Checks if the button was clicked"""
        # Adjust the position and size based on the actual screen size
        adjust_x, adjust_y = self.x * (Globals.WINDOW_WIDTH / Globals.WIDTH), self.y * (Globals.WINDOW_HEIGHT / Globals.HEIGHT)
        adjust_width, adjust_height = self.width * (Globals.WINDOW_WIDTH / Globals.WIDTH), self.height * (Globals.WINDOW_HEIGHT / Globals.HEIGHT)

        return collider.collides_rect((adjust_x - adjust_width/2 + 2, adjust_y - adjust_height/2 + 2, adjust_width, adjust_height), Globals.mouse_position)
    
class SidebarButton(Button):
    def __init__(self, text, pos, size, font):
        super().__init__(text, pos, size, font)
        self.type = "SidebarButton"

    def draw(self):
        """Draws the button"""
        text_width, text_height = self.font.size(self.text)
    
        # Check mouse collision
        if collider.collides_rect((self.x - 10, self.y - text_height/2 - 5, text_width + 20, 35), Globals.mouse_position):
            pyg.draw.rect(Globals.VID_BUFFER, Colors.MEDIUM_GRAY, (self.x, self.y + text_height/2, text_width, 2))

        # Check if it's the active setting
        if self.text == Globals.current_setting:
            pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (self.x, self.y + text_height/2, text_width, 2))
        
        text_display.left_text(self.text, self.font, Colors.WHITE, (self.x, self.y))

    def check_mcollision(self):
        """Checks if the button was clicked"""
        # Adjust the position and size based on the actual screen size
        text_width, text_height = self.font.size(self.text)
        adjust_x, adjust_y = self.x * (Globals.WINDOW_WIDTH / Globals.WIDTH), self.y * (Globals.WINDOW_HEIGHT / Globals.HEIGHT)
        text_width, text_height = text_width * (Globals.WINDOW_WIDTH / Globals.WIDTH), text_height * (Globals.WINDOW_HEIGHT / Globals.HEIGHT)

        return collider.collides_rect((adjust_x - 10, adjust_y - text_height/2 - 5, text_width + 20, 35), Globals.mouse_position)
    
class Checkbox(Button):
    def __init__(self, text, pos, size, font, value):
        super().__init__(text, pos, size, font)
        self.value = value
        self.type = "Checkbox"

    def draw(self):
        """Draw the checkbox"""
        text_width, text_height = self.font.size(self.text)

        text_display.left_text(self.text, self.font, Colors.WHITE, (self.x, self.y))

        pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (self.x + text_width + 20, self.y - 11, 20, 20))
        pyg.draw.rect(Globals.VID_BUFFER, Colors.GREEN if self.value else Colors.DARK_GRAY, (self.x + text_width + 21, self.y - 10, 18, 18))
        
    # Checks if a checkbox was clicked
    def check_mcollision(self):
        """Check if the checkbox was clicked"""
        text_width, _ = self.font.size(self.text)
        adjust_x, adjust_y = self.x * (Globals.WINDOW_WIDTH / Globals.WIDTH), self.y * (Globals.WINDOW_HEIGHT / Globals.HEIGHT)
        text_width *= (Globals.WINDOW_WIDTH / Globals.WIDTH)

        return collider.collides_rect((adjust_x + text_width + 20, adjust_y - 11, 20, 20), Globals.mouse_position)
    
class Dropdown(Button):
    def __init__(self, text, pos, size, font, value, active, options):
        super().__init__(text, pos, size, font)
        self.value = value
        self.active = active
        self.options = options
        self.type = "Dropdown"

    def draw(self):
        """Draws the dropdown while inactive"""
        text_width, _ = self.font.size(self.text)

        text_display.left_text(self.text, self.font, Colors.WHITE, (self.x, self.y))

        active_option = self.value
        active_width, active_height = self.font.size(active_option)

        # Draw text box
        pyg.draw.rect(Globals.VID_BUFFER, Globals.settings_background, (self.x + text_width + 22, self.y - active_height/2 - 2, active_width + 24, active_height * len(self.options) + 4))
        pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (self.x + text_width + 20, self.y - active_height/2 - 2, active_width + 24, active_height + 4))
        pyg.draw.rect(Globals.VID_BUFFER, Colors.DARK_GRAY, (self.x + text_width + 22, self.y - active_height/2, active_width + 20, active_height))
        text_display.left_text(active_option, self.font, Colors.WHITE, (self.x + text_width + 24, self.y))

        # Draw dropdown arrow
        pyg.draw.line(Globals.VID_BUFFER, Colors.WHITE, (self.x + text_width + active_width + 30, self.y - 4), (self.x + text_width + active_width + 34, self.y + 4))
        pyg.draw.line(Globals.VID_BUFFER, Colors.WHITE, (self.x + text_width + active_width + 38, self.y - 4), (self.x + text_width + active_width + 34, self.y + 4))
        
    def check_mcollision(self):
        """Checks if the inactive dropdown was clicked"""
        text_width, _ = self.font.size(self.text)
    
        active_option = self.value
        active_width, active_height = self.font.size(active_option)
        
        adjust_x, adjust_y = self.x * (Globals.WINDOW_WIDTH / Globals.WIDTH), self.y * (Globals.WINDOW_HEIGHT / Globals.HEIGHT)
        text_width *= (Globals.WINDOW_WIDTH / Globals.WIDTH)
        active_width, active_height = active_width * (Globals.WINDOW_WIDTH / Globals.WIDTH), active_height * (Globals.WINDOW_HEIGHT / Globals.HEIGHT)

        return collider.collides_rect((adjust_x + text_width + 20, adjust_y - active_height/2 - 2, active_width + 24, active_height + 4), Globals.mouse_position)
    
    def draw_active(self):
        """Draws the dropdown while active (the different options)"""
        text_width, _ = self.font.size(self.text)

        text_display.left_text(self.text, self.font, Colors.WHITE, (self.x, self.y))

        num_options = len(self.options)
        active_width = 0

        for i in range(num_options):
            option = self.options[i]
            temp_w, active_height = self.font.size(option)
            if active_width < temp_w:
                active_width = temp_w

        # Draw text box
        pyg.draw.rect(Globals.VID_BUFFER, Globals.settings_background, (self.x + text_width + 22, self.y - active_height/2 - 2, active_width + 24, active_height + 4))
        pyg.draw.rect(Globals.VID_BUFFER, Colors.LIGHT_GRAY, (self.x + text_width + 20, self.y - active_height/2 - 2, active_width + 8, 4 + (active_height * num_options)))
        pyg.draw.rect(Globals.VID_BUFFER, Colors.DARK_GRAY, (self.x + text_width + 22, self.y - active_height/2, active_width + 4, (active_height * num_options)))

        for i in range(num_options):
            active_option = self.options[i]
            text_display.left_text(active_option, self.font, Colors.WHITE, (self.x + text_width + 24, self.y + active_height * i))

    def check_active(self):
        """Checks what option was clicked, while active"""
        text_width, _ = self.font.size(self.text)
    
        num_options = len(self.options)
        active_width = 0

        adjust_x, adjust_y = self.x * (Globals.WINDOW_WIDTH / Globals.WIDTH), self.y * (Globals.WINDOW_HEIGHT / Globals.HEIGHT)
        text_width *= (Globals.WINDOW_WIDTH / Globals.WIDTH)

        for i in range(num_options):
            option = self.options[i]
            temp_w, active_height = self.font.size(option)
            if active_width < temp_w:
                active_width = temp_w
        
        active_width, active_height = active_width * (Globals.WINDOW_WIDTH / Globals.WIDTH), active_height * (Globals.WINDOW_HEIGHT / Globals.HEIGHT)
        for i in range(num_options):
            if collider.collides_rect((adjust_x + text_width + 24, adjust_y - active_height/2-2 + active_height * i, active_width + 24, active_height + 4), Globals.mouse_position):
                return i