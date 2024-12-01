# Player class managing player actions
import pygame
import copy
from os import path
from laser import Laser

class Player:
    def __init__(self):
        image_path = path.join("assets", "images", "ship.png")
        image = pygame.image.load(image_path)
        self.width = 50
        self.height = 50
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect()
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        self.rect.x = self.screen_width // 2
        self.rect.y = self.screen_height - 200
        self.speed = 0
        self.max_speed = 5 
        self.alive = True
        self.lasers = []
        self.lives = 3
        self.flicker_timer = 0
        


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
        if pygame.time.get_ticks() - self.flicker_timer < 1000:
            if(pygame.time.get_ticks() // 100) % 2 ==0:
                return
        screen.blit(self.image, self.rect)
        for laser in self.lasers:
            laser.draw(screen)
    
    def update(self):
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


    

