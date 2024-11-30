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
        "assets/images/Enemy/chiken.png", 
        "assets/images/Enemy/dead.png",
        "assets/images/background/heart.png",
        "assets/images/scores1.png"
    ]
    
    for file in required_files:
        try:
            open(file)
        except FileNotFoundError:
            print(f"Error: Required file '{file}' not found!")
            return False
    return True

def main():
    # Check dependencies
    if not check_dependencies():
        sys.exit("Missing required files!")

    try:
        pygame.init()
        game = Game()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        raise  # Re-raise the exception for debugging
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
