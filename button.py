import pygame.font
import pygame


class Button:
    def __init__(self, game, txt):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.txt_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.set_button_text(txt)

    def set_button_text(self, txt):
        self.txt = self.font.render(txt, True, self.txt_color, self.button_color)
        self.txt_rect = self.txt.get_rect()
        self.txt_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.txt, self.txt_rect)
