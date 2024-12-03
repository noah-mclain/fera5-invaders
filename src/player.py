# Player class managing player actions
import pygame
import copy
from os import path
from laser import Laser
from environment.sprite import StaticSprite

class Player(StaticSprite):
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        image_path = path.join("assets", "images", "ship.png")
        size = (50, 50)
        position = (screen_width // 2, screen_height - 200)
        
        super().__init__(image_path, position, size)
        
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
    
    def update(self, screenWidth=None, screenHeight=None):
        # Update position
        self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > self.screen_width - self.rect.width:
            self.rect.x = self.screen_width - self.rect.width
            
        # Update lasers
        self.fired_lasers()
        for laser in self.lasers:
            laser.update()

    def die(self):
        death_image_path = path.join("assets", "images", "shipDie.png")
        self.image = pygame.image.load(death_image_path)
        self.alive = False

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            print(f"Remaining lives: {self.lives}")
            return True
        return False   
        
    def is_alive(self):
        return self.lives > 0


    

