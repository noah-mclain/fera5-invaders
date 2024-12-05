import pygame
import random
from environment.sprite_sheet import SpriteSheet
from environment.animation_sequence import AnimationSequence

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, position, sprite_sheet_path, sprite_type="chicken", initial_state="alive"):
        super().__init__()
        self.animation_done = False
        
        try:
            # Load sprite sheet
            print(f"Loading sprite sheet from: {sprite_sheet_path}")
            self.sprite_sheet_image = pygame.image.load(sprite_sheet_path).convert_alpha()
            self.sprite_sheet = SpriteSheet(self.sprite_sheet_image)
            
            # Extract all frames
            self.frames = {}
            self.load_frames(sprite_type)  # Load frames based on sprite type
            
            # Set up animation sequences based on sprite type
            self.setup_animations(sprite_type)  # Setup animations
            
            # Set up initial sprite image and rect
            if initial_state not in self.frames or not self.frames[initial_state]:
                raise ValueError(f"No '{initial_state}' frames loaded")
            
            self.image = self.frames[initial_state][0]
            self.rect = self.image.get_rect(topleft=position)
            
            # Track current animation state
            self.current_animation = None
            self.previous_animation = None
            
            self.last_update_time = pygame.time.get_ticks()
        except Exception as e:
            print(f"Error initializing AnimatedSprite: {str(e)}")
            raise
    
    def load_frames(self, sprite_type):
        # Different frame dimensions for different sprites and their states
        sprite_data = {
            "chicken": {
                "alive": {
                    "width": 40,
                    "height": 35,
                    "frames": [
                        {"x": i * 40, "y": 0} for i in range(10)  # Generates frames with x positions
                    ],
                    "scale": 1.5
                },
                "dead": {
                    "width": 45,
                    "height": 35,
                    "frames": [
                        {"x": 360, "y": 0}],  # Single frame for death
                    "scale": 1
                },
               "food": {
                    "width": 45,
                    "height": 35,
                    "frames": [
                        {"x": 405, "y": 0, "width": 45, "height": 35},   # First food frame
                        {"x": 450, "y": 0, "width": 45, "height": 35},   # Second food frame
                        {"x": 495, "y": 0, "width": 45, "height": 35}    # Third food frame
                    ],
                    "scale": 1,
                }
            },
            "egg": {
                "whole": {
                    "width": 28,
                    "height": 24,
                    "frames": [
                        {"x": 0, "y": 0, "width": 28, "height": 24}],
                    "scale": 1
                },
                "broken": {
                    "width": 28,
                    "height": 24,
                    "frames": [
                        {"x": 28, "y": 0, "width": 28, "height": 24},
                        {"x": 56, "y": 0, "width": 28, "height": 24},
                        {"x": 81, "y": 0, "width": 28, "height": 24},
                        {"x": 109, "y": 0, "width": 28, "height": 24},
                        {"x": 137, "y": 0, "width": 28, "height": 24},
                        {"x": 165, "y": 0, "width": 28, "height": 24},
                        {"x": 193, "y": 0, "width": 28, "height": 24},
                        {"x": 221, "y": 0, "width": 28, "height": 24},
                    ],
                    "scale": 1,
                }     
            },
            "heart": {
                "full": {
                    "width": 15,
                    "height": 16,
                    "frames": [
                        {"x": 0, "y": 0, "width": 15, "height": 16},
                    ],
                    "scale": 1,
                },
                "empty": {
                    "width": 15,
                    "height": 16,
                    "frames": [
                        {"x": 16, "y": 0, "width": 15, "height": 16},
                    ],
                    "scale": 1,
                },
            },
        }
        
        data = sprite_data.get(sprite_type)
        if not data:
            raise ValueError(f"Unknown sprite type: {sprite_type}")
        
        # Extract frames for each animation state
        self.frames = {}  # Change to dictionary to store frames by state
        
        for state, state_data in data.items():
            self.frames[state] = []
            for frame_data in state_data.get("frames", []):
                try:
                    # Ensure frame_data is a dictionary
                    if isinstance(frame_data, int):
                        raise ValueError(f"Expected frame data to be a dictionary, got int: {frame_data}")

                    # Debugging output to check frame data
                    print(f"Processing {state} frame data: {frame_data}")
                    
                    width = frame_data.get("width", state_data["width"])
                    height = frame_data.get("height", state_data["height"])
                    
                    frame = self.sprite_sheet.get_image_at_pos(
                        x=frame_data["x"],
                        y=frame_data["y"],
                        width=width,
                        height=height,
                        scale=state_data["scale"],
                        color=(0, 0, 0)
                    )
                    
                    if frame is not None:
                        self.frames[state].append(frame)
                        print(f"Loaded {state} frame at position ({frame_data['x']}, {frame_data['y']}) with size {width}x{height}")
                        
                except Exception as e:
                    print(f"Error loading {state} frame: {str(e)}")
            
        # Debugging output
        for state, frames in self.frames.items():
            print(f"{state} frames loaded: {len(frames)}") 
    
    def setup_animations(self, sprite_type):
        animation_data = {
            "chicken": {
                "alive": {"speed": 0.1},
                "dead": {"speed": 0.1},
                "food": {"speed": 0.5}
            },
            "egg": {
                "whole": {"speed": 0.1},
                "broken": {"speed": 0.2}
            },
            "heart": {
                "full": {"speed": 0.2},
                "empty": {"speed": 0.2}
            }
        }
        
        data = animation_data.get(sprite_type)
        if not data:
            raise ValueError(f"No animation data for sprite type: {sprite_type}")
        
        self.animations = {}
        
        for anim_name, anim_info in data.items():
            try:
                if anim_name not in self.frames or not self.frames[anim_name]:
                    raise ValueError(f"No frames loaded for animation '{anim_name}'")
                
                self.animations[anim_name] = AnimationSequence(
                    self.frames[anim_name],
                    animation_speed=anim_info["speed"]
                )
            except Exception as e:
                print(f"Error setting up {anim_name} animation: {str(e)}")
    
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
        current_time = pygame.time.get_ticks()
        if self.current_animation:
            current_anim = self.animations[self.current_animation]
            if current_anim.is_playing:
                if current_time - self.last_update_time > current_anim.animation_speed * 1000:
                    self.image = current_anim.update(pygame.time.get_ticks())
                    self.last_update_time = current_time
            elif not current_anim.loop:
                # If animation is done and not looping, keep the last frame
                self.image = current_anim.frames[current_anim.frame_index]
                self.animation_done = True
                
            

    def isAnimationDone(self):
        return self.animation_done