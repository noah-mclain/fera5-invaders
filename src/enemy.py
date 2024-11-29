import pygame
from os import path
from egg import Egg
from environment.animated_sprite import AnimatedSprite
import random

class Chicken(AnimatedSprite):
    chicken_counter = 0

    def __init__(self, position, sprite_sheet_path):
        super().__init__(position, sprite_sheet_path, sprite_type="chicken")
        self.isChickenAlive = True
        self.speed_x = 2
        self.direction = 1
        self.x, self.y = position
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
        # Update position based on current state
        if self.current_state == "alive":
            if screenWidth is not None and screenHeight is not None:
                self.x += self.speed_x * self.direction
                self.rect.x = self.x

                # Handle screen boundaries
                if self.rect.left <= 0:
                    self.direction = 1
                elif self.rect.right >= screenWidth:
                    self.direction = -1
        elif self.current_state == "food":
            self.y += self.fall_speed
            self.rect.y = self.y
            
            # Remove if falls off screen
            if screenHeight and self.rect.top > screenHeight:
                self._remove_sprite()
        
        # Always update the current animation
        super().update()

    def killChicken(self):
        """Handle chicken death."""
        if self.current_state == "alive":
            self.isChickenAlive = False
            self.current_state = "dead"
            self.stop_animation()
            self.play_animation("dead", loop=False)
            self.animations["dead"].callback = self._switch_to_food
            Chicken.chicken_counter -= 1

    def _switch_to_food(self):
        """Helper method to switch to food state"""
        if self.current_state == "dead":  # Only switch if we're in dead state
            self.current_state = "food"
            self.stop_animation()
            self.play_animation("food", loop=True)
            self.is_food = True

    def _remove_sprite(self):
        """Remove the sprite after all animations are complete"""
        self.kill()  # This removes the sprite from all sprite groups

    @staticmethod
    def get_chicken_count():
        return Chicken.chicken_counter

    def layEggs(self):
        """Lay eggs from the chicken's position."""
        egg_x = self.rect.centerx
        egg_y = self.rect.bottom
        return Egg(egg_x, egg_y)