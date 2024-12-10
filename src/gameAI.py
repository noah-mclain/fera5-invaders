import game
import player
import pygame
from ai.ai_env import ai_env
from enemy import Chicken
from environment.heart import Heart
from ai.ai import AI
from ai.DQNMODEL import DQNMODEL
from player import Player

class GameAI(game.Game):
    def __init__(self):
        super().__init__()
        self.environment = ai_env(self)
        self.input_size =self.environment.input_nodes()
        self.network = DQNMODEL(num_actions=4)
        self.agent = AI(self.environment, 0.1, 1, self.network)
        self.experience_count = 0

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            self.experience_count+=1
            action = self.agent.get_action()
            if action == "shoot":
                action_number = 0
            elif action == "stop":
                action_number = 1
            elif action == "right":
                action_number = 2
            else:
                action_number = 3
            state = self.environment.get_state()
            # left, right, shoot , stop
            next_state, reward, done =self.environment.step(action)
            self.agent.store_experience(state,action, reward, next_state, done)
            if self.experience_count == 400:
                self.agent.train(0.7)
                self.experience_count=0
            

            self.check_collisions()
            self.update_game_state()
            self.render_game_state()
            if len(self.enemies) == 0:
                self.level_finished()

    def game_over(self):
        for enemy in self.enemies.sprites():
            for chicken in self.all_sprites:
                if isinstance(chicken, Chicken):
                    for egg in enemy.eggs[:]:
                        egg._remove_sprite()
            enemy._remove_sprite()
        self.enemies.empty()
            
        for laser in self.player.lasers:
            laser.kill()
            
        self.player.kill()
        self.reset()
       
    def reset(self):
        self.frozen = True 
        self.frozen_start_time = pygame.time.get_ticks()
        self.current_round = 1
        # print(f"All chickens defeated! Starting round {self.current_round}...")
        self.enemies.empty()
        self.player = Player(self.screen_width, self.screen_height)
        self.environment.reassign_player(self.player)
        
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
                
        self.setup_enemy_grid()

     #resets the game/round
    def level_finished(self):
        # self.score = 0
        # self.player = player.Player(self.screen_width, self.screen_height)
        self.handle_all_chickens_dead()
    
    def check_collisions(self):
        for enemy in self.enemies.sprites():
            for laser in self.player.lasers[:]:
                if laser.rect.colliderect(enemy.rect):
                    if enemy.current_state == "alive":  # Increment score only if alive
                        laser.engage()
                        enemy.killChicken()
                        enemy.update(self.screen_width, self.screen_height)
                        self.environment.hit_enemies = 1
                        self.player.score += 100
                    break
                
        for enemy in self.enemies:
            if enemy.current_state == "food":
                if enemy.rect.colliderect(self.player.rect):
                    xp_gain = enemy.get_xp()  
                    if xp_gain > 0:
                        #print(f"Gained {xp_gain} XP from food")
                        self.player.add_xp(xp_gain)
                        self.environment.eaten_chicken +=1
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
                            self.environment.egg_hit_by_laser+=1
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
                                self.environment.player_hit_by_egg+=1
                            
                            # Check if player is alive after losing life
                            if not self.player.is_alive():
                                #print("Player has no lives left.")
                                self.environment.player_death = True
                                self.game_over()  # Call game over to rest the round
                                
                        else:
                            # print("Player has no lives left.")
                            self.environment.player_death = True
                            self.game_over()
                            
                            
                        # Do not mark as disappeared immediately; let animation play first
                        #egg.isDisappear = True
                        egg.breakEgg()  

                # Remove the egg from all sprites and enemy eggs if it should disappear
                if egg.should_disappear():
                    enemy.eggs.remove(egg)  # Remove from enemy's eggs list
                    self.all_sprites.remove(egg)  # Remove from all sprites group
                
            