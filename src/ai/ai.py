from player import Player
from enemy import Chicken
from game import Game
from random import random
import tensorflow as tf
import gymnasium as gym
import numpy as np
from random import choice
from random import sample


class AI:
    """
    initializing the AI model with its own replay buffer
    """
    def __init__(self, environment, alpha, epsilon, model):
        self.environment = environment
        self.alpha = alpha 
        self.epsilon = epsilon
        self.model=model
        
        self.model.compile(optimizer='adam', loss='mse')
        self.decay_rate = 0.005
        self.replay_memory = []
        self.memory_capacity = 10000
        self.batch_size = 128
        self.min_epsilon = 0.1
    
    
    """retrieves the input nodes from class ai_env"""
    def get_input_layer(self):
        self.input_nodes = self.environment.input_nodes()
        return self.input_nodes
    
    """decides which action to take, exploit or explore, and the espilon's value decreases gradually to increase the probability of exploitation """
    def get_action(self):
        state = self.environment.get_state()
        max_shape = self.environment.input_nodes()
        state = [np.pad(state, (0, max(0, max_shape - len(state))), constant_values=0)]

        probability = np.random.random()
        #print(probability)

        if probability <= self.epsilon:
            # implement exploration logic here
            #print("Exploring!")
            actions = self.environment.available_actions()
            action = choice(actions)
            #print(action)
        
        else:
            # implement exploitation logic here
            #print("Exploiting!")
            q_values = self.model.predict(np.stack(state))
            actions = self.environment.all_actions()
            action_index = np.argmax(q_values[0]) # noah hatesss wewe
            action = actions[action_index]
        return action
    
    """
    retrieves past experiences in batches, and uses the Q-values learnt from these experience to adjust the neural network's internal weights using back propagation
    """
    def train(self, gamma):
        if len(self.replay_memory) < self.batch_size:
            return
        batch = sample(self.replay_memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        #states = [np.array(state, dtype=np.float32) for state in states] 
        #next_states = [np.array(next_state, dtype=np.float32) for next_state in next_states]
        q_values = np.array([np.zeros(4, dtype=np.float32) for _ in range(self.batch_size)])
        max_shape = self.environment.input_nodes()
        states = [np.pad(array, (0, max(0, max_shape - len(array))), constant_values=0) for array in states]
        next_states = [np.pad(array, (0, max(0,max_shape - len(array))), constant_values=0) for array in next_states]
        # print(states)
        #states = np.array(states, dtype=np.float32)
        #next_states = np.array(next_states, dtype=np.float32)
        #q_values = np.array(rewards, dtype=np.float32)
        next_q_values = self.model(np.stack(next_states))
        mapping = {"right" : 0, "left" : 1, "shoot" : 2, "stop" : 3}
        for i in range(self.batch_size):
            if dones[i]:
                q_values[i][mapping[actions[i]]] = rewards[i]
            else:
                max_q_value = np.max(next_q_values[i])
                q_values[i][mapping[actions[i]]] =  rewards[i] + gamma * next_q_values[max_q_value]

        self.model.fit(np.stack(states), np.stack(q_values), verbose = 1)
        self.update_epsilon()
        
    # state, action, reward, next_state, done
    """stores the experiences in the replay_memory list"""
    def store_experience(self, state, action, reward, next_state, done):
        if len(self.replay_memory) > self.memory_capacity:
            self.replay_memory.pop(0)
        self.replay_memory.append((state, action, reward, next_state, done))
        #print(self.replay_memory)
        
    """decreases the Epsilon's value gradually"""
    def update_epsilon(self):
        print("function called!")
        if self.epsilon > 0.5:
            self.epsilon*=0.99
        else:
            self.epsilon = max(self.min_epsilon, self.epsilon - (self.epsilon * self.decay_rate))
        print(self.epsilon)
    
    """methods to save and load the trained AI model """
    def save_model(self, file_path):
        self.model.save(file_path)

    def load_model(self, file_path):
        self.model.load(file_path)
