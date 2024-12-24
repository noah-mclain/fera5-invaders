import pygame
import sys
from game import Game
from gameAI import GameAI
from menu import GameMenu

def check_dependencies():
    required_files = [
        "assets/images/ship.png",
        "assets/images/bullet/a1.png",
        "assets/images/shipDie.png",
        "assets/images/Enemy/chickenRedSpriteSheet.png",
        "assets/images/Enemy/eggSpriteSheet.png",  
        "assets/images/background/livesSpriteSheet.png"
    ]

    for file in required_files:
        try:
            with open(file, 'rb') as f:
                print(f"Found {file}")
        except FileNotFoundError:
            print(f"Error: Required file '{file}' not found!")
            return False
    return True

def run_game():
    # print("Initializing pygame...")
    pygame.init()

    # print("Setting up display...")
    pygame.display.init()

    # print("Creating game menu...")
    menu = GameMenu()

    # print("Running menu loop...")
    choice = menu.menu_loop()  # Get user selection from menu
    if choice == "start_game":
        # print("Starting the game...")
        game = GameAI()
        # print("Game created successfully")
        game.run()

    elif choice == "play_as_ai":
        # print("You are playing as AI...")
        # Implement AI logic here
        game = GameAI()
        game.run()

    elif choice == "train_ai":
        print("Training AI...")
        # Implement AI training here

    elif choice == "options":
        print("Opening options...")
        # Implement options here

    elif choice == "quit":
        print("Exiting the game...")
        pygame.quit()
        sys.exit()

def main():
    if not check_dependencies():
        print("Missing required files. Please ensure all assets are in place.")
        return

    run_game()

if __name__ == "__main__":
    main()
