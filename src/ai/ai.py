from player import Player
from enemy import Chicken
from game import Game
from random import random
import tensorflow as tf
import gymnasium as gym



class ai_env:
    def __init__(self, game):
        self.player = game.player
        self.enemies = game.enemies
        self.score = 0
        self.actions=["right", "left", "shoot", "stop"]  
        
               
    def available_actions(self):
        available_actions = ["shoot", "stop"]
        if self.player.rect.x < self.game.screen_width:
            available_actions.append("left")
        if self.player.rect.x > 0:
            available_actions.append("right")
    
    def input_nodes(self):
        player_nodes = 2
        MAX_chicken_nodes = 40 * 2
        MAX_egg_nodes = MAX_chicken_nodes
        MAX_laser_nodes = 20
        MAX_powerups_nodes = 6
        total_nodes = player_nodes + MAX_chicken_nodes + MAX_egg_nodes + MAX_laser_nodes + MAX_powerups_nodes
        return total_nodes



class AI:
    def __init__(self, environment, alpha, epsilon):
        self.environment = environment
        self.alpha = alpha
        self.epsilon = epsilon
    
    def get_input_layer(self):
        self.input_nodes = self.environment.input_nodes()
        return self.input_nodes

class DQNMODEL(tf.keras.Model):
    def __init__(self, input_size, num_actions):
        super(DQNMODEL, self).__init__()
        

        
    
    

    