from player import Player
from enemy import Chicken
from game import Game
from random import random
import tensorflow as tf
import gymnasium as gym
import numpy as np
from random import choice
from random import sample
import keras

class AI:
    """
    initializing the AI model with its own replay buffer
    """
    def __init__(self, environment, alpha, epsilon, model):
        self.environment = environment
        self.alpha = alpha
        self.epsilon = epsilon
        self.model=model
        self.decay_rate = 0.02
        self.replay_memory = []
        self.memory_capacity = 10000
        self.batch_size = 32
    
    
    """retrieves the input nodes from class ai_env"""
    def get_input_layer(self):
        self.input_nodes = self.environment.input_nodes()
        return self.input_nodes
    
    """decides which action to take, expolit or explore, and the espilon's value decreases gradually to increase the probability of exploitation """
    def get_action(self):
        state = self.environment.get_state()
        state = np.array(state).reshape(1,-1)

        probability = np.random.random()

        if probability <= self.epsilon:
            # implement exploration logic here
            print(self.environment.available_actions())
            print(self.epsilon)
            action = choice(self.environment.available_actions())
        
        else:
            # implement exploitation logic here
            q_values = self.model.predict(state)
            actions = self.environment.available_actions()
            action_index = np.argmax(q_values[0])
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
        for i, state in enumerate(states):
            print(len(state))
        print("5alasna!")
        padded_states = keras.pad_sequences(states, padding='post')  # Pads with zeros at the end
        states_array = np.array(padded_states)
        padded_new_states = keras.pad_sequences(padded_new_states, padding='post')
        padded_new_states=np.array(padded_new_states)
        states = np.array(states_array).flatten()
        next_states = np.array(padded_new_states).flatten()
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
    """stores the experiences in the replay_memory list"""
    def store_experience(self, state, action, reward, next_state, done):
        if len(self.replay_memory) > self.memory_capacity:
            self.replay_memory.pop(0)
        self.replay_memory.append((state, action, reward, next_state, done))
        print(self.replay_memory)
        
    """decreases the Epsilon's value gradually"""
    def update_epsilon(self):
        self.epsilon = max(0, self.epsilon - (self.epsilon * self.decay_rate))

    
    """methods to save and load the trained AI model """
    def save_model(self, file_path):
        self.model.save(file_path)

    def load_model(self, file_path):
        self.model.load(file_path)

    