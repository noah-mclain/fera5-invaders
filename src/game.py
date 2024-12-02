# Game class handling game logic

import pygame
import random
from os import path

# Class imports
from player import Player
from enemy import Chicken
from environment.sprite import StaticSprite

class Game:
    def __init__(self):
        print("Initializing game...")
        # Initialize pygame
        if not pygame.get_init():
            pygame.init()
        
        try:
            # Get current dimensions
            info = pygame.display.Info()
            self.screen_width = min(info.current_w, 1920)
            self.screen_height = min(info.current_h, 1080)
            print(f"Screen dimensions: {self.screen_width}x{self.screen_height}")
            
            # Create screen
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            if not self.screen:
                raise RuntimeError("Failed to create display")
            
            print("Display created successfully")
            
            pygame.display.set_caption("Fera5 Invaders")
            
            self.running = True
            self.score = 0

            # Create sprite groups
            self.all_sprites = pygame.sprite.Group()
            self.enemies = pygame.sprite.Group()
            self.lasers = pygame.sprite.Group()
            
            # Create static sprite
            self.player = Player(self.screen_width, self.screen_height)
            if not self.player:
                raise RuntimeError("Failed to create player")
                
            self.all_sprites.add(self.player)
            
            # Enemy grid setup
            self.setup_enemy_grid()
                    
        except Exception as e:
            print(f"Game initialization error: {str(e)}")
            raise
    
    def setup_enemy_grid(self):
        try:
            # Enemy grid configuration
            self.num_of_enemies = 2
            chicken_width = 40
            chicken_height = 35
            
            # Calculate grid layout
            columns = max(1, (self.screen_width // chicken_width) - 2)
            rows = max(1, (self.num_of_enemies + columns - 1) // columns)
            
            # Calculate spacing
            spacing_x = self.screen_width / (columns + 1)
            spacing_y = (self.screen_height / 3) / (rows + 1)
            
            print(f"Creating enemy grid: {columns}x{rows}")
            print(f"Spacing: {spacing_x}x{spacing_y}")
            
            # Create enemies
            sprite_sheet_path = path.join("assets", "images", "Enemy", "chickenRedSpriteSheet.png")
            
            # Verify sprite sheet exists
            if not path.exists(sprite_sheet_path):
                raise FileNotFoundError(f"Sprite sheet not found: {sprite_sheet_path}")
            
            enemies_created = 0
            for i in range(self.num_of_enemies):
                try:
                    x = (i % columns) * spacing_x + spacing_x
                    y = (i // columns) * spacing_y + spacing_y
                    position = (x, y)
                    
                    chicken = Chicken(position, sprite_sheet_path)
                    self.enemies.add(chicken)
                    self.all_sprites.add(chicken)
                    enemies_created += 1
                    print(f"Created enemy {enemies_created}")
                    
                except Exception as e:
                    print(f"Failed to create enemy {i}: {str(e)}")
                    continue
            
            if enemies_created == 0:
                raise RuntimeError("No enemies were created successfully")
            
            print(f"Successfully created {enemies_created} enemies")
            
        except Exception as e:
            print(f"Error setting up enemy grid: {str(e)}")
            raise
    
    def check_collisions(self):
        # Check laser collisions with enemies 
        for enemy in self.enemies.sprites():
            for laser in self.player.lasers[:]:
                if laser.rect.colliderect(enemy.rect):
                    laser.engage()
                    enemy.killChicken()
                    enemy.update(self.screen_width, self.screen_height)
                    self.score += 100
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
                        
            # Update sprites
            self.player.update(self.screen_width, self.screen_height)
            
            # Update and add new lasers to sprite groups
            for laser in self.player.lasers:
                if laser not in self.all_sprites:
                    self.all_sprites.add(laser)
                    self.lasers.add(laser)
                laser.update(self.screen_width, self.screen_height)
            
            # Remove dead lasers from sprite groups
            for laser in self.lasers.copy():
                if not laser.is_fired:
                    self.all_sprites.remove(laser)
                    self.lasers.remove(laser)
            
            # Update enemies
            for enemy in self.enemies:
                enemy.update(self.screen_width, self.screen_height)
                if enemy.current_state == "alive":
                     # Laying those eggs
                    if random.random() < 0.01:
                        enemy.lay_eggs(self.all_sprites)
                    
            # Draw all sprites
            self.all_sprites.draw(self.screen)
                
            # Check collisions
            self.check_collisions()
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
                
            pygame.display.flip()
    
    