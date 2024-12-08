import game
import player
import pygame
from ai.ai_env import ai_env
from ai.ai import AI
from ai.DQNMODEL import DQNMODEL
class GameAI(game.Game):
    def __init__(self):
        super().__init__()
        self.environment = ai_env(self)
        self.input_size =self.environment.input_nodes()
        self.network = DQNMODEL(self.input_size, 4)
        self.agent = AI(self.environment, 0.1, 1, self.network)
        self.count = 0

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60) 
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
            self.agent.store_experience(state,action_number, reward, next_state, done)
            self.check_collisions()
            self.update_game_state()
            self.render_game_state()
            self.count+=1
            if self.count >= 100:
                self.agent.train(0.7)
                self.count = 0



            
    #resets the game/round
    def game_over(self):
        self.score = 0
        self.enemies = []
        self.player = player.Player(self.screen_width, self.screen_height)
        self.setup_enemy_grid()