import pygame
from os import path

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, powerup_type, laser_increment=0, laser_type=0):
        super().__init__()
        # Load the sprite sheet
        sprite_sheet_path = "assets/images/powerups/powerup.png"
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()


        audio_path = path.join("assets", "sounds", "take-off-36682.mp3")
        if not path.exists(audio_path):
            raise FileNotFoundError(f"Power-up sound not found: {audio_path}")
        self.powerup_sound = pygame.mixer.Sound(audio_path)
        # Extract individual frames from the sprite sheet
        self.frames = self._extract_frames(sprite_sheet, frame_width=45, frame_height=35)
        if not self.frames:
            raise ValueError("No frames extracted. Check sprite sheet size and frame dimensions.")
        self.current_frame = 0
        self.animation_speed = 0.1  # Time between frames
        self.last_update = pygame.time.get_ticks()
        self.animation_done = False

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.type = powerup_type
        self.laser_increment = laser_increment
        self.laser_type = laser_type

    def _extract_frames(self, sprite_sheet, frame_width, frame_height):
        sheet_width, sheet_height = sprite_sheet.get_size()
        frames = []
       
        for x in range(0, sheet_width, frame_width):
            if x + frame_width > sheet_width:  # Check if frame exceeds width
                break
            if frame_height > sheet_height:  # Check if frame exceeds height
                break
            frame = sprite_sheet.subsurface(pygame.Rect(x, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def apply_to_player(self, player):
        self.play_powerup_effect()
        if self.type == "increment_laser":
            player.laser_count += self.laser_increment
            #print(f"Laser count increased to {player.laser_count}!")
        elif self.type == "change_laser":
            player.laser_type = self.laser_type
            #print(f"Laser type changed to {player.laser_type}!")
        
    def play_powerup_effect(self):
        self.powerup_sound.play()

    def update(self):
        """Update the animation frames."""
        if not self.animation_done:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > self.animation_speed * 1000:
                self.last_update = current_time
                self.current_frame += 1
                if self.current_frame < len(self.frames):
                    self.image = self.frames[self.current_frame]
                else:
                    self.animation_done = True
                    
    def draw(self, screen):
        """Draw the current frame on the screen."""
        if not self.animation_done:
            screen.blit(self.image, self.rect)
