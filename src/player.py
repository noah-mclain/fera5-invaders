# Player class managing player actions
import copy
from os import path

import pygame

from environment.animation_sequence import AnimationSequence
from environment.sprite import StaticSprite
from environment.sprite_sheet import SpriteSheet
from laser import Laser
from powerup import PowerUp 

MAX_LIVES =3

class Player(StaticSprite):
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.laser_count = 1 
        self.laser_type = 0
        
        self.sprite_path_format = path.join("assets", "images", "ship{}.png")
        initial_image_path = self.sprite_path_format.format(self.laser_count)
        size = (50, 50)
        position = (screen_width // 2, screen_height - 200)

        self.sprite = pygame.image.load(initial_image_path).convert_alpha()
        
        self.speed = 0
        self.max_speed = 8
        self.alive = True
        self.lasers = []
        self.lives = 3
        self.xp = 0
        self.score = 0
        self.flicker_timer = 0
        self.powerup_animation = None
        self.is_animating_powerup = False
        self.max_laser_count = 10
        
        self.game_instance = None # So that player can access the hearts later on 
        
        super().__init__(initial_image_path, position, size)

    def shoot(self):
        if len(self.lasers) == 10:
            return
        if len(self.lasers) < self.laser_count:
            total_spread = 5  # Total spread angle in degrees (adjust as desired)
            if self.laser_count == 1:
                angles = [0]  
            else:
                step = total_spread / (self.laser_count - 1)
                angles = [-total_spread / 2 + i * step for i in range(self.laser_count)]
            
            laser_spacing = 15  
            total_width = laser_spacing * (self.laser_count - 1)
            start_x = self.rect.centerx - (total_width // 2)

            for i, angle in enumerate(angles):
                laser_x = start_x + i * laser_spacing
                laser_type = 1 if self.laser_count >= 3 else 0  
                laser = Laser(laser_x, self.rect.top, laser_type, angle)
                laser.fire()
                self.lasers.append(laser)


    def fired_lasers(self):
        self.lasers = [laser for laser in self.lasers if laser.is_fired]

    def move(self, change):
        self.speed += change

    def stop(self):
        self.speed = 0

    def draw(self, screen):
        if pygame.time.get_ticks() - self.flicker_timer < 1000:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                return
        screen.blit(self.image, self.rect)
        for laser in self.lasers:
            laser.draw(screen)
            
        if self.powerup_animation and not self.powerup_animation.animation_done:
            self.powerup_animation.update()
            self.powerup_animation.draw(screen)
        
        for laser in self.lasers:
            laser.draw(screen)

    def update(self, screen_width=None, screen_height=None):
        self.rect.x += self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > self.screen_width - self.rect.width:
            self.rect.x = self.screen_width - self.rect.width
        keys = pygame.key.get_pressed()
       
        for laser in self.lasers[:]:
            laser.update()
            if laser.rect.bottom < 0:
                self.lasers.remove(laser)

        self.fired_lasers()

        for laser in self.lasers:
            laser.update()

        if self.powerup_animation and not self.powerup_animation.animation_done:
            self.powerup_animation.update()

    def die(self):
        death_image_path = path.join("assets", "images", "shipDie.png")
        self.image = pygame.image.load(death_image_path)
        self.alive = False

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            #print(f"Remaining lives: {self.lives}")
            return True
        return False   
        
    def is_alive(self):
        return self.lives > 0

    def apply_powerup(self, powerup):
        powerup.apply_to_player(self)
        self._update_sprite_for_laser_count()
        self.powerup_animation = None 

    def _update_sprite_for_laser_count(self):
        new_sprite_path = self.sprite_path_format.format(self.laser_count)
        if path.exists(new_sprite_path):
            self.sprite = pygame.image.load(new_sprite_path).convert_alpha()
        else:
            print(f"Warning: Sprite for laser count {self.laser_count} not found.")
       
    def add_xp(self, amount):
        """Add XP and handle life restoration or point conversion."""
        #print(f"XP gained: {amount}. Total XP before addition: {self.xp}")
        
        self.xp += amount
        
        while self.xp >= 1000:
            if self.lives < MAX_LIVES:
                #print("Life restored!")
                self.lives += 1
                self.xp -= 1000
                
                # Trigger heart restoration animation
                if hasattr(self.game_instance, 'hearts') and len(self.game_instance.hearts) > (self.lives - 1):
                    self.game_instance.hearts[self.lives - 1].play_reverse_animation()
            else:
                points_gained = (self.xp // 1000) * 500
                #print(f"Converted {self.xp} XP to {points_gained} points")
                self.score += points_gained
                self.xp %= 1000  # Keep remainder of XP after conversion
