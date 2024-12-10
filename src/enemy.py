import pygame
from os import path
import random
from egg import Egg
from environment.animated_sprite import AnimatedSprite

class Chicken(AnimatedSprite):
    chicken_counter = 0

    def __init__(self, position, sprite_sheet_path):
        try:
            super().__init__(position, sprite_sheet_path, sprite_type="chicken", initial_state="alive")
            #print(f"Initialized chicken at position {position}")
        except Exception as e:
            print(f"Error initializing Chicken: {str(e)}")
            raise
        
        self.isChickenAlive = True
        self.speed_x = 5
        self.direction = 1
        self.x, self.y = position
        self.eggs = []
        self.fall_speed = 3
        Chicken.chicken_counter += 1
        
        # Start with alive animation
        self.play_animation("alive", loop=True)
        
        # Track states
        self.is_food = False
        self.is_dying = False
        self.current_state = "alive"  # New state tracker

    def update(self, screenWidth=None, screenHeight=None):
        """Update chicken's position and animation."""
        # Debug logging
        #print(f"Current state: {self.current_state}, Animation: {self.current_animation}")
        
        # Update position based on current state
        # if self.current_state == "alive":
        #     if screenWidth is not None and screenHeight is not None:
        #         self.x += self.speed_x * self.direction
        #         self.rect.x = self.x

        #         # Handle screen boundaries
        #         if self.rect.left <= 0:
        #             self.direction = 1
        #         elif self.rect.right >= screenWidth:
        #             self.direction = -1
                    
        if self.current_state == "dead":
            if self.animation_done:
                self._switch_to_food()
        elif self.current_state == "food":
            self.y += self.fall_speed
            self.rect.y = self.y
            
            # Remove if falls off screen
            if screenHeight and self.rect.top > screenHeight:
                self._remove_sprite()
                
        for egg in list(self.eggs):
            egg.update(screenHeight)
            
            if egg.should_disappear():
                egg._remove_sprite()
        
        # Always update the current animation
        super().update()
        
    def eggDisappear(self):
        aliveEggs = []
        
        for egg in self.eggs:
            if egg.shouldDisappear() == False or egg.isBreaking == True:
                aliveEggs.append(egg)
            if egg.super().isAnimationDone():
                aliveEggs.remove(egg)
            #elif egg.rect.bottom <= self.screenHeight:
                #aliveEggs.append(egg)
        #waw!        
        self.eggs = aliveEggs
    
    def killChicken(self):
        """Handle chicken death."""
        if self.current_state == "alive":
            self.isChickenAlive = False
            self.current_state = "dead"
            self.stop_animation()
            if "dead" in self.animations:
                self.play_animation("dead", loop=False)
                #print("playing dead animation")

            Chicken.chicken_counter -= 1

    def _switch_to_food(self):
        """Helper method to switch to food state"""
        if self.current_state == "dead":
            #print("Switching to food")
            self.current_state = "food"
            self.stop_animation()
            
            # Randomly select one of the food frames
            food_frame = random.choice(["chicken_leg", "double_chicken_leg", "roast"]) 
            
            #print(f"Selected food frame: {food_frame}")
                
            if "food" in self.animations:
                #print(f"Playing {food_frame} animation")
                if food_frame in [frame[1] for frame in self.frames["food"]]:
                    self.play_animation("food", loop=False, specific_frame=food_frame)
                    self.is_food = True
            else:
                print(f"Warning: Food frame '{food_frame}' not found in animations.")
                
    def get_xp(self):
        """Return the XP value based on the current state"""
        if self.current_state == "food":
            # Check which food frame is currently displayed
            current_frame_name = super().current_animation_frame_name()  # Assume this method returns the current frame's name
            if current_frame_name == "chicken_leg":
                return 25
            elif current_frame_name == "double_chicken_leg":
                return 50
            elif current_frame_name == "roast":
                return 100
        return 0  # No XP if not in a food state
    
    def _remove_sprite(self):
        """Remove the sprite after all animations are complete"""
        self.kill()  # This removes the sprite from all sprite groups

    @staticmethod
    def get_chicken_count():
        return Chicken.chicken_counter

    def lay_eggs(self, all_sprites):
        """Lay eggs from the chicken's position."""
        egg_x = self.rect.centerx
        egg_y = self.rect.bottom
        new_egg = Egg(egg_x, egg_y)
        self.eggs.append(new_egg)
        all_sprites.add(new_egg)
        #print(f"Laying egg at position: ({egg_x}, {egg_y})")  
        return Egg(egg_x, egg_y)
    
    def set_alpha(self, alpha_value):
        self.image.set_alpha(alpha_value)