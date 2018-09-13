import pygame

from simulozza.data_file import data_file
from simulozza.objects import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super().__init__(*groups)
        self.image = self.stand_image = pygame.image.load(data_file('female_stand.png'))
        self.walk_image = pygame.image.load(data_file('female_walk1.png'))
        self.rect = pygame.rect.Rect((0,0), self.image.get_size())
        self.rect.bottomleft = location
        # is the player resting on a surface and able to jump?
        self.resting = False
        # player's velocity in the Y direction
        self.dy = 0
        # is the player dead?
        self.is_dead = False
        # movement in the X direction; postive is right, negative is left
        self.direction = 1
        # time since the player last shot
        self.gun_cooldown = 0

    def update(self, dt, game):
        # take a copy of the current position of the player before movement for
        # use in movement collision response
        last = self.rect.copy()

        # handle the player movement left/right keys
        key = pygame.key.get_pressed()
        move = 0
        if key[pygame.K_LEFT]:
            move = -300 * dt
        if key[pygame.K_RIGHT]:
            move += 300 * dt

        if move > 0:
           self.rect.x += move
           self.image = self.walk_image
           self.direction = 1
        elif move < 0:
            self.rect.x += move
            self.image = pygame.transform.flip(self.walk_image, True, False)
            self.direction = -1
        elif self.direction > 0:
            self.image = self.stand_image
        else:
            self.image =  pygame.transform.flip(self.stand_image, True, False)

        # handle the player shooting key
        if key[pygame.K_LSHIFT] and not self.gun_cooldown:
            # create a bullet at an appropriate position (the side of the player
            # sprite) and travelling in the correct direction
            if self.direction > 0:
                Bullet(self.rect.midright, 1, game.sprites)
            else:
                Bullet(self.rect.midleft, -1, game.sprites)
            # set the amount of time until the player can shoot again
            self.gun_cooldown = 1
            game.shoot.play()

        # decrement the time since the player last shot to a minimum of 0 (so
        # boolean checks work)
        self.gun_cooldown = max(0, self.gun_cooldown - dt)

        # if the player's allowed to let them jump with the spacebar; note that
        # wall-jumping could be allowed with an additional "touching a wall"
        # flag
        if self.resting and key[pygame.K_SPACE]:
            game.jump.play()
            # we jump by setting the player's velocity to something large going
            # up (positive Y is down the screen)
            self.dy = -500

        # add gravity on to the currect vertical speed
        self.dy = min(400, self.dy + 40)

        # now add the distance travelled for this update to the player position
        self.rect.y += self.dy * dt

        # collide the player with the map's blockers
        new = self.rect
        # reset the resting trigger; if we are at rest it'll be set again in the
        # loop; this prevents the player from being able to jump if they walk
        # off the edge of a platform
        self.resting = False
        # look up the tilemap triggers layer for all cells marked "blockers"
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            # find the actual value of the blockers property
            blockers = cell['blockers']
            # now for each side set in the blocker check for collision; only
            # collide if we transition through the blocker side (to avoid
            # false-positives) and align the player with the side collided to
            # make things neater
            if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                # reset the vertical speed if we land or hit the roof; this
                # avoids strange additional vertical speed if there's a
                # collision and the player then leaves the platform
                self.dy = 0
            if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0

        for cell in game.tilemap.layers['triggers'].collide(new, 'lava'):
            self.is_dead = True

        for cell in game.tilemap.layers['triggers'].collide(new, 'spikes'):
            self.is_dead = True

        # re-focus the tilemap viewport on the player's new position
        game.tilemap.set_focus(new.x, new.y)
