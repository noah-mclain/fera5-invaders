import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
        sheet_width, sheet_height = self.sheet.get_size()
        print(f"Sprite sheet dimensions: {sheet_width}x{sheet_height}")
        
    def get_image_at_pos(self, x, y, width, height, scale=1, color=None):
        try:
            sheet_width, sheet_height = self.sheet.get_size()
            print(f"Attempting to extract frame:")
            print(f"- Sheet size: {sheet_width}x{sheet_height}")
            print(f"- Extraction area: x={x}, y={y}, width={width}, height={height}")
            
            # Validate extraction coordinates
            if x < 0 or y < 0 or x + width > sheet_width or y + height > sheet_height:
                print("WARNING: Extraction coordinates out of bounds!")
                print(f"- Right edge would be: {x + width}")
                print(f"- Bottom edge would be: {y + height}")
                return None  # Return None if out of bounds
            
            # Create a new surface for the frame
            image = pygame.Surface((width, height), pygame.SRCALPHA)
            
            # Copy the sprite from the sheet
            image.blit(self.sheet, (0, 0), (x, y, width, height))
            
            # Scale if necessary
            if scale != 1:
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = pygame.transform.scale(image, (new_width, new_height))
            
            # Set color key if specified
            if color is not None:
                image.set_colorkey(color)
            
            return image
            
        except Exception as e:
            print(f"Error extracting frame: {str(e)}")
            raise
