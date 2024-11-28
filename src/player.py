# Player class managing player actions
import pygame
from laser import Laser

class Player:
    def __int__(self, x,y):
        self.image = pygame.image.load("assets\images\ship.png")
        self.rect = self.image.get_rect()
        info = pygame.display.Info()
        self.screen.width = info.current_w
        self.screen.height = info.current_h
        self.rect.x = self.screen.width /2
        self.rect.y = self.screen.height - 15
        self.speed = 0
        self.max_speed = 5 
        self.alive = True


    def shoot(self):
        laser = Laser(self.rect.x, self.rect.y)
        laser.fire()

    # player movement
    def move(self,change):
        self.speed += change
            
    def stop(self):
        self.speed = 0
    

    # drawing the player ship
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > self.screen.width - self.rect.width:
            self.rect.x = self.screen.width - self.rect.width

    def die(self):
        self.image = pygame.image.load("assets\images\shipDie.png")
        self.alive = False

        
       


    

