import pygame
from os import path

class Egg:
    
    def __init__(self,x,y) -> None:
        image_path = path.join("assets", "images", "Enemy", "egg.png")
        image=pygame.image.load(image_path)
        self.width=10
        self.height=10
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.rect=self.image.get_rect(topleft=(x,y))
        self.speedY=2
        self.isDisappear = False

    def draw(self,screen):
        screen.blit(self.image,self.rect)
    
    def update(self,screenHeight):
        self.rect.y+=self.speedY
        
        #if egg hits bottom of screen
        if self.rect.bottom>screenHeight:
            self.rect.bottom=screenHeight
            self.isDisappear = True

        #if egg hits spaceship?
    
    def shouldDisappear(self):
        return self.isDisappear  
        
            
        