# Game class handling game logic

import pygame
import random

# Class imports
from player import Player
#from enemy import Enemy
from laser import Laser

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        
        # Get current dimensions
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        
        # Create screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Fera5 Invaders")
        
        self.running = True
        self.score = 0

        # Creating Player instance
        self.player = Player()
        
        # Creating Enemies
        self.num_of_enemies = 6
        '''self.enemies = [
                Enemy(
                    random.randint(0, self.screen_width - 64), 
                    random.randint(50, 150)
                ) for _ in range(self.num_of_enemies)
            ]'''
        
    '''def check_collisions(self):
        # Check laser collisions with enemies 
        for enemy in self.enemies[:]:
            for laser in self.player.lasers[:]:
                if laser.rect.colliderect(enemy.rect):
                    laser.engage()
                    enemy.die()
                    self.score += 100
                    self.enemies.remove(enemy)
                    break'''
                        
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
            '''for enemy in self.enemies:
                enemy.update()
                enemy.draw(self.screen)'''
                
            # Check collisions
            #self.check_collisions()
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
                
            pygame.display.flip()
    
    