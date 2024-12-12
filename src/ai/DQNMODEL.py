"""
A neural network model that will simulate Q-learning using a neural network
"""
import tensorflow as tf

class DQNMODEL(tf.keras.Model):
    """ initializing the model using keras' layers class """
    def __init__(self, num_actions):
        super(DQNMODEL, self).__init__()
        self.dense1 = tf.keras.layers.Dense(128, activation = 'relu')
        self.dense2 = tf.keras.layers.Dense(64, activation='relu')
        self.dense3 = tf.keras.layers.Dense(32, activation = 'relu')
        self.dropout1 = tf.keras.layers.Dropout(0.5)
        self.dense4 = tf.keras.layers.Dense(16, activation = 'relu')
        self.outputLayer=tf.keras.layers.Dense(num_actions,activation=None)
        
    """ Overriding DQN'S call function"""    
    def call(self, state):
        x = self.dense1(state)
        x = self.dense2(x)
        x = self.dense3(x)
        x = self.dropout1(x)
        x = self.dense4(x)
        return self.outputLayer(x)
    
    """ methods that will save and load the weights that the network will learn"""
    def save_model(self, file_path):
        self.save_weights(file_path)

    def load_model(self, file_path):
        self.load_weights(file_path)