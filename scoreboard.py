import pygame.font
from pygame.sprite import Group
from ship import Ship
import os.path


class Scoreboard:
    def __init__(self, game):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        self.game = game

        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.prepare_score()
        self.prepare_highscore()
        self.prepare_ships()

    def prepare_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prepare_highscore(self):
        highscore = round(self.stats.highscore, -1)
        highscore_str = f"{highscore:,}"
        self.highscore_image = self.font.render(highscore_str, True, self.text_color)
        self.highscore_rect = self.highscore_image.get_rect()
        self.highscore_rect.centerx = self.screen_rect.centerx
        self.highscore_rect.top = self.score_rect.top

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.highscore_image, self.highscore_rect)
        self.ships.draw(self.screen)

    def check_highscore(self):
        if self.stats.score > self.stats.highscore:
            try:
                with open(
                    os.path.join(os.path.dirname(__file__), "highscore.txt"), "w"
                ) as file:
                    file.write(str(self.stats.score))
                self.stats.highscore = self.stats.score
                self.prepare_highscore()
            except FileNotFoundError:
                print("Cannot open highscore file")
                raise

    def prepare_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
