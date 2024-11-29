import pygame
from environment.sprite import Sprite

class FrameSprite(Sprite):
    """Sprite that represents a portion of an image."""
    def __init__(self):
        super().__init__()
        self.frame_x = 0
        self.frame_y = 0
        self.frame_width = 0
        self.frame_height = 0

    def draw(self, context, camera=None):
        if self.frame_width <= 0 or self.frame_height <= 0:
            return
        
        # Create a subsurface for the current frame
        try:
            frame_rect = pygame.Rect(
                self.frame_x, self.frame_y, self.frame_width, self.frame_height
            )
            draw_x = self.x - (camera.x if camera else 0)
            draw_y = self.y - (camera.y if camera else 0)
            cropped_frame = self.image.subsurface(frame_rect)
            context.blit(cropped_frame, (draw_x, draw_y))
        except ValueError as e:
            print(f"Frame error: {e}")
            print(f"Frame dimensions: {self.frame_width}x{self.frame_height}")
            print(f"Image dimensions: {self.image.get_width()}x{self.image.get_height()}")