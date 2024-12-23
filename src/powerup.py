import os

import pygame

from environment.animated_sprite import AnimatedSprite


class PowerUp(AnimatedSprite):
    def __init__(self, powerup_type, position, laser_increment=0, laser_type=0):
        sprite_sheet_path = "assets/images/powerups/powerup.png"
        super().__init__(position, sprite_sheet_path, sprite_type="powerup", initial_state="active")

        audio_path = os.path.join("assets", "sounds", "take-off-36682.mp3")
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Power-up sound not found: {audio_path}")
        self.powerup_sound = pygame.mixer.Sound(audio_path)

        self.type = powerup_type
        self.laser_increment = laser_increment
        self.laser_type = laser_type


        self.play_animation("active", loop=False)
        self.powerup_sound.play()

    def apply_to_player(self, player):
        if self.type == "increment_laser":
            player.laser_count += self.laser_increment
        elif self.type == "change_laser":
            player.laser_type = self.laser_type

    def draw(self, screen):
        if not self.animation_done:
            screen.blit(self.image, self.rect)
            
    def update(self):
        super().update()
        