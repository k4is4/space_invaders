class UIText:
    def __init__(self, game):
        self.settings = game.settings
        self.screen = game.screen

        self.text_color = (255, 255, 255)
        self.font = self.settings.font
        self.ship = game.ship

    def update_ship_position_text(self):
        coords = str(self.ship.rect.x)
        ship_pos_text = self.font.render(coords, True, self.text_color)
        ship_pos_rect = ship_pos_text.get_rect()
        ship_pos_rect.topleft = (20, 20)
        self.screen.blit(ship_pos_text, ship_pos_rect)
