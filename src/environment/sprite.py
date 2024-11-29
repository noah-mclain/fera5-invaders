import pygame
from os import path

class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, position, size=None):
        super().__init__()
        
        # Load the image
        self.image = pygame.image.load(image_path).convert_alpha()
        
        # Scale if size is provided
        if size:
            self.image = pygame.transform.scale(self.image, size)
            
        # Set up rect
        self.rect = self.image.get_rect(topleft=position)
        
    def update(self):
        # Static sprites don't need animation updates
        pass
