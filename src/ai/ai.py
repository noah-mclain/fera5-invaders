from player import Player
from enemy import Chicken
from game import Game
from random import random
import tensorflow as tf


class ai_env:
    def __init__(self, game):
        self.player = game.player
        self.enemies = game.enemies
        self.score = 0
        self.actions=["right", "left", "shoot", "stop"]
        
               
    def available_actions(self):
        available_actions = ["shoot", "stop"]
        if self.player.rect.x < self.game.screen_width:
            available_actions.append["left"]
        if self.player.rect.x > 0:
            available_actions.append["right"]

class AI:
    def __init__(self, environment, alpha, epsilon):
        self.environment = environment
        self.alpha = alpha
        self.epsilon = epsilon