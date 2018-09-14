import pygame

from simulozza.data_file import data_file


class Bullet(pygame.sprite.Sprite):
    image = pygame.image.load(data_file('swear.png'))

    def __init__(self, location, direction, *groups):
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        # movement in the X direction; positive is right, negative is left;
        # supplied by the player (shooter)
        self.direction = direction
        # time this bullet will live for in seconds
        self.lifespan = 1

    def update(self, dt, game):
        # decrement the lifespan of the bullet by the amount of time passed and
        # remove it from the game if its time runs out
        self.lifespan -= dt
        if self.lifespan < 0:
            self.kill()
            return

        # move the enemy by 400 pixels per second in the movement direction
        self.rect.x += self.direction * 400 * dt

        # check for collision with any of the enemy sprites; we pass the "kill
        # if collided" flag as True so any collided enemies are removed from the
        # game
        if pygame.sprite.spritecollide(self, game.enemies, True):
            game.explosion.play()
            # we also remove the bullet from the game or it will continue on
            # until its lifespan expires
            self.kill()


class Punch(pygame.sprite.Sprite):
    image = pygame.image.load(data_file('transparent.png'))

    def __init__(self, location, direction, *groups):
        super().__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        # movement in the X direction; positive is right, negative is left;
        # supplied by the player (shooter)
        self.direction = direction
        #self.direction = direction
        # time this bullet will live for in seconds
        self.lifespan = 2

    def update(self, dt, game):
        # decrement the lifespan of the bullet by the amount of time passed and
        # remove it from the game if its time runs out
        self.lifespan -= dt
        if self.lifespan < 0:
            self.kill()
            return

        # move the enemy by 400 pixels per second in the movement direction
        #self.rect.x += self.direction * 400 * dt

        # check for collision with any of the enemy sprites; we pass the "kill
        # if collided" flag as True so any collided enemies are removed from the
        # game
        if pygame.sprite.spritecollide(self, game.enemies, True):
            image = pygame.image.load(data_file('enemy.png'))
            game.punch.play()
            # we also remove the bullet from the game or it will continue on
            # until its lifespan expires
            self.kill()
>>>>>>> 05520480ef5c463309dfc877f5c677cdaa14addb
