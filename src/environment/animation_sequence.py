class AnimationSequence:
    def __init__(self, frames, animation_speed=0.1):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.last_update = 0
        self.is_playing = False
        self.loop = True
        self.callback = None
        self.animation_finished = False
    
    def play(self, loop=True):
        """Start playing the animation sequence"""
        self.is_playing = True
        self.loop = loop
        self.frame_index = 0
        self.animation_finished = False
    
    def stop(self):
        """Stop the animation sequence"""
        self.is_playing = False
        self.frame_index = 0
    
    def pause(self):
        """Pause the animation sequence"""
        self.is_playing = False
    
    def update(self, current_time):
        """Update the animation frame"""
        if not self.is_playing:
            return self.frames[self.frame_index] if self.frames else None
            
        if current_time - self.last_update > self.animation_speed * 1000:
            self.last_update = current_time
            
            # Move to next frame
            if self.frame_index < len(self.frames) - 1:
                self.frame_index += 1
            else:
                if self.loop:
                    self.frame_index = 0  # Reset to first frame for looping animations
                else:
                    # For non-looping animations, stay on last frame
                    self.animation_finished = True
                    if self.callback:
                        self.callback()
                        
        # Make sure frame_index is valid before accessing
        if 0 <= self.frame_index < len(self.frames):
            return self.frames[self.frame_index]
        else:
            print(f"Warning: Invalid frame index {self.frame_index}. Total frames: {len(self.frames)}")
            return None  # Or handle accordingly
