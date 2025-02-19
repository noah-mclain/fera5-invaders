"""
A class that will serve as the link between the AI model and the game
It has helper methods that will transfer the current state of the game's environment to the AI model
and it has a step function that will relay back the actions taken by the AI
"""
class ai_env:
    def __init__(self, game):
        self.game = game
        self.player = game.player
        self.enemies = game.enemies
        self.score = 0
        self.actions=["right", "left", "shoot", "stop"]  
        self.hit_enemies = 0
        self.eaten_chicken = 0
        self.egg_hit_by_laser = 0
        self.player_hit_by_egg = 0
        self.missed_laser = 0
        self.player_death = False
        self.previous_position = self.player.rect.x
        self.no_movement_steps = 0
    # returns all possible actions in a given state        
    def available_actions(self):
        available_actions = ["shoot"]
        if self.player.rect.x < self.game.screen_width:
            available_actions.append("right")
        if self.player.rect.x > 0:
            available_actions.append("left")
        return available_actions
    
    def all_actions(self):
        return self.actions
    
    # performs the current action chosen by the AI 
    def step(self,action): 
        if action=="right":
            self.player.move(3.7)
            print()
        elif action=="left":
            self.player.move(-3.7)
        elif action=="shoot":
            self.player.shoot()
        #self.game.update()
        
        reward=self.calculate_reward()
         
        done=self.game_over()
        
        state=self.get_state()
        
        return state,reward,done    
        
      
    # to calculate the number of the input nodes  
    def input_nodes(self):
        player_nodes = 2
        MAX_chicken_nodes = 30 * 2
        MAX_egg_nodes = MAX_chicken_nodes * 15
        MAX_laser_nodes = 20
        MAX_powerups_nodes = 6
        total_nodes = player_nodes + MAX_chicken_nodes + MAX_egg_nodes + MAX_laser_nodes + MAX_powerups_nodes
        return total_nodes
    
    # returns the current state of the game
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
    
    # checks if the game is over
    def game_over(self):
        if self.game.running == False:
            return 0
        return 1
    
    # to calculate the reward/penalty for each action the AI takes

    
    def calculate_reward(self):
        """Calculates and returns the reward for the current action."""
        reward = 0
        reward += 1 * self.hit_enemies
        self.hit_enemies = 0
        reward += 1 * self.eaten_chicken
        self.eaten_chicken = 0
        # reward += 0.1 * self.egg_hit_by_laser
        # self.egg_hit_by_laser = 0
        reward -= 1 * self.player_hit_by_egg
        self.player_hit_by_egg = 0
        if self.player_death:
            reward -= 10
            self.player_death = False  #reset flag
        reward -= 0.05 * self.missed_laser
        self.missed_laser = 0
        
        #penalty for staying in cornars
        corner_threshold = 15 
        if self.player.rect.x < corner_threshold or self.player.rect.x > (self.game.screen_width - corner_threshold):
            reward -= 0.1  # smol penalty to encourage movement
        
        #reward for moving towards the center
        center_x = self.game.screen_width / 2
        distance_from_center = abs(self.player.rect.x - center_x)
        reward += -distance_from_center * 0.001  #encouraging staying near the center
        
        #penalty for no movement over multiple steps
        if self.player.rect.x == self.previous_position:
            self.no_movement_steps += 1
            if self.no_movement_steps > 50:
                reward -= 10  #penalty for being stuck
        else:
            self.no_movement_steps = 0
            self.previous_position = self.player.rect.x
        
        return reward
    
    def reassign_player(self, player):
        """Reassigns the player object, useful after resetting the game."""
        self.player = player
