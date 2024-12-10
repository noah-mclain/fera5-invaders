from os import path
import pygame
from environment.animated_sprite import AnimatedSprite

class Heart(AnimatedSprite):
    def __init__(self, position):
        sprite_sheet_path = path.join("assets", "images", "background", "livesSpriteSheet.png")
        super().__init__(position, sprite_sheet_path, sprite_type="heart", initial_state="full")
        
        self.current_state = "full"
        self.flickering = False
        self.flicker_count = 0 
        self.flicker_delay = 200
        self.play_animation("full", loop=False)
        
    def lose_life(self):
        # Start the flickering animation when the player loses a life
        if self.current_state == "full":
            #print("Heart is flickering")
            self.flickering = True
            self.flicker_count = 4
            self.play_animation("empty", loop=False)
            
    def play_reverse_animation(self):
        # Play the lose life animation in reverse to restore the life
        #print("Restoring life")
        self.animation_done = False
        self.play_animation("full", loop=False)
        
    def update(self):
        super().update()  # Call parent update to handle animation frames

        # Update the heart's state.
        if self.flickering:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time >= self.flicker_delay:
                # Check if we need to switch animations based on flicker count
                if self.flicker_count > 0:
                    if self.current_animation == "empty":
                        self.play_animation("full", loop=False)  # Switch to empty
                    else:
                        self.play_animation("empty", loop=False)  # Switch back to full
                    
                    # Decrease flicker count after switching states
                    self.flicker_count -= 1
                    self.last_update_time = current_time
                    
                # If flicker count reaches zero, set to empty state and stop flickering.
                if self.flicker_count <= 0 and self.current_animation == "empty":
                    self.current_state = "empty"
                    #print("Heart is now empty")
                    self.flickering = False
                    self.play_animation("empty", loop=False)


    def draw(self, screen):
        # Draw the current image of the heart on the given surface.
        if self.image is not None: 
            screen.blit(self.image, self.rect)  
