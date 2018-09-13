import pygame

from simulozza.data_file import data_file


class HealthIcon(pygame.sprite.Sprite):
    image_good = pygame.image.load(data_file('hud_heartFull.png'))
    image_bad = pygame.image.load(data_file('hud_heartEmpty.png'))

    def __init__(self, num, *groups):
        super().__init__(*groups)
        self.num = num
        self.image = self.image_good
        w = self.image.get_size()[0]
        self.rect = pygame.rect.Rect((num * w, 0), self.image.get_size())

    def update(self, dt, game):
        if game.player.lives > self.num:
            self.image = self.image_good
        else:
            self.image = self.image_bad
