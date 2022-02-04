class GameStats:
    def __init__(self, game):
        self.settings = game.settings
        self.reset_stats()
        self.game_active = False
        self.highscore = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
