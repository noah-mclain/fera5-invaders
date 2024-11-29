import pygame
from os import path
from egg import Egg
from environment.animated_sprite import AnimatedSprite

class Chicken(AnimatedSprite):
    chicken_counter = 0

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.isChickenAlive = True
        self.speed_x = 2
        self.direction = 1
        Chicken.chicken_counter += 1

        # Load the sprite sheet
        sprite_path = path.join("assets", "images", "Enemy", "chickenRed.png")
        self.image = pygame.image.load(sprite_path).convert_alpha()
        
        # Scale the sprite sheet first
        total_width = self.width * 8  # 8 frames
        self.image = pygame.transform.scale(self.image, (total_width, self.height))
        
        # Now set the frame dimensions
        self.set_frame_dimensions(self.width, self.height)
        
        # Add animation sequences
        self.add_sequence("alive", 0, 0, 0, 7)
        self.add_sequence("dead", 0, 0, 0, 0)
        
        # Start the animation
        self.play_sequence("alive", loop=True)
        
        # Set initial rect
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self, screen):
        """Draw the current frame."""
        if self.isChickenAlive:
            # Extract the current frame
            frame_rect = pygame.Rect(
                self.frame_x, self.frame_y, self.frame_width, self.frame_height
            )
            frame = self.image.subsurface(frame_rect)
            screen.blit(frame, (self.rect.x, self.rect.y))
        else:
            # Optional: Draw other effects when dead
            pass

    def update(self, screenWidth, screenHeight):
        """Update chicken's position and animation."""
        if not self.isChickenAlive:
            return

        # Update position
        self.x += self.speed_x * self.direction
        self.rect.x = self.x  # Sync position with rect

        # Handle screen boundaries
        if self.rect.left <= 0:
            self.direction = 1
            self.y += 20
            self.rect.y = self.y
        elif self.rect.right >= screenWidth:
            self.direction = -1
            self.y += 20
            self.rect.y = self.y

        # Keep within screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
            self.y = self.rect.y
        if self.rect.bottom > screenHeight:
            self.rect.bottom = screenHeight
            self.y = self.rect.y - self.height

        # Update animation
        super().update(1 / 60)

    def killChicken(self):
        """Handle chicken death."""
        if self.isChickenAlive:
            self.play_sequence("dead", loop=False)  # Play death animation
            Chicken.chicken_counter -= 1
            self.isChickenAlive = False

    @staticmethod
    def get_chicken_count():
        return Chicken.chicken_counter

    def layEggs(self):
        """Lay eggs from the chicken's position."""
        egg_x = self.rect.centerx
        egg_y = self.rect.bottom
        return Egg(egg_x, egg_y)