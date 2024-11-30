# Main game loop and initialization
import pygame
import sys
from game import Game

def check_dependencies():
    """Check if all required assets and modules are available"""
    required_files = [
        "assets/images/ship.png",
        "assets/images/bullet/a1.png",
        "assets/images/shipDie.png",
        "assets/images/Enemy/chickenRed.png",
        "assets/images/Enemy/dead.png",
        "assets/images/Enemy/egg.png"
    ]
    
    for file in required_files:
        try:
            with open(file, 'rb') as f:
                print(f"Found {file}")
        except FileNotFoundError:
            print(f"Error: Required file '{file}' not found!")
            return False
    return True

def main():
    game = None
    try:
        print("Checking dependencies...")
        if not check_dependencies():
            print("Missing required files. Please ensure all assets are in place.")
            return

        print("Initializing pygame...")
        pygame.init()
        
        print("Setting up display...")
        pygame.display.init()
        
        print("Creating game...")
        game = Game()
        print("Game created successfully")
        
        print("Running game...")
        if game:
            game.run()
        
    except pygame.error as e:
        print(f"Pygame error occurred: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        if game:
            game.running = False
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
