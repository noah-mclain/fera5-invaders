# Game class handling game logic

import pygame
import random

# Class imports
from player import Player
from enemy import Chicken
from laser import Laser

class Game:
    def __init__(self):
        print("Initializing Game...")
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
        self.paused = False
        self.score = 0

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
        for enemy in self.enemies[:]:
            for laser in self.player.lasers[:]:
                if laser.rect.colliderect(enemy.rect):
                    laser.engage()
                    enemy.killChicken()
                    self.score += 100
                    if not enemy.isChickenAlive:
                        self.enemies.remove(enemy)
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
            self.player.update()
            for enemy in self.enemies:
                enemy.update(self.screen_width, self.screen_height)
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
    