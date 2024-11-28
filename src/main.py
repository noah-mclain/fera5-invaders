# Main game loop and initialization
import pygame
import sys
from game import Game

def check_dependencies():
    """Check if all required assets and modules are available"""
    required_files = [
        "assets/images/ship.png",
        "assets/images/bullet/a1.png",
        "assets/images/shipDie.png"
    ]
    
    for file in required_files:
        try:
            open(file)
        except FileNotFoundError:
            print(f"Error: Required file '{file}' not found!")
            return False
    return True

def main():
    # Check if all required files exist
    if not check_dependencies():
        print("Missing required files. Please ensure all assets are in place.")
        sys.exit(1)

    try:
        # Initialize pygame
        pygame.init()
        
        # Set up display
        pygame.display.init()
        
        # Create and run game
        game = Game()
        game.run()
        
    except pygame.error as e:
        print(f"Pygame error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Clean up
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
