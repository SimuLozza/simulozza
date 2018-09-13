import pygame

from simulozza.data_file import data_file


image_location = {
    "stand": (0, 0, 80, 110),
    "walk 1": (0, 110, 80, 110),
    "walk 2": (80, 110, 80, 110),
    "climb 1": (400, 0, 80, 110),
    "climb 2": (480, 0, 80, 110),
}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super().__init__(*groups)
        self.sheet = pygame.image.load(data_file('Daz-NPC.png'))
        self.set_image("stand")
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.rect.bottomleft = location
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

    def set_image(self, image_name, flip=False):
        location = image_location[image_name]
        image = self.sheet.subsurface(location)
        # if self.set_color:
        #     image = color_surface(image, self.set_color)
        if flip:
            image = pygame.transform.flip(image, True, False)
        # if self.player_shrunk:
        #     image = pygame.transform.scale(image, (30, 30))
        # if self.rect is not None:
        #     self.rect.size = image.get_size()
        self.image = image

    def animate(self, frame1, frame2, frame_time, flip=False):
        if self.animate_time > frame_time*2:
            self.animate_time = 0
        if self.animate_time < frame_time:
            self.set_image(frame1, flip)
        else:
            self.set_image(frame2, flip)
