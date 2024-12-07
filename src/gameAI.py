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

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            action = self.agent.get_action()
            state = self.environment.get_state()
            # left, right, shoot , stop
            next_state, reward, done =self.environment.step(action)
            self.agent.store_experience(state,action, reward, next_state, done)
            self.check_collisions()
            self.update_game_state()
            self.render_game_state()


            
    #resets the game/round
    def game_over(self):
        self.score = 0
        self.enemies = []
        self.player = player.Player(self.screen_width, self.screen_height)
        self.setup_enemy_grid()