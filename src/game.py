# Game class handling game logic

import pygame
import random

# Class imports
from player import Player
from enemy import Chicken
from environment.sprite import Sprite

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        try:
            # Get current dimensions
            info = pygame.display.Info()
            self.screen_width = min(info.current_w, 1920)  # Cap at reasonable size
            self.screen_height = min(info.current_h, 1080)
            
            # Create screen with fallback
            try:
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            except pygame.error:
                print("Failed to create full-screen window, trying windowed mode")
                self.screen_width = 1280
                self.screen_height = 720
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                
            pygame.display.set_caption("Fera5 Invaders")
            
            self.running = True
            self.score = 0

            # Create game objects
            self.player = Player()
            self.enemies = []
            
            # Create enemies with error handling
            self.num_of_enemies = 6
            for i in range(self.num_of_enemies):
                try:
                    x = (i % 3) * 200 + 100
                    y = (i // 3) * 100 + 50
                    self.enemies.append(Chicken(x, y))
                except Exception as e:
                    print(f"Failed to create enemy {i}: {e}")
                    
        except Exception as e:
            print(f"Game initialization error: {e}")
            raise
    
    def check_collisions(self):
        # Check laser collisions with enemies 
        for enemy in self.enemies[:]:
            for laser in self.player.lasers[:]:
                if laser.rect.colliderect(enemy.rect):
                    laser.engage()
                    enemy.killChicken()
                    self.score += 100
                    if not enemy.isChickenAlive:
                        self.enemies.remove(enemy)
                    break
                        
    def run(self):
        clock = pygame.time.Clock() # To keep the framerate consistent
        
        while self.running:
            clock.tick(60) # FPS limit (can change later)
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
                        self.player.shoot()
                            
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.player.stop()
                        
            # Update player position and draw them
            self.player.update()
            self.player.draw(self.screen)
            
            # Update enemies and draw them
            for enemy in self.enemies:
                enemy.update(self.screen_width, self.screen_height)
                enemy.draw(self.screen)
                
            # Check collisions
            self.check_collisions()
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
                
            pygame.display.flip()
    
    