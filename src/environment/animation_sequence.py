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
        self.image = self.frames[self.frame_index]

    def play(self, loop=True):
        self.is_playing = True
        self.loop = loop
        self.frame_index = 0
        self.animation_finished = False

    def update(self, current_time):
        """Update the current animation frame."""
        if not self.is_playing or self.animation_finished:
            return  self.image

        if current_time - self.last_update > self.animation_speed * 1000:
            self.last_update = current_time
            if self.frame_index < len(self.frames) - 1:
                self.frame_index += 1
            else:
                if self.loop:
                    self.frame_index = 0
                else:
                    self.animation_finished = True
                    self.is_playing = False
                    if self.callback:
                        self.callback()
        if 0 <= self.frame_index < len(self.frames):
            return self.frames[self.frame_index]
        else:
            print(f"Warning: Invalid frame index {self.frame_index}. Total frames: {len(self.frames)}")
            return None  # Or handle accordingly

    def draw(self, screen, position):
        if 0 <= self.frame_index < len(self.frames):
            frame = self.frames[self.frame_index]
            if frame:  # Ensure the frame is not None
                frame_rect = frame.get_rect(center=position)
                screen.blit(frame, frame_rect)
            else:
                print(f"Warning: Frame at index {self.frame_index} is None.")
        else:
            print(f"Warning: Invalid frame index {self.frame_index}. Total frames: {len(self.frames)}")

    def stop(self):
        """Stop the animation sequence"""
        self.is_playing = False
        self.frame_index = 0
    
    def pause(self):
        """Pause the animation sequence"""
        self.is_playing = False