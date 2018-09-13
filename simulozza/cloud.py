import pygame

from simulozza.data_file import data_file
from simulozza.lightning import Lightning


class Cloud(pygame.sprite.Sprite):
    image = pygame.image.load(data_file('cloud9.png'))

    def __init__(self, location, *groups):
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.lightning_timer = 0

    def update(self, dt, game):
        self.lightning_timer = max(0, self.lightning_timer - dt)

        if self.lightning_timer == 0:
            for lightning in game.tilemap.layers['triggers'].find('lightning'):
                Lightning((lightning.px, lightning.py), game.sprites)
            self.lightning_timer = 1.5
