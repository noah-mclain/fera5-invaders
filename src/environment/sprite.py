# Sprite class to handle sprite functions
import pygame

class Drawable:
    """Base class for drawable objects"""
    pass

class Sprite(Drawable):
    """Static sprite class"""
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = None
    
    def draw(self, context, camera=None):
        if camera:
            context.blit(self.image, (self.x - camera.x, self.y - camera.y))
        else:
            context.blit(self.image, (self.x, self.y))




