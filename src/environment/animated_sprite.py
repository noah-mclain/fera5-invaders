from environment.frame_sprite import FrameSprite
from environment.animation_sequence import AnimationSequence

class AnimatedSprite(FrameSprite):
    """Sprite that can be animated."""
    def __init__(self):
        super().__init__()
        self.last_elapsed = 0
        self.frames_per_second = 20  # Frames per second
        self.current_sequence = None
        self.playing = False
        self.looping = False
        self.sequences = {}
    
    def update(self, delta):
        if not self.playing or not self.current_sequence:
            return
        
        # Update time
        self.last_elapsed += delta
        frame_duration = 1 / self.frames_per_second
        
        if self.last_elapsed < frame_duration:
            return
        self.last_elapsed -= frame_duration

        # Move to the next frame in the sequence
        seq = self.current_sequence
        current_col = self.frame_x // self.frame_width
        current_row = self.frame_y // self.frame_height

        # Advance frame
        current_col += 1
        if current_col > seq.end_column:
            current_col = seq.start_column
            current_row += 1
            if current_row > seq.end_row:
                if self.looping:
                    current_row = seq.start_row
                else:
                    self.playing = False
                    return

        # Update frame coordinates
        self.frame_x = current_col * self.frame_width
        self.frame_y = current_row * self.frame_height

    def _is_end_of_sequence(self):
        """Check if the current frame is the last in the sequence."""
        seq = self.current_sequence
        current_col = self.frame_x // self.frame_width
        current_row = self.frame_y // self.frame_height

        return (
            current_row > seq.end_row
            or (current_row == seq.end_row and current_col > seq.end_column)
        )

    def play_sequence(self, seq_name, loop=False):
        """Start playing a specific animation sequence."""
        if seq_name not in self.sequences:
            raise ValueError(f"Sequence {seq_name} not found.")
        
        self.current_sequence = self.sequences[seq_name]
        self.looping = loop
        self.playing = True
        self.frame_x = self.current_sequence.start_column * self.frame_width
        self.frame_y = self.current_sequence.start_row * self.frame_height

    def stop_playing(self):
        """Stop the animation."""
        self.playing = False

    def set_frame_dimensions(self, width, height):
        """Set frame width and height."""
        self.frame_width = width
        self.frame_height = height

    def set_columns_rows(self, columns, rows):
        """Set number of columns and rows in the sprite sheet."""
        self.frame_width = self.image.get_width() // columns
        self.frame_height = self.image.get_height() // rows

    def add_sequence(self, name, start_row, start_column, end_row, end_column):
        """Create and add a new animation sequence."""
        self.sequences[name] = AnimationSequence(
            start_row, start_column, end_row, end_column
        )