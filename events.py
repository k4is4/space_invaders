import pygame
import sys


class Events:
    def __init__(self, game):
        self.game = game

    def check_events(self):
        # Responses to keypresses and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

    def check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.game.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.game.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.game.ship.fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.game.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.game.ship.moving_left = False

    def check_play_button(self, mouse_pos):
        button_clicked = self.game.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game.stats.game_active:
            pygame.mouse.set_visible(False)
            self.game.settings.setup_dynamic_settings()
            self.game.stats.reset_stats()
            self.game.sb.prepare_score()
            self.game.sb.prepare_ships()
            self.game.stats.game_active = True
            self.game.aliens.empty()
            self.game.bullets.empty()
            self.game.alien.create_fleet()
            self.game.ship.center_ship()
