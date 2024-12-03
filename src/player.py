# Player class managing player actions
import pygame
import copy
from os import path
from laser import Laser
from environment.sprite import StaticSprite
from environment.sprite_sheet import SpriteSheet
from environment.animation_sequence import AnimationSequence


class Player(StaticSprite):
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.laser_count = 1 

        self.sprite_path_format = path.join("assets", "images", "ship{}.png")
        initial_image_path = self.sprite_path_format.format(self.laser_count)
        size = (50, 50)
        position = (screen_width // 2, screen_height - 200)

        self.sprite = pygame.image.load(initial_image_path).convert_alpha()
        self.powerup_sound = pygame.mixer.Sound("assets/sounds/take-off-36682.mp3")

        powerup_sprite_sheet_path = path.join("assets", "images","powerups", "atomic-powerup.png")
        sprite_sheet = SpriteSheet(pygame.image.load(powerup_sprite_sheet_path).convert_alpha())
        self.powerup_animation = AnimationSequence(
            [sprite_sheet.get_image_at_pos(i * 32, 0, 32, 32) for i in range(30)], animation_speed=0.1
        )
        self.is_animating_powerup = False
        
        super().__init__(initial_image_path, position, size)

        self.speed = 0
        self.max_speed = 5
        self.alive = True
        self.lasers = []
        self.lives = 3
        self.flicker_timer = 0

    def shoot(self):
        print(f"Shooting {self.laser_count} lasers!")
        for i in range(self.laser_count):
            offset = i - (self.laser_count // 2)  
            laser = Laser(self.rect.x + offset * 10, self.rect.y)
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
            self.powerup_animation.update()
            self.powerup_animation.draw(screen)
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

        self.fired_lasers()
        for laser in self.lasers:
            laser.update()

    def die(self):
        death_image_path = path.join("assets", "images", "shipDie.png")
        self.image = pygame.image.load(death_image_path)
        self.alive = False

    def lose_life(self):
        self.lives -= 1
        self.flicker_timer = pygame.time.get_ticks()

    def is_alive(self):
        return self.lives > 0

    def apply_powerup(self, powerup):
        powerup.apply(self)
        self._trigger_powerup_animation()



    def _update_sprite_for_laser_count(self):
        new_sprite_path = self.sprite_path_format.format(self.laser_count)
        if path.exists(new_sprite_path):
            self.sprite = pygame.image.load(new_sprite_path).convert_alpha()
        else:
            print(f"Warning: Sprite for laser count {self.laser_count} not found.")

    def _trigger_powerup_animation(self):
        print("Triggering powerup animation!")
        self.is_animating_powerup = True