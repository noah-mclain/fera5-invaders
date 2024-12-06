import pygame
from os import path
from environment.sprite import StaticSprite

# Laser class for shooting mechanics
class Laser(StaticSprite):
    class Laser(StaticSprite):
        def __init__(self, x, y, laser_type=0, angle=0):
            image_paths = [
                path.join("assets", "images", "bullet", "a1.png"),  # Yellow laser
                path.join("assets", "images", "bullet", "b1.png")   # Red laser
            ]
            image_path = image_paths[laser_type]
            if not path.exists(image_path):
                raise FileNotFoundError(f"Laser image not found: {image_path}")
            
            position = (x, y)
            
            super().__init__(image_path, position)

            self.speed = -5
            self.angle = angle
            self.is_fired = False
            self.is_engaged = False
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, screenWidth=None, screenHeight=None):
        self.rect.x += self.angle
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




