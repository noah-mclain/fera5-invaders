import pygame
from os import path
from environment.animated_sprite import AnimatedSprite

class Egg(AnimatedSprite): 
    def __init__(self, x, y):
        sprite_sheet_path = path.join("assets", "images", "Enemy", "eggSpriteSheet.png")
        
        super().__init__((x, y), sprite_sheet_path, sprite_type="egg", initial_state="whole")
        
        self.speedY = 2
        self.isDisappear = False
        
        self.current_state = "whole"
        self.is_egg_whole = True
        self.isBreaking = False
        
        self.play_animation("whole", loop=False)
    
    def update(self, screenHeight):
        #if not self.isDisappear:
        self.rect.y += self.speedY
        
        #if egg hits bottom of screen
        if self.rect.bottom > screenHeight:
            self.rect.bottom = screenHeight
            # self.isDisappear = True

            if not self.isBreaking:
                self.breakEgg()
            
        # If the egg is breaking, check that the animation is complete
        if self.isBreaking:
            current_time = pygame.time.get_ticks()
            super().update()
            
            if super().isAnimationDone():
                self.isDisappear = True
          
                if self.isDisappear:
                    self._remove_sprite()
                  
    def breakEgg(self):
        if self.current_state == "whole":
            self.is_egg_whole = False
            self.current_state = "broken"
            self.stop_animation()
            if 'broken' in self.animations:
                self.play_animation("broken", loop=False)
                self.isBreaking = True
                print("playing broken animation")

        #if egg hits spaceship?
    
    def should_disappear(self):
        return self.isDisappear  
    
    def isEggWhole(self):
        return self.is_egg_whole
    
    def _remove_sprite(self):
        """Remove the sprite after all animations are complete"""
        self.kill()  # This removes the sprite from all sprite groups
    
