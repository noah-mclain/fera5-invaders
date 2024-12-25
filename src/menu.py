import pygame
import os
from game import Game
from gameAI import GameAI

class GameMenu:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.SCREEN_WIDTH = min(info.current_w, 1920)
        self.SCREEN_HEIGHT = min(info.current_h, 1080)

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Chicken Invaders - Game Menu")

        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.font_large = pygame.font.SysFont("Arial", 50, bold=True)

        self.WHITE = (255, 255, 255)
        self.NEON_GREEN = (0, 255, 0)
        self.NEON_BLUE = (0, 255, 255)
        self.DARK_BLUE = (0, 0, 128)
        self.PURPLE = (128, 0, 128)

        self.menu_items = ["Start Game", "Play as AI", "Train AI", "Options", "Quit"]
        self.selected_item = 0

        self.background_image = pygame.image.load(os.path.join("assets", "images", "background", "galaxy_background.jpg"))
        self.background_image = pygame.transform.scale(self.background_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.logo_image = pygame.image.load(os.path.join("assets", "images", "logo", "chicken_invaders_logo.png"))
        self.logo_image = pygame.transform.scale(self.logo_image, (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 4))

    def draw_menu(self):
        self.screen.blit(self.background_image, (0, 0))
        logo_rect = self.logo_image.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 6))
        self.screen.blit(self.logo_image, logo_rect)

        total_menu_height = len(self.menu_items) * 50
        start_y = (self.SCREEN_HEIGHT - total_menu_height) // 2

        for i, item in enumerate(self.menu_items):
            color = self.NEON_BLUE if i == self.selected_item else self.WHITE
            menu_text = self.font.render(item, True, color)
            menu_rect = menu_text.get_rect(center=(self.SCREEN_WIDTH // 2, start_y + i * 50))
            self.screen.blit(menu_text, menu_rect)

            if self.selected_item == i:
                pygame.draw.rect(self.screen, self.NEON_GREEN, menu_rect.inflate(20, 10), 5)

        pygame.display.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                elif event.key == pygame.K_DOWN:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                elif event.key == pygame.K_RETURN:
                    return self.menu_items[self.selected_item].lower().replace(" ", "_")
        return "menu"

    def menu_loop(self):
        while True:
            self.screen.fill(self.DARK_BLUE)
            self.draw_menu()
            choice = self.handle_events()

            if choice == "start_game":
                # print("Starting the game...")
                game = Game()
                game.run()
                break
            elif choice == "play_as_ai":
                # print("You are playing as AI...")
                game = GameAI()
                game.run()
                break
            elif choice == "options":
                # print("Opening options...")
                break
            elif choice == "quit":
                # print("Exiting the game...")
                pygame.quit()
                break
