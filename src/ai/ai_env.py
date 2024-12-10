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
        self.player_death = False

    # returns all possible actions in a given state        
    def available_actions(self):
        available_actions = ["shoot", "stop"]
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
        reward=0
        reward+= 1 * self.hit_enemies
        self.hit_enemies = 0
        reward+= 1 * self.eaten_chicken
        self.eaten_chicken = 0
        #reward+= 0.1 * self.egg_hit_by_laser
        #self.egg_hit_by_laser = 0
        reward-= 1 * self.player_hit_by_egg
        self.player_hit_by_egg = 0
        if self.player_death:
            reward -=2
        else:
            reward += 0.2
        reward += self.score * 0.0001
        return reward

    def reassign_player(self, player):
        self.player = player

