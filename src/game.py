import pygame
import random
from os import path

# Class imports
from player import Player
from enemy import Chicken
from environment.sprite import StaticSprite
from powerup import PowerUp  # Added to handle power-ups

class Game:
    def __init__(self):
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
            self.paused = False  # Updated: Pause functionality
            self.score = 0
            self.all_chickens_dead = False  # Added: To track when all chickens are dead

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
            self.num_of_enemies = 30
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

        # Added: Check if all chickens are dead
        if Chicken.get_chicken_count() == 0 and not self.all_chickens_dead:
            self.all_chickens_dead = True
            self.handle_all_chickens_dead()

    # Added: Handle actions when all chickens are dead
    def handle_all_chickens_dead(self):
        """
        - Increment score by 10,000.
        - Respawn chickens with flicker effect.
        - Increment player's power-up.
        """
        self.score += 10000
        print("All chickens defeated! Respawning...")

        # Apply flicker effect to the player
        self.player._play_powerup_effect()

        # Respawn new chickens
        self.setup_enemy_grid()
        self.apply_chicken_flicker_effect()

        # Increment player's power-up (laser count)
        powerup = PowerUp("increment_laser", laser_increment=1)
        self.player.apply_powerup(powerup)

        # Reset the flag for chicken respawn
        self.all_chickens_dead = False

    # Added: Flicker effect for chickens
    def apply_chicken_flicker_effect(self):
        """
        Apply a flicker effect to all newly respawned chickens.
        """
        flicker_duration = 1500  # 1.5 seconds
        flicker_interval = 100   # 100ms interval
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < flicker_duration:
            for chicken in self.enemies:
                chicken.set_alpha(0)  # Make chickens invisible
            pygame.time.delay(flicker_interval // 2)
            for chicken in self.enemies:
                chicken.set_alpha(255)  # Make chickens visible
            pygame.time.delay(flicker_interval // 2)

    def game_over(self):
        self.running = False

    def toggle_pause(self):
        self.paused = not self.paused

    def run(self):
        print("Game loop started.")
        clock = pygame.time.Clock()  # Keep framerate consistent
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
                        
            if not self.paused:
                self.update_game_state()
                self.render_game_state()

    def update_game_state(self):
        self.player.update(self.screen_width, self.screen_height)

        for laser in self.player.lasers:
            if laser not in self.all_sprites:
                self.all_sprites.add(laser)
                self.lasers.add(laser)
            laser.update(self.screen_width, self.screen_height)

        for laser in self.lasers.copy():
            if not laser.is_fired:
                self.all_sprites.remove(laser)
                self.lasers.remove(laser)

        for enemy in self.enemies:
            enemy.update(self.screen_width, self.screen_height)
            if enemy.current_state == "alive" and random.random() < 0.01:
                enemy.lay_eggs(self.all_sprites)

        self.all_sprites.draw(self.screen)
        self.check_collisions()

    def render_game_state(self):
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.render_lives()
        self.render_scores()
        pygame.display.flip()

    def render_lives(self):
        heart_image = pygame.image.load("assets/images/background/heart.png")
        heart_image = pygame.transform.scale(heart_image, (40, 40))
        for i in range(self.player.lives):
            self.screen.blit(heart_image, (self.screen_width - (i + 1) * 50, 10))

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
