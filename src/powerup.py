import pygame
from os import path


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, powerup_type, laser_increment=0, laser_type=0):
        super().__init__()
        self.image = pygame.image.load("assets/images/powerup/powerup.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.type = powerup_type
        self.laser_increment = laser_increment
        self.laser_type = laser_type

    def apply(self, player):
        if self.type == "increment_laser":
            player.laser_count += self.laser_increment
            print(f"Laser count increased to {self.laser_count}!")
        elif self.type == "change_laser":
            player.laser_type = self.laser_type
            print(f"Laser type changed to {self.laser_type}!")
        self._trigger_powerup_animation()
        self._play_powerup_effect()
