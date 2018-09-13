import pygame

from simulozza.data_file import data_file


class Enemy(pygame.sprite.Sprite):
    image = pygame.image.load(data_file('enemy.png'))

    def __init__(self, location, *groups):
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        # movement in the X direction; positive is right, negative is left
        self.direction = 1

    def update(self, dt, game):
        # move the enemy by 100 pixels per second in the movement direction
        self.rect.x += self.direction * 100 * dt

        # check all reverse triggers in the map to see whether this enemy has
        # touched one
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
            # reverse movement direction; make sure to move the enemy out of the
            # collision so it doesn't collide again immediately next update
            if self.direction > 0:
                self.rect.right = cell.left
            else:
                self.rect.left = cell.right
            self.direction *= -1
            break

        # check for collision with the player; on collision mark the flag on the
        # player to indicate game over (a health level could be decremented here
        # instead)
        if self.rect.colliderect(game.player.collide_rect):
            game.player.hurt()
