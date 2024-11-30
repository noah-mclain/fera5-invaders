import pygame
import random
from environment.sprite_sheet import SpriteSheet
from environment.animation_sequence import AnimationSequence

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position, sprite_sheet_path, sprite_type="chicken"):
        super().__init__()
        
        try:
            # Load sprite sheet
            print(f"Loading sprite sheet from: {sprite_sheet_path}")
            self.sprite_sheet_image = pygame.image.load(sprite_sheet_path).convert_alpha()
            self.sprite_sheet = SpriteSheet(self.sprite_sheet_image)
            
            # Extract all frames
            self.frames = {}
            self.load_frames(sprite_type)
            
            # Set up animation sequences based on sprite type
            self.setup_animations(sprite_type)
            
            # Set up initial sprite image and rect
            if "alive" not in self.frames or not self.frames["alive"]:
                raise ValueError("No 'alive' frames loaded")
            
            self.image = self.frames["alive"][0]
            self.rect = self.image.get_rect(topleft=position)
            
            # Track current animation state
            self.current_animation = None
            self.previous_animation = None
            
        except Exception as e:
            print(f"Error initializing AnimatedSprite: {str(e)}")
            raise
    
    def load_frames(self, sprite_type):
        # Different frame dimensions and positions for different sprites and their states
        sprite_data = {
            "chicken": {
                "alive": {
                    "width": 40,
                    "height": 35,
                    "frames": [
                        {"x": i * 40, "y": 0} for i in range(10)  # Generates 10 frames with x positions 0, 40, 80, etc.
                    ],
                    "scale": 1
                },
                "dead": {
                    "width": 37,
                    "height": 35,
                    "frames": [
                        {"x": 366, "y": 0}
                    ],
                    "scale": 1
                },
                "food": {
                    "frames": [
                        {"x": 403, "y": 0, "width": 21, "height": 35},
                        {"x": 424, "y": 0, "width": 41, "height": 35},
                        {"x": 465, "y": 0, "width": 45, "height": 35}
                    ],
                    "scale": 1,
                    "speed": 0.5  # Slower animation speed for food
                }
            }
        }
        
        data = sprite_data.get(sprite_type)
        if not data:
            raise ValueError(f"Unknown sprite type: {sprite_type}")
        
        # Extract frames for each animation state
        self.frames = {}
        
        for state, state_data in data.items():
            self.frames[state] = []
            for frame_data in state_data["frames"]:
                try:
                    width = frame_data.get("width", state_data.get("width"))
                    height = frame_data.get("height", state_data.get("height"))
                    
                    print(f"Loading {state} frame with dimensions: {width}x{height}")
                    
                    frame = self.sprite_sheet.get_image_at_pos(
                        x=frame_data["x"],
                        y=frame_data["y"],
                        width=width,
                        height=height,
                        scale=state_data["scale"],
                        color=(0, 0, 0)
                    )
                    self.frames[state].append(frame)
                except Exception as e:
                    print(f"Error loading {state} frame: {str(e)}")
    
    def setup_animations(self, sprite_type):
        animation_data = {
            "chicken": {
                "alive": {"speed": 0.1},
                "dead": {"speed": 0.5},
                "food": {"speed": 0.2}
            },
            "egg": {
                "whole": {"speed": 0.1}
            }
        }
        
        data = animation_data.get(sprite_type)
        if not data:
            raise ValueError(f"No animation data for sprite type: {sprite_type}")
        
        self.animations = {}
        
        for anim_name, anim_info in data.items():
            try:
                self.animations[anim_name] = AnimationSequence(
                    self.frames[anim_name],
                    animation_speed=anim_info["speed"]
                )
            except Exception as e:
                print(f"Error setting up {anim_name} animation: {str(e)}")
                raise
    
    def play_animation(self, animation_name, loop=True):
        """Play the specified animation sequence"""
        if animation_name in self.animations:
            # Stop the previous animation if it exists
            if self.current_animation and self.current_animation != animation_name:
                self.animations[self.current_animation].stop()
                self.previous_animation = self.current_animation
            
            self.current_animation = animation_name
            self.animations[animation_name].play(loop=loop)
        else:
            print(f"Warning: Animation '{animation_name}' not found")

    def stop_animation(self):
        """Stop the current animation"""
        if self.current_animation:
            self.animations[self.current_animation].stop()
            self.previous_animation = self.current_animation
            self.current_animation = None

    def pause_animation(self):
        """Pause the current animation"""
        if self.current_animation:
            self.animations[self.current_animation].pause()

    def update(self):
        """Update the sprite's animation"""
        if self.current_animation:
            current_anim = self.animations[self.current_animation]
            if current_anim.is_playing:
                self.image = current_anim.update(pygame.time.get_ticks())
            elif not current_anim.loop:
                # If animation is done and not looping, keep the last frame
                self.image = current_anim.frames[current_anim.frame_index]

# Test the animation
# if __name__ == "__main__":
#     pygame.init()
    
#     # Set up display
#     SCREEN_WIDTH = 500
#     SCREEN_HEIGHT = 500
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     pygame.display.set_caption('Animated Sprite')
    
#     # Create sprite and sprite group
#     sprite_group = pygame.sprite.Group()
#     animated_sprite = AnimatedSprite(
#         position=(200, 200),
#         sprite_sheet_path='assets/images/Enemy/chickenRed.png'
#     )
#     sprite_group.add(animated_sprite)
    
#     # Game loop
#     clock = pygame.time.Clock()
#     running = True
    
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
        
#         sprite_group.update()
        
#         screen.fill((50, 50, 50))
#         sprite_group.draw(screen)
#         pygame.display.flip()
        
#         clock.tick(60)
    
#     pygame.quit()