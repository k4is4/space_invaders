import pygame
from pygame.sprite import Sprite
from time import sleep
from bullet import Bullet
import random

from explosion import Explosion


class Ship(Sprite):
    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        # Load the ship image and get its rect:
        self.image = pygame.image.load("images/ship_transparent.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)
        # Movement flag
        self.moving_right = False
        self.moving_left = False

        self.game = game

    def blitme(self):
        # Draws the ship at its current position (2nd parameter)
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def fire_bullet(self):
        # Creates new bullet instance and adds it to the bullet group
        if len(self.game.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.game)
            random.choice(self.game.shooting_sounds).play()
            self.game.bullets.add(new_bullet)

    def ship_hit(self):
        explosion = Explosion(self.game)
        explosion.set_explosion_center_and_object(self.rect.center, "ship")
        self.game.explosions.add(explosion)
        if self.game.stats.ships_left > 0:
            self.game.stats.ships_left -= 1
            self.game.sb.prepare_ships()
            self.game.aliens.empty()
            self.game.bullets.empty()
            self.game.create_fleet()
            self.center_ship()
            sleep(0.5)
        else:
            self.game.stats.game_active = False
            pygame.mouse.set_visible(True)

    def update(self):
        # Updates the ship's position on the movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # Only the integer part is stored in self.rect.x
        self.rect.x = self.x
