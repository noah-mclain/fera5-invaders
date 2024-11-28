# Player class managing player actions
import pygame

class Player:
    def __int__(self, x,y):
        self.image = pygame.image.load("assets\images\ship.png")
        self.rect = self.image.get_rect((x,y))
        

    def shoot(self):
        ...

    def move(self,change):
        self.rect.x += change
        return self.rect.x
    

    

