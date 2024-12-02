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
        
        self.current_state = "whole"
        self.isEggWhole = True
        
        self.play_animation("whole", loop=False)
    
    def update(self,screenHeight):
        self.rect.y += self.speedY
        
        #if egg hits bottom of screen
        if self.rect.bottom>  screenHeight:
            self.rect.bottom = screenHeight
            self.isDisappear = True
            
    def breakEgg(self):
        if self.current_state == "whole":
            self.isEggWhole = False
            self.current_state = "broken"
            self.stop_animation()
            if 'broken' in self.animations:
                self.play_animation("broken", loop=False)
            print("playing broken animation")

        #if egg hits spaceship?
    
    def should_disappear(self):
        return Egg.isDisappear  
    
    def isEggWhole(self):
        return self.isEggWhole
        
            
        