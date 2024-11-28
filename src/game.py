# Game class handling game logic

import pygame
import random

# Class imports
from player import Player
from enemy import Enemy
from laser import Laser

class Game:
    def __init__(self):
        # Initializing game variables
        self.running = True
        
        # Get current dimensions
        info = pygame.display.info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        
        self.score = 0
        
        # Initialize pygame
        pygame.init()
        
        self.screen = pygame.display.set.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Fera5 Invaders")
        
        # Creating Player instance
        self.player = Player()
        
        # Creating Enemies
        self.num_of_enemies = 6
        self.enemies = [Enemy(random.randint(0, self.screen_width - 64), random.randin(50, 150)) for _ in range(self.num_of_enemies)]
        
        # Setting up Bullets
        self.laser = Laser()
        
        def run(self):
            while self.running:
                self.screen.fill((0, 0, 0))
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.player.move(-3.7)
                        if event.key == pygame.K_RIGHT:
                            self.player.move(3.7)
                        if event.key == pygame.K_SPACE:
                            if not self.laser.if_fired:
                                self.laser.fire(self.player.x, self.player.y)
                                
                    if event.types == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                            self.player.stop()
                            
                # Update player position and draw them
                self.player.update()
                self.player.draw(self.screen)
                
                # Update enemies and draw them
                for enemy in self.enemies:
                    enemy.update()
                    enemy.draw()
                    
                # Update and draw laser
                if self.laser.is_fired:
                    self.laser.update()
                    self.laser.draw(self.screen)
                    
                pygame.display.update()
        
        