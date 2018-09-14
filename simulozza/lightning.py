import pygame

from simulozza.data_file import data_file


class Lightning(pygame.sprite.Sprite):
    image = pygame.image.load(data_file('lightning.png'))

    def __init__(self, location, *groups):
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.life_span = 0.25


    def update(self, dt, game):

        self.life_span = max(0, self.life_span - dt)
        # check for collision with the player; on collision mark the flag on the
        # player to indicate game over (a health level could be decremented here
        # instead)

        if self.life_span == 0:
            self.kill()

        if self.rect.colliderect(game.player.collide_rect):
            game.player.is_dead = True
