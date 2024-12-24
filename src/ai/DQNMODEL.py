"""
A neural network model that will simulate Q-learning using a neural network
"""
import tensorflow as tf

class DQNMODEL(tf.keras.Model):
    """ initializing the model using keras' layers class """
    def __init__(self, num_actions: int):
        super(DQNMODEL, self).__init__()
        self.dense1 = tf.keras.layers.Dense(128, activation = 'relu', input_shape=(990,))
        self.bn1 = tf.keras.layers.BatchNormalization()
        self.dense2 = tf.keras.layers.Dense(64, activation='relu')
        self.dropout1 = tf.keras.layers.Dropout(0.5)
        self.dense3 = tf.keras.layers.Dense(32, activation = 'relu')
        self.dropout2 = tf.keras.layers.Dropout(0.3)
        self.dense4 = tf.keras.layers.Dense(16, activation = 'relu')
        self.outputLayer=tf.keras.layers.Dense(num_actions,activation=None)
        
    """ Overriding DQN'S call function""" 
    #pass input from layer to layer   
    def call(self, state: tf.Tensor) -> tf.Tensor:
        x = self.dense1(state)
        x = self.bn1(x)
        x = self.dense2(x)
        x = self.dropout1(x, training=True)
        x = self.dense3(x)
        x = self.dropout2(x, training=True)
        x = self.dense4(x)
        return self.outputLayer(x)
    
    def build_model(self, input_shape):
        self.build(input_shape)
        
    """ methods that will save and load the weights that the network will learn"""
    def save_model(self, file_path):
        self.save_weights(file_path)

    def load_model(self, file_path):
        try:
            self.load_weights(file_path)
        except Exception as e:
            print(f"Error loading model weights: {e}")