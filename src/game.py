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
        print("Initializing Game...")
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
            # Get current dimensions
            info = pygame.display.Info()
            self.screen_width = info.current_w
            self.screen_height = info.current_h
            
            # Create screen
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption("Fera5 Invaders")
            
            self.running = True
            self.paused = False
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
    
        # Creating Player instance
        self.player = Player()
        # Creating Enemies
        self.num_of_enemies = 18
        self.enemies = []
        for i in range(self.num_of_enemies):
            x = (i // 3) * 200 + 100
            y = (i % 3) * 100 + 50
            self.enemies.append(Chicken(x, y))
        
        
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
        # Flatten the list of eggs from all the enemies
        for egg in [egg for enemy in self.enemies for egg in enemy.eggs]:
            for laser in self.player.lasers[:]:
                if laser.rect.colliderect(egg.rect):
                    laser.engage()
                    egg.breakEgg()
                    self.all_sprites.remove(laser)
                    break
            for egg in enemy.eggs:
                if egg.rect.colliderect(self.player.rect):
                    self.player.lose_life()
                    egg.isDisappear = True
                    if not self.player.is_alive():
                        self.game_over()

    def game_over(self):
        self.running = False
        # make this into a main menu b2a 

    def toggle_pause(self):
        self.paused = not self.paused
    def run(self):
        print("Game loop started.")
        clock = pygame.time.Clock() # To keep the framerate consistent
        while self.running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Pause button
                        self.toggle_pause()
                    if not self.paused:  # Handle other keys when not paused
                        if event.key == pygame.K_LEFT:
                            self.player.move(-3.7)
                        if event.key == pygame.K_RIGHT:
                            self.player.move(3.7)
                        if event.key == pygame.K_SPACE:
                            self.player.shoot()
                if event.type == pygame.KEYUP:
                    if not self.paused and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                        self.player.stop()
                        
            
            
            # Update enemies
            if not self.enemies:
                self.display_victory_message()
                self.running = False
                
            
            if not self.paused:
                self.update_game_state()
                self.render_game_state()
            else:
                font = pygame.font.Font(None, 48)
                pause_text = font.render("Game paused (Press P to resume)", True, (255,255,255))
                self.screen.blit(pause_text, (self.screen.width // 2 - 200, self.screen_height // 2))
                pygame.display.flip()
            
            
                
            
    def update_game_state(self):       
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
            
    
    def render_game_state(self):
        self.screen.fill((0,0,0))
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.render_lives()
        self.render_scores()
        pygame.display.flip()
        
        
    def render_lives(self):
        heart_image = pygame.image.load("assets/images/background/heart.png")
        heart_image = pygame.transform.scale(heart_image, (40, 40))
        for i in range(self.player.lives):
            self.screen.blit(heart_image, (self.screen_width - (i+1)*50, 10))
            
            
            
    def display_victory_message(self):
        font = pygame.font.Font(None, 72)
        victory_text = font.render("You Win!", True, (0, 255, 0))
        self.screen.fill((0, 0, 0))
        self.screen.blit(victory_text, (self.screen_width // 2 - 100, self.screen_height // 2))
        pygame.display.flip()
        pygame.time.delay(3000)  

    def render_scores(self):
        score_image_path = "assets/images/scores1.png"  
        score_sheet = pygame.image.load(score_image_path).convert_alpha()

        digit_width = score_sheet.get_width() // 10 
        digit_height = score_sheet.get_height()
        digits = [score_sheet.subsurface(pygame.Rect(i * digit_width, 0, digit_width, digit_height)) for i in range(10)]
        score_str = str(self.score)
        x_offset = 10 
        y_offset = 10 

        for digit in score_str:
            digit_surface = digits[int(digit)]  
            self.screen.blit(digit_surface, (x_offset, y_offset))
            x_offset += digit_width + 2 
    