import pygame
from pygame.sprite import Sprite
from bullet import Bullet
from explosion import Explosion
import os.path


class Ship(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen_rect = game.screen.get_rect()
        self.image = pygame.image.load(
            os.path.join(os.path.dirname(__name__), "images", "ship.png")
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(
            self.rect.x
        )  # Store a decimal value for the ship's horizontal position

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw the ship at its current position (2nd parameter)"""
        self.game.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def fire_bullet(self):
        """Create a new bullet instance and add it to the bullet group"""
        if len(self.game.bullets) < self.game.settings.bullets_allowed:
            new_bullet = Bullet(self.game)
            self.game.shooting_sound.play()
            self.game.bullets.add(new_bullet)

    def ship_hit(self):
        if self.game.stats.ships_left > 0:
            explosion = Explosion(self.game)
            explosion.set_explosion_center_and_object(self.rect.center, "ship")
            self.game.explosions.add(explosion)
            self.game.explosion_sound.play()

            self.game.stats.ships_left -= 1
            self.game.sb.prepare_ships()
            self.game.aliens.empty()
            self.game.bullets.empty()
            self.game.alien.create_fleet()
            self.center_ship()
        else:
            self.game.stats.game_active = False
            self.game.stats.game_over = True
            pygame.mouse.set_visible(True)

    def update(self):
        """Updates the ship's position on the movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.game.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.game.settings.ship_speed

        self.rect.x = self.x  # Only the integer part is stored in self.rect.x
