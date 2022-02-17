import pygame
import os.path


class GameStats:
    def __init__(self, game):
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.reset_stats()
        self.game_active = False
        self.game_over = False
        self.highscore = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0

    def get_highscore(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), "highscore.txt")) as file:
                highscore = file.readline()
                if not highscore:
                    highscore = 0
                return int(highscore)
        except FileNotFoundError:
            print("Cannot open highscore file")
            raise

    def show_game_over(self):
        self.font = pygame.font.SysFont(None, 144)
        self.game_over_image = self.font.render("GAME OVER", True, (0, 255, 0))
        self.game_over_image_rect = self.game_over_image.get_rect()
        self.game_over_image_rect.centerx = self.screen_rect.centerx
        self.game_over_image_rect.y = 40
        self.screen.blit(self.game_over_image, self.game_over_image_rect)
