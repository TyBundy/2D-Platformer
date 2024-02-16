# Import statements
import pygame as pyg
pyg.init()

# Custom modules
from classes.globals import Globals
from classes.level import Level
from scripts.entity_script import Entity
import modules.collider as collider

class Player(Entity):
    """Player entity, which the user controls"""
    
    def __init__(self, pos):
        # Call the base class' constructor
        super(Player, self).__init__(pos)
        self.width, self.height = 50, 80
        self.wall_jump_delay = 0
        self.speed = 0
        self.kickback = 0
        self.coyotee_timer = 0
        self.respawn_timer = 0

        self.facing = "Right"
        self.type = "player"
        self.holding_right = False
        self.holding_left = False
        self.floored = False
        self.jumping = False
        self.is_sliding = False

        self.idle_sprites = [pyg.image.load("resources/" + self.type + "/idle0.png")]
        self.blank_sprite = pyg.image.load("resources/blank.png")

    def move(self, direction):
        """Moves left to right based on the direction"""
        self.speed = direction * Globals.player_speed * (0.1 if self.jumping else 1)
        self.velocity[0] += self.speed
        if self.velocity[0] >= 0:
            self.facing = "Right"
            self.velocity[0] = min(self.velocity[0], Globals.player_speed)
        else:
            self.facing = "Left"
            self.velocity[0] = max(self.velocity[0], -Globals.player_speed)

        self.velocity[0] += self.kickback

    def jump(self):
        """Makes the player wall/jump"""
        if not self.jumping and (self.floored or self.coyotee_timer):
            self.velocity[1] += Globals.jump_force
            
        elif (self.can_wall_jump == "Right" and self.holding_right and self.wall_jump_delay == 0):
            self.velocity[1] = max(self.velocity[1], Globals.jump_force)
            self.wall_jump_delay = 10
            self.kickback = -Globals.player_speed / 2.5
        
        elif (self.can_wall_jump == "Left" and self.holding_left and self.wall_jump_delay == 0):
            self.velocity[1] = max(self.velocity[1], Globals.jump_force)
            self.wall_jump_delay = 10
            self.kickback = Globals.player_speed / 2.5

        self.jumping = True

    def resolve_collisions(self, level: Level=None):
        """Resolves collisions between the player and the platforms in the level"""
        self.can_wall_jump = "None"
        self.is_sliding = False
        self.floored = False

        for platform in level.platforms:
            collision = collider.collides_platform(self, platform)
            if collision:
                # Moving right
                if collision[0] == -1:
                    self.is_sliding = True
                    self.velocity[0] = 0
                    self.x = platform.x - self.width - 0.1
                    self.can_wall_jump = "Right"
                    
                # Moving left
                elif collision[0] == 1:
                    self.is_sliding = True
                    self.velocity[0] = 0
                    self.x = platform.x + platform.width
                    self.can_wall_jump = "Left"
                    
                # Falling
                if collision[1] == -1:
                    self.velocity[1] = 0
                    self.y = platform.y + platform.height
                    self.jumping = False
                    self.floored = True
                    self.wall_jump_delay = 0
                    self.coyotee_timer = 6

                # Ceiling bonk
                elif collision[1] == 1:
                    self.velocity[1] = 0
                    self.y = platform.y - self.height - 0.1

                    
    def update(self, level):
        """Updates the player based on its velocity"""
        self.respawn_timer = max(0, self.respawn_timer-1)
        self.wall_jump_delay = max(0, self.wall_jump_delay-1)
        self.coyotee_timer = max(0, self.coyotee_timer-1)

        if self.respawn_timer > 40:
            self.velocity = [0, 0]
            return

        # Update the position
        self.x += self.velocity[0]
        self.x = min(max(self.x, 0), Globals.WIDTH - self.width)
        self.y += self.velocity[1]

        # Check and resolve platform collisions
        if level is not None:
            self.resolve_collisions(level)

        self.velocity[1] -= Globals.gravity * (0.2 if self.is_sliding and (self.velocity[1] < 0) else 1)

        # Apply sliding friction
        if self.velocity[1] < 0:
            if self.is_sliding:
                self.velocity[1] = max(-4, self.velocity[1])
            self.velocity[1] = max(-Globals.max_fall_speed, self.velocity[1])
            

        # Apply friction
        self.speed /= Globals.frictions["normal"] if not self.jumping else 1.1
        self.velocity[0] /= Globals.frictions["normal"] if not self.jumping else 1.1
        self.kickback /= Globals.frictions["normal"] if not self.jumping else 1.1

        # Die when falling off screen
        if self.y < 0 - self.height - 50:
            self.killed()

    def killed(self):
        """Runs the respawn animation and sounds relating to death"""
        self.respawn_timer = 80
        self.x, self.y = Globals.reset_pos


    def draw(self):
        """Draws the player sprite"""
        current_sprite = pyg.transform.scale(self.idle_sprites[0], (50, 80))
        if 0 < self.respawn_timer <= 8 or 16 < self.respawn_timer <= 24 or 30 < self.respawn_timer <= 38 or 46 < self.respawn_timer <= 80:
            current_sprite = self.blank_sprite
        
        Globals.VID_BUFFER.blit(pyg.transform.flip(current_sprite, self.facing == "Left", False), (self.x, Globals.HEIGHT - self.y - self.height, self.width, self.height))
