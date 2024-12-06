# Player class managing player actions
import copy
from os import path

import pygame

from environment.animation_sequence import AnimationSequence
from environment.sprite import StaticSprite
from environment.sprite_sheet import SpriteSheet
from laser import Laser


class Player(StaticSprite):
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.laser_count = 1 
        self.laser_type = 0
        self.laser_count = 1
        # self.rect = self.image.get_rect(midbottom=(screen_width // 2, screen_height - 20))
        self.sprite_path_format = path.join("assets", "images", "ship{}.png")
        initial_image_path = self.sprite_path_format.format(self.laser_count)
        size = (50, 50)
        position = (screen_width // 2, screen_height - 200)

        self.sprite = pygame.image.load(initial_image_path).convert_alpha()
        self.powerup_sound = pygame.mixer.Sound("assets/sounds/take-off-36682.mp3")

        powerup_sprite_sheet_path = path.join("assets", "images","powerups", "powerup.png")
        sprite_sheet = SpriteSheet(pygame.image.load(powerup_sprite_sheet_path).convert_alpha())
        print("SPRITE FOUND")
        
        self.powerup_animation = AnimationSequence(
            [sprite_sheet.get_image_at_pos(i * 64, 0, 64, 64, scale=1.5) for i in range(30)],
            animation_speed=0.1
        )
        self.is_animating_powerup = False
        
        super().__init__(initial_image_path, position, size)

        self.speed = 0
        self.max_speed = 8
        self.alive = True
        self.lasers = []
        self.lives = 3
        self.flicker_timer = 0
        self.powerup_effects={}

    def shoot(self):
        if len(self.lasers) < self.laser_count:
            total_spread = 60  # Total spread angle in degrees (adjust as desired)
            if self.laser_count == 1:
                angles = [0]  # Single laser shoots straight up
            else:
                step = total_spread / (self.laser_count - 1)
                angles = [-total_spread / 2 + i * step for i in range(self.laser_count)]
            
            laser_spacing = 15  # Distance between lasers
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
            
        if self.is_animating_powerup:
            self.powerup_animation.update(pygame.time.get_ticks())
            self.powerup_animation.draw(screen, self.rect.center)
            if self.powerup_animation.animation_finished:
                self.is_animating_powerup = False 
        else:
            screen.blit(self.image, self.rect) 
        
        for laser in self.lasers:
            laser.draw(screen)

    def update(self, screen_width=None, screen_height=None):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > self.screen_width - self.rect.width:
            self.rect.x = self.screen_width - self.rect.width
        keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     self.rect.x -= self.speed
        # if keys[pygame.K_RIGHT]:
        #     self.rect.x += self.speed

        self.rect.clamp_ip(pygame.Rect(0, 0, 1920, 1080))
        for laser in self.lasers[:]:
            laser.update()
            if laser.rect.bottom < 0:
                self.lasers.remove(laser)

        self.fired_lasers()
        for laser in self.lasers:
            laser.update()

    def die(self):
        death_image_path = path.join("assets", "images", "shipDie.png")
        self.image = pygame.image.load(death_image_path)
        self.alive = False

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            print(f"Remaining lives: {self.lives}")
            return True
        return False   
        
    def is_alive(self):
        return self.lives > 0

    def apply_powerup(self, powerup):
        #powerup.apply(self)
        if powerup.type == "increment_laser":
            self.laser_count += powerup.laser_increment
        elif powerup.type == "change_laser":
            self.laser_type = powerup.laser_type
        self._trigger_powerup_animation()
        self._play_powerup_effect()



    def _update_sprite_for_laser_count(self):
        new_sprite_path = self.sprite_path_format.format(self.laser_count)
        if path.exists(new_sprite_path):
            self.sprite = pygame.image.load(new_sprite_path).convert_alpha()
        else:
            print(f"Warning: Sprite for laser count {self.laser_count} not found.")

    def _trigger_powerup_animation(self):
        print("Triggering powerup animation!")
        self.is_animating_powerup = True
        self.powerup_animation.play(loop = False)

    def _play_powerup_effect(self):
        print("Power-up activated!")
        self.powerup_sound.play()