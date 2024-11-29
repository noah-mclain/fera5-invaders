# Enemy class for chicken behavior
import pygame
from os import path
from egg import Egg
from random import random
class Chicken:

    chicken_counter=0
    
    def __init__(self,x,y) -> None:
        image_path = path.join("assets","images","Enemy", "chiken.png") 
        image=pygame.image.load(image_path)
        self.width = 50
        self.height = 50
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.isChickenAlive=True
        self.rect=self.image.get_rect(topleft=(x,y))
        Chicken.chicken_counter+=1
        
        self.speed_x = 2
        self.direction = 1
        self.eggs=[]
       
    
    def draw(self,screen):
        if self.isChickenAlive:
            screen.blit(self.image,self.rect)
            for egg in self.eggs:
                egg.draw(screen)
            

    def update(self, screenWidth,screenHeight):
        if not self.isChickenAlive:
            return
        
        self.rect.x += self.speed_x * self.direction
        
        if self.rect.left <= 0:
            self.direction =1
            self.rect.y += 20
        elif self.rect.right >= screenWidth:
            self.direction = -1
            self.rect.y += 20
            
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screenHeight:
            self.rect.bottom = screenHeight
            
        if random() <= 0.001:
            self.layEggs()

        self.eggDisappear()
        for egg in self.eggs:
            egg.update(screenHeight)
            
            
        
    def eggDisappear(self):
        aliveEggs=[]
        
        for egg in self.eggs:
            if egg.shouldDisappear()== False:
                aliveEggs.append(egg)
        #waw!        
        self.eggs=aliveEggs

            

    def killChicken(self):   
        if self.isChickenAlive:
            death_image_path = path.join("assets","images","Enemy","dead.png")
            death_image = pygame.image.load(death_image_path)
            self.image = pygame.transform.scale(death_image, (50, 50))
            Chicken.chicken_counter-=1
            self.isChickenAlive=False

    # def __del__(self): # to kill the chicken
    @staticmethod
    def get_chicken_count():
        return Chicken.chicken_counter

    def layEggs(self):
        eggX= self.rect.centerx
        eggY=self.rect.bottom
        egg = Egg(eggX,eggY)
        self.eggs.append(egg)

    
        

