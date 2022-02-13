import pygame


class Settings:
    def __init__(self) -> None:
        # Screen settings
        self.screen_width = 1100
        self.screen_height = 600
        self.bg_color = (0, 0, 0)
        self.fullscreen = True

        # Ship settings
        self.ship_speed = 1
        self.ship_limit = 1

        # Bullet settings
        # self.bullet_speed = 1.0
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # Alien settings
        # self.alien_speed = 1.0
        self.fleet_drop_speed = 10  # How many pixels drop after hitting the wall
        self.fleet_direction = 1  # 1 = right, -1 = left

        # Difficulty settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.setup_dynamic_settings()

        # UI text settings
        self.font = pygame.font.SysFont(None, 48)  # font, styles
        # self.font = pygame.font.Font("fontname.ttf") if you have a font you want

    def check_fullscreen(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen_width = self.screen.get_rect().width
            self.screen_height = self.screen.get_rect().height

    def setup_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        if self.fullscreen:
            self.alien_speed = 2.0
        else:
            self.alien_speed = 1.0
        self.alien_points = 10
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
