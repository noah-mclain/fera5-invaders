# Player class managing player actions
import pygame
import copy
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
        self.lasers = []


    def shoot(self):
        laser = Laser(self.rect.x, self.rect.y)
        laser.fire()
        self.lasers.append(laser)
    
    def fired_lasers(self):
        new_lasers = []
        for laser in self.lasers:
            if laser.is_fired == True:
                new_lasers.append(laser)
        self.lasers = new_lasers
        


    # player movement
    def move(self,change):
        self.speed += change
            
    def stop(self):
        self.speed = 0
    

    # drawing the player ship
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for laser in self.lasers:
            laser.draw()
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > self.screen.width - self.rect.width:
            self.rect.x = self.screen.width - self.rect.width
        self.fired_lasers()
        for laser in self.fired_lasers():
            laser.update()


    def die(self):
        self.image = pygame.image.load("assets\images\shipDie.png")
        self.alive = False

        
       


    

