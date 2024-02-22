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
        self.frame_counter = 0
        self.fall_counter = 0
        self.ducking_timer = 0
        self.dissolve_timer = 0
        self.jump_timer = 0
        self.pause_timer = 0

        self.facing = "Right"
        self.type = "player"
        self.holding_right = False
        self.holding_left = False
        self.floored = False
        self.jumping = False
        self.is_sliding = False
        self.walking = False
        self.ducking = False
        self.load_sprites()

    def load_sprites(self):
        """Loads the player's sprites"""
        self.idle_sprites = {
            "period": 100,
            "0": pyg.image.load("resources/" + self.type + "/idle/idle0.png"),
            "25": pyg.image.load("resources/" + self.type + "/idle/idle1.png"),
            "50": pyg.image.load("resources/" + self.type + "/idle/idle0.png"),
            "70": pyg.image.load("resources/" + self.type + "/idle/idle2.png"),
            "75": pyg.image.load("resources/" + self.type + "/idle/idle3.png"),
            "80": pyg.image.load("resources/" + self.type + "/idle/idle5.png"),
            "85": pyg.image.load("resources/" + self.type + "/idle/idle6.png"),
            "100": pyg.image.load("resources/" + self.type + "/idle/idle1.png"),
        }
        self.falling_sprites = {
            "0": pyg.image.load("resources/" + self.type + "/idle/idle0.png"),
            "20": pyg.image.load("resources/" + self.type + "/fall/fall2.png"),
            "30": pyg.image.load("resources/" + self.type + "/fall/fall3.png"),
            "50": pyg.image.load("resources/" + self.type + "/fall/fall4.png"),
        }
        self.running_sprites = {
            "period": 35,
            "0": pyg.image.load("resources/" + self.type + "/run/run0.png"),
            "5": pyg.image.load("resources/" + self.type + "/run/run1.png"),
            "10": pyg.image.load("resources/" + self.type + "/run/run2.png"),
            "15": pyg.image.load("resources/" + self.type + "/run/run3.png"),
            "20": pyg.image.load("resources/" + self.type + "/run/run4.png"),
            "25": pyg.image.load("resources/" + self.type + "/run/run5.png"),
            "30": pyg.image.load("resources/" + self.type + "/run/run6.png"),
        }
        self.walking_sprites = {
            "period": 40,
            "0": pyg.image.load("resources/" + self.type + "/walk/walk0.png"),
            "10": pyg.image.load("resources/" + self.type + "/walk/walk1.png"),
            "20": pyg.image.load("resources/" + self.type + "/walk/walk2.png"),
            "30": pyg.image.load("resources/" + self.type + "/walk/walk3.png"),
        }
        self.ducking_sprites = {
            "0": pyg.image.load("resources/" + self.type + "/duck/duck0.png"),
            "5": pyg.image.load("resources/" + self.type + "/duck/duck1.png"),
            "10": pyg.image.load("resources/" + self.type + "/duck/duck2.png"),
            "15": pyg.image.load("resources/" + self.type + "/duck/duck3.png"),
            "20": pyg.image.load("resources/" + self.type + "/duck/duck4.png"),
            "25": pyg.image.load("resources/" + self.type + "/duck/duck5.png"),
            "30": pyg.image.load("resources/" + self.type + "/duck/duck6.png"),
        }
        self.dissolve_sprites = {
            "30": pyg.image.load("resources/" + self.type + "/dissolve/dissolve0.png"),
            "25": pyg.image.load("resources/" + self.type + "/dissolve/dissolve1.png"),
            "20": pyg.image.load("resources/" + self.type + "/dissolve/dissolve2.png"),
            "15": pyg.image.load("resources/" + self.type + "/dissolve/dissolve3.png"),
            "10": pyg.image.load("resources/blank.png"),
            "0": pyg.image.load("resources/blank.png"),
        }
        self.blank_sprite = pyg.image.load("resources/blank.png")

    def move(self, direction):
        """Moves left to right based on the direction"""        
        self.speed = direction * Globals.player_speed * (0.1 if self.jumping else 1)
        # Increase velocity by speed, then clamp it
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
        # Allows the player to jump if they pressed space within a few frames of hitting the ground
        self.jump_timer = 5 

        # Normal jumping
        if not self.jumping and (self.floored or self.coyotee_timer):
            self.velocity[1] += Globals.jump_force
            self.fall_counter = 0
            
        # Wallkicks
        elif (self.can_wall_jump == "Right" and self.holding_right and self.wall_jump_delay == 0):
            self.velocity[1] = max(self.velocity[1], Globals.jump_force)
            self.wall_jump_delay = 10
            self.kickback = -Globals.player_speed / 2.5
            self.fall_counter = 0
        
        elif (self.can_wall_jump == "Left" and self.holding_left and self.wall_jump_delay == 0):
            self.velocity[1] = max(self.velocity[1], Globals.jump_force)
            self.wall_jump_delay = 10
            self.kickback = Globals.player_speed / 2.5
            self.fall_counter = 0

        self.jumping = True

    def resolve_collisions(self, level: Level=None):
        """Resolves collisions between the player and the platforms in the level"""
        self.can_wall_jump = "None"
        self.is_sliding = False
        self.floored = False

        # Check objects like the flag
        for object in level.objects:
            collision, collision_type = collider.collides_platform(self, object)
            if collision_type == "flag":
                return "flag"

        # Check platforms like lava or steel blocks
        for platform in level.platforms:
            collision, collision_type = collider.collides_platform(self, platform)
            # Lava
            if collision_type == "lava":
                self.dissolve_timer = 30

            # Normal blocks
            elif collision:
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
                    self.fall_counter = 0
                    self.wall_jump_delay = 0
                    self.coyotee_timer = 6
                    if self.jump_timer > 0:
                        self.jump()

                # Ceiling bonk
                elif collision[1] == 1:
                    self.velocity[1] = 0
                    self.y = platform.y - self.height - 0.1
                    
    def update(self, level):
        """Updates the player based on its velocity"""
        self.respawn_timer = max(0, self.respawn_timer-1)
        self.wall_jump_delay = max(0, self.wall_jump_delay-1)
        self.coyotee_timer = max(0, self.coyotee_timer-1)

        # Update timers
        self.frame_counter += 1
        self.fall_counter += 1
        self.dissolve_timer = max(0, self.dissolve_timer - 1)
        self.jump_timer = max(0, self.jump_timer - 1)
        self.pause_timer = max(0, self.pause_timer - 1)

        if self.ducking or self.ducking_timer != 0:
            self.ducking_timer += 1
        if self.ducking_timer > 15 and self.ducking:
            self.ducking_timer -= 1

        if not self.ducking and self.ducking_timer > 35:
            self.ducking_timer = 0

        if self.dissolve_timer == 1:
            self.killed()

        if self.respawn_timer > 40 or self.dissolve_timer > 0 or self.pause_timer > 0:
            self.velocity = [0, 0]
            return
        
        # Don't move or jump if ducking or dissolving
        if self.ducking_timer != 0:
            self.velocity[0] = 0

        if self.walking:
            if self.floored:
                self.velocity[0] *= 0.6
            else:
                self.velocity[0] *= 0.93

        # Update the position
        delta = 1
        if Globals.current_framerate != 0:
            delta = Globals.FPS / Globals.current_framerate

        self.x += self.velocity[0] * delta
        # self.x = min(max(self.x, 0), Globals.WIDTH - self.width)
        self.y += self.velocity[1] * delta

        # Check and resolve platform collisions
        return_val = ""
        if level is not None:
            return_val = self.resolve_collisions(level)

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

        return return_val

    def killed(self):
        """Runs the respawn animation and sounds relating to death"""
        self.respawn_timer = 80
        self.x, self.y = Globals.reset_pos
        Globals.data["deaths"] += 1

    def draw(self):
        """Draws the player sprite"""
        current_sprite = self.blank_sprite

        # Dissolve animation
        if self.dissolve_timer > 0:
            current_sprite = pyg.transform.scale(self.dissolve_sprites["30"], (self.width, self.height))
            keys = list(self.dissolve_sprites.keys())
            for i in range(len(keys)):
                key = keys[i]
                if key != "period":
                    if int(key) < self.dissolve_timer:
                        current_sprite = pyg.transform.scale(self.dissolve_sprites[keys[i-1]], (self.width + 10, self.height))
                        break

        # Ducking animation
        elif self.ducking or self.ducking_timer != 0:
            current_sprite = pyg.transform.scale(self.ducking_sprites["0"], (self.width, self.height))
            keys = list(self.ducking_sprites.keys())
            for i in range(len(keys)):
                key = keys[i]
                if key != "period":
                    if int(key) > self.ducking_timer:
                        current_sprite = pyg.transform.scale(self.ducking_sprites[keys[i-1]], (self.width + 10, self.height))
                        break
            
        # Idle animation
        elif not self.holding_right and not self.holding_left and self.floored:
            current_sprite = pyg.transform.scale(self.idle_sprites["0"], (self.width, self.height))
            keys = list(self.idle_sprites.keys())
            for i in range(len(keys)):
                key = keys[i]
                if key != "period":
                    if int(key) > self.frame_counter % self.idle_sprites["period"]:
                        current_sprite = pyg.transform.scale(self.idle_sprites[keys[i-1]], (self.width, self.height))
                        break

        # Running animation
        elif self.floored and not self.walking:
            current_sprite = pyg.transform.scale(self.running_sprites["0"], (self.width, self.height))
            keys = list(self.running_sprites.keys())
            for i in range(len(keys)):
                key = keys[i]
                if key != "period":
                    if int(key) > self.frame_counter % self.running_sprites["period"]:
                        current_sprite = pyg.transform.scale(self.running_sprites[keys[i-1]], (self.width, self.height))
                        break

        # Walking animation
        elif self.floored and self.walking:
            current_sprite = pyg.transform.scale(self.walking_sprites["0"], (self.width, self.height))
            keys = list(self.walking_sprites.keys())
            for i in range(len(keys)):
                key = keys[i]
                if key != "period":
                    if int(key) > self.frame_counter % self.walking_sprites["period"]:
                        current_sprite = pyg.transform.scale(self.walking_sprites[keys[i-1]], (self.width + 2, self.height))
                        break

        # Falling animation
        elif not self.floored:
            current_sprite = pyg.transform.scale(self.falling_sprites["50"], (self.width, self.height))
            keys = list(self.falling_sprites.keys())
            for i in range(len(keys)):
                key = keys[i]
                if key != "period":
                    if int(key) > self.fall_counter:
                        current_sprite = pyg.transform.scale(self.falling_sprites[keys[i-1]], (self.width + 3, self.height + 6))
                        break
            if self.is_sliding:
                current_sprite = pyg.transform.scale(self.falling_sprites["20"], (self.width + 3, self.height + 6))
        
        # Respawn blinking
        if 0 < self.respawn_timer <= 8 or 16 < self.respawn_timer <= 24 or 30 < self.respawn_timer <= 38 or 46 < self.respawn_timer <= 80:
            current_sprite = self.blank_sprite
        
        Globals.VID_BUFFER.blit(pyg.transform.flip(current_sprite, self.facing == "Left", False), (self.x, Globals.HEIGHT - self.y - self.height, self.width, self.height))
