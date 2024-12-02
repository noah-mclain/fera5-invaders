import pygame
from os import path
from environment.sprite import StaticSprite

# Laser class for shooting mechanics
class Laser(StaticSprite):
    def __init__(self, x, y):
        image_path = path.join("assets", "images", "bullet", "a1.png")
        position = (x, y + 5)
        
        super().__init__(image_path, position)
        
        self.speed = -5
        self.is_fired = False
        self.is_engaged = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, screenWidth=None, screenHeight=None):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.is_engaged:
            self.die()

    def fire(self):
        self.is_fired = True

    def die(self):
        self.is_fired = False

    def engage(self):
        self.is_engaged = True
        self.die()




