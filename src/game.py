import random
from os import path

import pygame

from enemy import Chicken
from environment.heart import Heart
from environment.sprite import StaticSprite
# Class imports
from player import Player
from powerup import PowerUp  # Added to handle power-ups


class Game:
    def __init__(self):
        # print("Initializing Game...")
        # Initialize pygame
        if not pygame.get_init():
            pygame.init()
        
        try:
            # Get current dimensions
            info = pygame.display.Info()
            self.screen_width = min(info.current_w, 1920)
            self.screen_height = min(info.current_h, 1080)
            #print(f"Screen dimensions: {self.screen_width}x{self.screen_height}")
            
            # Create screen
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            if not self.screen:
                raise RuntimeError("Failed to create display")
            
            #print("Display created successfully")
            
            pygame.display.set_caption("Fera5 Invaders")
            
            self.running = True
            self.paused = False  # Updated: Pause functionality
# The above code snippet is defining a class in Python with an attribute `score` initialized to 0.
            # self.score = 0
            self.all_chickens_dead = False  # Added: To track when all chickens are dead
            self.current_round = 1
            self.round_transitioning = False
            self.round_transition_start_time =0 
            self.frozen = False  # New: Game is frozen during power-up
            self.frozen_start_time = 0
            self.freeze_duration = 3000
            
            self.all_sprites = pygame.sprite.Group()
            self.enemies = pygame.sprite.Group()
            self.lasers = pygame.sprite.Group()
           
            self.direction = 1
            self.movement_speed = 3
            
            self.player = Player(self.screen_width, self.screen_height)
            self.player.game_instance = self
            if not self.player:
                raise RuntimeError("Failed to create player")
            
            self.all_sprites.add(self.player)

            self.hearts = []
            for i in range(self.player.lives):
                # print(f"Initializing heart {i + 1} at position: ({self.screen_width - (i + 1) * 70}, 20)")
                try:
                    heart = Heart((self.screen_width - (i + 1) * 70, 20))
                    heart.rect.size = (60, 60)
                    self.hearts.append(heart)
                    self.all_sprites.add(heart)
                    # print(f"Heart {i + 1} initialized successfully.")
                except KeyError as e:
                    print(f"KeyError while initializing heart {i + 1}: {str(e)}")
                except Exception as e:
                    print(f"Error while initializing heart {i + 1}: {str(e)}")

            # self.hearts = [Heart((self.screen_width - (i + 1) * 70, 20)) for i in range(self.player.lives)]           
            # for heart in self.hearts:
            #     heart.rect.size = (60, 60) 
            #     self.all_sprites.add(heart)
                    
            self.all_sprites.add(self.player)
            self.active_powerup = None
            # Enemy grid setup
            self.setup_enemy_grid()
                    
        except Exception as e:
            # print(f"Game initialization error: {str(e)}")
            raise
    
    def setup_enemy_grid(self):
        for enemy in self.enemies.sprites():
            enemy._remove_sprite()
        self.enemies.empty()

        try:
            # Enemy grid configuration
            self.num_of_enemies = 30
            chicken_width = 50
            chicken_height = 45
            padding = 10
            left_padding = 100 
            right_padding = 100 
            max_top_padding = 50
            max_bottom_padding = 50
            
            # Calculate available height for enemies
            available_width = self.screen_width - left_padding - right_padding
            
            # Calculate grid layout
            columns = max(1, (available_width // (chicken_width + padding)))
            rows = (self.num_of_enemies + columns - 1) // columns
            
            # Calculate spacing
            spacing_x = (self.screen_width - (columns + 1) * padding) / columns
            spacing_y = (self.screen_height / 4) / rows
            
            #print(f"Creating enemy grid: {columns}x{rows}")
            #print(f"Spacing: {spacing_x}x{spacing_y}")
            
            # Create enemies
            sprite_sheet_path = path.join("assets", "images", "Enemy", "chickenRedSpriteSheet.png")
            
            # Verify sprite sheet exists
            if not path.exists(sprite_sheet_path):
                raise FileNotFoundError(f"Sprite sheet not found: {sprite_sheet_path}")
            
            enemies_created = 0
            for i in range(self.num_of_enemies):
                try:
                    x = left_padding + (i % columns) * (chicken_width + padding)
                    y = max_top_padding + (i // columns) * (chicken_height + padding) + (chicken_height / 2)
                    position = (x, y)
                    
                    chicken = Chicken(position, sprite_sheet_path)
                    self.enemies.add(chicken)
                    self.all_sprites.add(chicken)
                    enemies_created += 1
                    # print(f"Created enemy {enemies_created} at position {position}")
                    
                except Exception as e:
                    print(f"Failed to create enemy {i}: {str(e)}")
                    continue
            
            if enemies_created == 0:
                raise RuntimeError("No enemies were created successfully")
            
            #print(f"Successfully created {enemies_created} enemies")
            
        except Exception as e:
            print(f"Failed to create enemy at position {position if 'position' in locals() else 'unknown'}: {str(e)}")
            raise   
        
    def move_enemies(self):
        for chicken in self.enemies.sprites():
            new_x = chicken.rect.x + (self.direction * self.movement_speed)

            if new_x < 0 or new_x + chicken.rect.width > self.screen_width:
                self.direction *= -1  # Reverse direction
                return
            
            chicken.rect.x = new_x
        
    def check_collisions(self):
        # Check laser collisions with enemies 
        for enemy in self.enemies.sprites():
            for laser in self.player.lasers[:]:
                if laser.rect.colliderect(enemy.rect):
                    if enemy.current_state == "alive":  # Increment score only if alive
                        laser.engage()
                        enemy.killChicken()
                        enemy.update(self.screen_width, self.screen_height)
                        self.player.score += 100
                    break
        
        collected_food = set()
        for enemy in self.enemies.sprites():
            if enemy.current_state == "food":
                if enemy.rect.colliderect(self.player.rect):
                    if enemy not in collected_food:
                        xp_gain = enemy.get_xp()  
                        if xp_gain > 0:
                            # print(f"Gained {xp_gain} XP from food")
                            self.player.add_xp(xp_gain)
                            collected_food.add(enemy)
                    enemy._remove_sprite()
                        
        # Flatten the list of eggs from all the enemies
        for enemy in self.enemies:
            for egg in enemy.eggs[:]:  # Use a copy of the list to avoid modifying it during iteration
                # Check if the egg is still active
                if not egg.should_disappear():  # Use instance method
                    # Check collision with lasers
                    for laser in self.player.lasers[:]:
                        if laser.rect.colliderect(egg.rect):
                            laser.engage()
                            egg.breakEgg()  # Trigger the broken animation
                            self.player.score += 50
                            if laser in self.all_sprites:
                                self.all_sprites.remove(laser)
                            break
                    
                    # Check collision with player
                    if egg.rect.colliderect(self.player.rect) and egg.current_state == "whole":
                        if self.player.lose_life():
                            # Trigger the flickering on that heart
                            if len(self.hearts) > (self.player.lives):  
                                #print(f"Losing life: {self.player.lives}")
                                self.hearts[self.player.lives].lose_life()
                            
                            # Check if player is alive after losing life
                            if not self.player.is_alive():
                                #print("Player has no lives left.")
                                self.game_over()  # Call game over if player has no lives left
                        else:
                            #print("Player has no lives left.")
                            self.game_over()
                            
                        # Do not mark as disappeared immediately; let animation play first
                        #egg.isDisappear = True
                        egg.breakEgg()  

                # Remove the egg from all sprites and enemy eggs if it should disappear
                if egg.should_disappear():
                    enemy.eggs.remove(egg)  # Remove from enemy's eggs list
                    self.all_sprites.remove(egg)  # Remove from all sprites group

        # Added: Check if all chickens are dead
        if Chicken.get_chicken_count() == 0 and not self.all_chickens_dead:
            self.all_chickens_dead = True
            self.handle_all_chickens_dead()
            
    # Added: Handle actions when all chickens are dead
    def handle_all_chickens_dead(self):
        self.round_transitioning = True
        self.frozen = True 
        self.frozen_start_time = pygame.time.get_ticks()
        self.current_round +=1
        self.player.score += 10000
        # print(f"All chickens defeated! Starting round {self.current_round}...")

        # Create a PowerUp and store it
        self.active_powerup = PowerUp(powerup_type="increment_laser", position=self.player.rect.center, laser_increment=1)
        self.all_sprites.add(self.active_powerup)

        self.setup_enemy_grid()
        self.apply_chicken_flicker_effect()
        self.all_chickens_dead = False

    def apply_chicken_flicker_effect(self):
        flicker_duration = 1500  # 1.5 seconds
        start_time = pygame.time.get_ticks()

        def flicker():
            elapsed_time = pygame.time.get_ticks() - start_time
            visible = (elapsed_time // 100) % 2 == 0
            for chicken in self.enemies:
                chicken.set_alpha(255 if visible else 0)

        while pygame.time.get_ticks() - start_time < flicker_duration:
            flicker()
            pygame.time.delay(50)
        
    def game_over(self):
        ##YA MALAAAAKAKKK WRITE HERE THE LOGIC FOR THE EXIT MENUUU
        ##le7ad ma teegy ha7ot replacement code 
        font = pygame.font.Font(None, 72)
        message = "Game Over!" if self.player.lives == 0 else "You Win!"
        text = font.render(message, True, (255, 0, 0))
        self.screen.fill((0, 0, 0))
        self.screen.blit(text, (self.screen_width // 2 - 100, self.screen_height // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        self.running = False

    def toggle_pause(self):
        self.paused = not self.paused
  
    def run(self):
        # print("Game loop started.")
        clock = pygame.time.Clock() 
        
        while self.running:
            clock.tick(60)
            #keys = pygame.key.get_pressed()
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
                self.check_collisions()
                self.update_game_state()
                self.render_game_state()
            else:
                font = pygame.font.Font(None, 48)
                pause_text = font.render("Game paused (Press P to resume)", True, (255,255,255))
                self.screen.fill((0, 0, 0))
                self.screen.blit(pause_text, (self.screen_width // 2 - 200, self.screen_height // 2))
                pygame.display.flip()
        
    def update_game_state(self):       
        self.player.update(self.screen_width, self.screen_height)
        for heart in self.hearts:
            heart.update()
        
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
                if random.random() < 0.001:
                    enemy.lay_eggs(self.all_sprites)

        self.move_enemies()
                    
        # Draw all sprites
        for sprite in self.all_sprites:
            if not hasattr(sprite, "image") or not isinstance(sprite.image, pygame.Surface):
                print(f"Invalid sprite: {sprite}, type: {type(sprite)}")

         # Check if power-up is done animating and apply to player
        if self.active_powerup and self.active_powerup.isAnimationDone():
            self.active_powerup.apply_to_player(self.player)
            self.all_sprites.remove(self.active_powerup)
            self.active_powerup = None

        # If still frozen, handle freeze logic
        if self.frozen:
            current_time = pygame.time.get_ticks()
            if current_time - self.frozen_start_time > self.freeze_duration:
                self.frozen = False
                self.round_transitioning = False
                self.setup_enemy_grid()
            return
                        
        self.all_sprites.draw(self.screen)
                 
    def render_game_state(self):
        self.screen.fill((0,0,0))
        self.player.draw(self.screen)
        
        self.all_sprites.draw(self.screen)
        
        for i in range(self.player.lives):
            if i < len(self.hearts):
                self.hearts[i].draw(self.screen)
            
        if self.active_powerup:
            self.active_powerup.draw(self.screen)
            self.active_powerup.update()
        self.render_scores()
        self.render_xp()
        self.render_round_number()
        pygame.display.flip()
        
    def render_round_number(self):
        font = pygame.font.Font(None, 48)
        round_text = font.render(f"Round: {self.current_round}", True, (255, 255, 255))
        self.screen.blit(round_text, (10, 50))  # Position below the score
        
    def display_victory_message(self):
        font = pygame.font.Font(None, 72)
        victory_text = font.render("You Win!", True, (0, 255, 0))
        self.screen.fill((0, 0, 0))
        self.screen.blit(victory_text, (self.screen_width // 2 - 100, self.screen_height // 2))
        pygame.display.flip()
        pygame.time.delay(3000)  

    def render_scores(self):
        score_image_path = path.join("assets", "images", "scores1.png")  
        score_sheet = pygame.image.load(score_image_path).convert_alpha()

        digit_width = score_sheet.get_width() // 10
        digit_height = score_sheet.get_height()
        digits = [score_sheet.subsurface(pygame.Rect(i * digit_width, 0, digit_width, digit_height)) for i in range(10)]
        score_str = str(self.player.score)
        x_offset = 10
        y_offset = 10

        for digit in score_str:
            digit_surface = digits[int(digit)]
            self.screen.blit(digit_surface, (x_offset, y_offset))
            x_offset += digit_width + 2

    def render_xp(self):
        xp_image_path = path.join("assets", "images", "scores1.png")  
        xp_sheet = pygame.image.load(xp_image_path).convert_alpha()

        digit_width = xp_sheet.get_width() // 10
        digit_height = xp_sheet.get_height()

        digits = [xp_sheet.subsurface(pygame.Rect(i * digit_width, 0, digit_width, digit_height)) for i in range(10)]

        xp_str = str(self.player.xp)
        x_offset = 30
        y_offset = 30 

        font = pygame.font.Font(None, 36) 
        label_surface = font.render("XP: ", True, (255, 255, 255))  
        self.screen.blit(label_surface, (x_offset, y_offset))

        x_offset += label_surface.get_width() 

        for digit in xp_str:
            digit_surface = digits[int(digit)] 
            self.screen.blit(digit_surface, (x_offset, y_offset)) 
            x_offset += digit_width + 2  