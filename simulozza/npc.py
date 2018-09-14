import pygame

from simulozza.data_file import data_file
from simulozza.text import text_to_screen


class Enemy(pygame.sprite.Sprite):
    image_sheet = 'Daz-NPC.png'
    image_location = {
        "stand": (0, 0, 80, 110),
        "walk 1": (0, 110, 80, 110),
        "walk 2": (80, 110, 80, 110),
        "climb 1": (400, 0, 80, 110),
        "climb 2": (480, 0, 80, 110),
    }

    def __init__(self, location, *groups):
        super().__init__(*groups)
        self.sheet = pygame.image.load(data_file(self.image_sheet))
        self.set_image("stand")
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.rect.bottomleft = location
        # movement in the X direction; positive is right, negative is left
        self.direction = 1
        self.animate_time = 0
        self.dead = False

    def update(self, dt, game):
        self.animate_time += dt
        # move the enemy by 100 pixels per second in the movement direction
        self.rect.x += self.direction * 100 * dt
        move = 0
        # check all reverse triggers in the map to see whether this enemy has
        # touched one
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
            # reverse movement direction; make sure to move the enemy out of the
            # collision so it doesn't collide again immediately next update
            if self.direction > 0:
                self.rect.right = cell.left
                move = -300 * dt
            else:
                self.rect.left = cell.right
                move += 300 * dt
            self.direction *= -1
            break

        self.rect.x += move

        if self.direction > 0:
            self.animate("walk 1", "walk 2", .20)
        elif self.direction < 0:
            self.animate("walk 1", "walk 2", .20, flip=True)

        # check for collision with the player; on collision mark the flag on the
        # player to indicate game over (a health level could be decremented here
        # instead)
        if self.rect.colliderect(game.player.collide_rect):
            game.player.hurt()

    def set_image(self, image_name, flip=False):
        location = self.image_location[image_name]
        image = self.sheet.subsurface(location)
        if flip:
            image = pygame.transform.flip(image, True, False)
        self.image = image

    def animate(self, frame1, frame2, frame_time, flip=False):
        if self.animate_time > frame_time*2:
            self.animate_time = 0
        if self.animate_time < frame_time:
            self.set_image(frame1, flip)
        else:
            self.set_image(frame2, flip)


class Bug(Enemy):
    image_sheet = 'enemies.png'
    image_location = {
        "stand": (0, 326, 71, 45),
        "walk 1": (0, 90, 72, 51),
        "walk 2": (0, 37, 77, 53),
    }
    def set_image(self, image_name, flip=False):
        super().set_image(image_name, flip=not flip)


class Matt(pygame.sprite.Sprite):
    image_sheet = 'Matt.png'
    image_location = {
        "stand": (0, 0, 80, 110),
    }

    def __init__(self, location, *groups):
        super().__init__(*groups)
        self.sheet = pygame.image.load(data_file(self.image_sheet))
        self.set_image("stand")
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.rect.bottomleft = location
        # movement in the X direction; positive is right, negative is left
        self.direction = 1
        self.animate_time = 0
        self.dead = False

    def update(self, dt, game):
        if self.rect.colliderect(game.player.collide_rect):
            game.player.won = True

    def set_image(self, image_name, flip=False):
        location = self.image_location[image_name]
        image = self.sheet.subsurface(location)
        if flip:
            image = pygame.transform.flip(image, True, False)
        self.image = image
