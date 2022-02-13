import sys
import pygame
from settings import Settings
from ship import Ship
from game_texts import UIText
from alien import Alien
from game_stats import GameStats
from button import Button
from explosion import Explosion
from scoreboard import Scoreboard
import os.path


class SpaceInvaders:
    # Class to manage game assets and behaviour
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        self.settings.check_fullscreen()
        self.bg_image = pygame.image.load("images/starfield.png").convert_alpha()
        pygame.display.set_caption("Space Invaders")
        self.bg_color = self.settings.bg_color  # RGB sulkeissa
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # Creates empty sprite group
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.ui_text = UIText(self)
        self.alien = Alien(self)
        self.alien.create_fleet()
        self.play_button = Button(self, "PLAY")

        self.stats = GameStats(self)
        self.stats.highscore = self.get_highscore()
        self.sb = Scoreboard(self)

        self.setup_sounds()

    def run_game(self):
        pygame.mixer.music.play(loops=-1)

        # Main loop
        while True:
            self.check_events()  # Watch for keyboard and mouse events
            if self.stats.game_active:  # Only when game is active
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
                self.explosions.update()
            self.update_screen()  # Update screen anyyway

    def get_highscore(self):
        try:
            with open("highscore.txt") as file:
                highscore = file.readline()
                if not highscore:
                    highscore = 0
                return int(highscore)
        except:
            print("cannot open highscore file")
            raise

    def setup_sounds(self):
        pygame.mixer.music.load("sounds/music.wav")
        pygame.mixer.music.set_volume(0.1)

        self.shooting_sounds = []
        sound_dir = os.path.join(os.path.dirname(__file__), "sounds")
        for sound in ["laser.wav", "laser2.wav"]:
            self.shooting_sounds.append(pygame.mixer.Sound(f"sounds/{sound}"))

        for s in self.shooting_sounds:
            s.set_volume(0.5)

        self.explosion_sound = pygame.mixer.Sound(
            os.path.join(sound_dir, "explosion.wav")
        )
        self.explosion_sound.set_volume(0.1)

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
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.ship.fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            pygame.mouse.set_visible(False)
            self.settings.setup_dynamic_settings()
            self.sb.prepare_score()
            self.sb.prepare_ships()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.aliens.empty()
            self.bullets.empty()
            self.alien.create_fleet()
            self.ship.center_ship()

    def update_bullets(self):
        self.bullets.update()  # Calls every instance's (in bullets) update method
        # Get rid of bullets that have disappeared from screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self):
        # Bullet-alien collision
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.explosion_sound.play()
            for aliens in collisions.values():  # if we hit many aliens at the same time
                self.stats.score += self.settings.alien_points * len(aliens)
                for alien in aliens:
                    explosion = Explosion(self)
                    explosion.set_explosion_center_and_object(
                        alien.rect.center, "alien"
                    )
                    self.explosions.add(explosion)
            self.sb.prepare_score()
            self.sb.check_highscore()

        # Check if no more aliens left -> we create a new fleet
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
            self.screen.fill(self.bg_color)
            self.play_button.draw_button()
        else:
            # self.screen.fill(self.bg_color)
            self.screen.blit(self.bg_image, self.screen.get_rect())
            self.ship.blitme()
            # self.ui_text.update_ship_position_text()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.explosions.draw(self.screen)
            self.sb.show_score()
        pygame.display.flip()  # Make the most recently drawn screen visible
