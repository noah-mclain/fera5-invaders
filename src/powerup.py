import pygame
from os import path


class PowerUp:
    def __init__(self, powerup_type, laser_increment, sound_path="assets/sounds/powerup_woosh.mp3"):
        self.powerup_type = powerup_type
        self.laser_increment = laser_increment
        self.sound = pygame.mixer.Sound(sound_path) 

    def apply(self, player):
        player.laser_count += self.laser_increment
        self._play_sound()
        self._trigger_visual_effect(player)
        player._update_sprite_for_laser_count()

    def _play_sound(self):
        self.sound.play()

    def _trigger_visual_effect(self, player):
        flicker_duration = 1500
        flicker_interval = 100
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < flicker_duration:
            player.sprite.set_alpha(0)
            pygame.time.delay(flicker_interval // 2)
            player.sprite.set_alpha(255)
            pygame.time.delay(flicker_interval // 2)
