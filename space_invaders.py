import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import Button
from explosion import Explosion
from scoreboard import Scoreboard
from events import Events
import os.path


class SpaceInvaders:
    """Class to manage game assets and behaviour"""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.settings.check_fullscreen()
        self.bg_image = pygame.image.load(
            os.path.join(os.path.dirname(__name__), "images", "starfield.png")
        ).convert_alpha()
        pygame.display.set_caption("Space Invaders")
        self.events = Events(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # Creates empty sprite group
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.alien = Alien(self)
        self.alien.create_fleet()
        self.play_button = Button(self, "PLAY")
        self.stats = GameStats(self)
        self.stats.highscore = self.stats.get_highscore()
        self.sb = Scoreboard(self)
        self.setup_sounds()

    def run_game(self):
        pygame.mixer.music.play(loops=-1)

        # Main loop
        while True:
            self.events.check_events()
            if self.stats.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
                self.explosions.update()
            self.update_screen()

    def setup_sounds(self):
        sound_dir = os.path.join(os.path.dirname(__name__), "sounds")

        pygame.mixer.music.load(os.path.join(sound_dir, "music.wav"))
        pygame.mixer.music.set_volume(0.3)

        self.shooting_sound = pygame.mixer.Sound(os.path.join(sound_dir, "laser.wav"))
        self.shooting_sound.set_volume(0.1)

        self.explosion_sound = pygame.mixer.Sound(
            os.path.join(sound_dir, "explosion.wav")
        )
        self.explosion_sound.set_volume(0.1)

    def update_bullets(self):
        self.bullets.update()  # Calls every instance's (in bullets) update method
        # Get rid of bullets that have disappeared from screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.explosion_sound.play()

            for aliens in collisions.values():
                # If we hit many aliens at the same time with wide bullet
                self.stats.score += self.settings.alien_points * len(aliens)

                for alien in aliens:
                    explosion = Explosion(self)
                    explosion.set_explosion_center_and_object(
                        alien.rect.center, "alien"
                    )
                    self.explosions.add(explosion)
            self.sb.prepare_score()
            self.sb.check_highscore()

        # Check if no more aliens left -> Create a new fleet
        if not self.aliens:
            self.bullets.empty()
            self.alien.create_fleet()
            self.settings.increase_speed()

    def update_aliens(self):
        self.alien.check_fleet_edges()
        self.aliens.update()
        self.alien.check_aliens_bottom()

        # Check alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship.ship_hit()

    def update_screen(self):
        if not self.stats.game_active:
            self.screen.fill(self.settings.bg_color)
            self.play_button.draw_button()
            if self.stats.game_over:
                self.stats.show_game_over()
        else:
            self.screen.blit(self.bg_image, self.screen.get_rect())
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.explosions.draw(self.screen)
            self.sb.show_score()
        pygame.display.flip()  # Make the most recently drawn screen visible
