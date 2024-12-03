from player import Player
from enemy import Chicken
from game import Game
from random import random
import tensorflow as tf
import gymnasium as gym
import numpy as np
from random import choice
from random import sample



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

    def get_state(self):
        # Player position
        # Chicken position
        # Bullets position
        # Egg position
        # Powerups and their positions
        # Fera5 matboo5a position
        state = []
        state.append(self.game.player.rect.x)
        state.append(self.game.player.rect.y)
        
        for chicken in self.game.enemies:
            state.append(chicken.rect.x)
            state.append(chicken.rect.y)
            for egg in chicken.eggs:
                state.append(egg.rect.x)
                state.append(egg.rect.y)

        for laser in self.player.lasers:
            state.append(laser.rect.x)
            state.append(laser.rect.y)

        return state
        

class AI:
    def __init__(self, environment, alpha, epsilon, model):
        self.environment = environment
        self.alpha = alpha
        self.epsilon = epsilon
        self.model=model
        self.decay_rate = 0.02
        self.replay_memory = []
        self.memory_capacity = 10000
        self.batch_size = 32
    
    def get_input_layer(self):
        self.input_nodes = self.environment.input_nodes()
        return self.input_nodes
    
    def get_action(self):
        state = self.environment.get_state()
        state = np.array(state).reshape(1,-1)

        probability = np.random.random()

        if probability <= self.epsilon:
            # implement exploration logic here
            action = choice[self.environment.available_actions()]
        
        else:
            # implement exploitation logic here
            q_values = self.model.predict(state)
            actions = self.environment.available_actions()
            action_index = np.argmax(q_values[0])
            action = actions[action_index]
            
        return action
    

    def train(self, gamma):
        if len(self.replay_memory < self.batch_size):
            return
        batch = sample(self.replay_memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        states = np.array(states)
        next_states = np.array(next_states)
        q_values = np.array(rewards)
        next_q_values = self.model.predict(next_states)

        for i in range(self.batch_size):
            if dones[i]:
                q_values[i][actions[i]] = rewards[i]
            else:
                max = np.argmax(next_q_values)
                q_values[i][actions[i]] =  rewards[i] + gamma * next_q_values[max]

        self.model.fit(states, q_values, verbose = 1)

        
    # state, action, reward, next_state, done
    def store_experience(self, state, action, reward, next_state, done):
        if len(self.replay_memory) > self.memory_capacity:
            self.replay_memory.pop(0)
        self.replay_memory.append((state, action, reward, next_state, done))
    
    def update_epsilon(self):
        self.epsilon = max(0, self.epsilon - (self.epsilon * self.decay_rate))

    def save_model(self, file_path):
        self.model.save(file_path)

    def load_model(self, file_path):
        self.model.load(file_path)




class DQNMODEL(tf.keras.Model):
    def __init__(self, input_size, num_actions):
        super(DQNMODEL, self).__init__()
        self.dense1 = tf.keras.Model.layers.Dense(64, activation = 'relu', input_shape = (self.environment.input_nodes()))
        self.dense2 = tf.keras.Model.layers.Dense(32, activation='relu')
        self.dense3 = tf.keras.Model.layers.Dense(16, activation = 'relu')

    def call(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        return self.dense3(x)



        

        
    
    

    