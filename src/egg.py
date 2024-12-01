import pygame
from os import path
from environment.animated_sprite import AnimatedSprite

class Egg(AnimatedSprite):
    
    isDisappear=False
    
    def __init__(self, x, y):
        sprite_sheet_path = path.join("assets", "images", "Enemy", "eggSpriteSheet.png")
        
        super().__init__((x, y), sprite_sheet_path, sprite_type="egg", initial_state="whole")
        
        self.speedY = 2
        self.isDisappear = False
        
        self.play_animation("whole", loop=False)
        

    # def draw(self,screen):
    #     super().draw(screen)
    
    def update(self,screenHeight):
        self.rect.y += self.speedY
        
        #if egg hits bottom of screen
        if self.rect.bottom>  screenHeight:
            self.rect.bottom = screenHeight
            self.isDisappear = True

        #if egg hits spaceship?
    
    def should_disappear(self):
        return Egg.isDisappear  
        
            
        