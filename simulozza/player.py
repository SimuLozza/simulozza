import pygame

from simulozza.color_surface import color_surface
from simulozza.data_file import data_file
from simulozza.objects import Bullet
from simulozza.objects import Punch

image_location = {
    "stand": (0, 0, 80, 110),
    "walk 1": (0, 110, 80, 110),
    "walk 2": (80, 110, 80, 110),
    "climb 1": (415, 0, 80, 110),
    "climb 2": (480, 0, 80, 110),
    "jumping": (80, 0, 80, 110),
    "falling": (560, 0, 80, 110),
    "punch 1": (160, 110, 80, 110),
    "punch 2": (240, 110, 80, 110),
    "dead": (340, 0, 80, 110),
}

class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super().__init__(*groups)
        self.player_shrunk = False
        self.rect = None
        self.set_color = False
        self.sheet = pygame.image.load(data_file('lauren_tilesheet.png'))
        self.set_image("stand")
        self.rect = pygame.rect.Rect((0, 0), self.image.get_size())
        self.rect.bottomleft = location
        # is the player resting on a surface and able to jump?
        self.resting = False
        self.mid_air = False
        self.already_double_jumped = False
        # player's velocity in the Y direction
        self.dy = 0
        # movement in the X direction; postive is right, negative is left
        self.direction = 1
        # time since the player last shot
        self.gun_cooldown = 0
        self.jump_cooldown = 0
        self.punch_cooldown = 0
        self.on_ladder = False
        self.animate_time = 0
        self.animate_frame = ''

        # is the player dead?
        self.is_dead = False
        self.lives = 3
        self.hurt_cooldown = 0

    def hurt(self):
        if self.hurt_cooldown > 0:
            return
        self.lives -= 1
        self.hurt_cooldown = 1
        if self.lives <= 0:
            self.is_dead = True

    @property
    def collide_rect(self):
        w, h = self.rect.size
        if self.player_shrunk:
            w -= 10
        else:
            w -= 30
        r = pygame.rect.Rect((0, 0), (w, h))
        r.midbottom = self.rect.midbottom
        return r

    def set_image(self, image_name, flip=False):
        location = image_location[image_name]
        image = self.sheet.subsurface(location)
        if self.set_color:
            image = color_surface(image, self.set_color)
        if flip:
            image = pygame.transform.flip(image, True, False)
        if self.player_shrunk:
            image = pygame.transform.scale(image, (30, 30))
        if self.rect is not None:
            midbot = self.rect.midbottom
            self.rect.size = image.get_size()
            self.rect.midbottom = midbot
        self.image = image

    def animate(self, frame1, frame2, frame_time, flip=False):
        if self.animate_time > frame_time*2:
            self.animate_time = 0
        if self.animate_time < frame_time:
            self.set_image(frame1, flip)
        else:
            self.set_image(frame2, flip)

    def handle_event(self, game, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump(game)
            elif event.key == pygame.K_z and not self.gun_cooldown:
                self.shoot(game)
            elif event.key == pygame.K_x and not self.punch_cooldown:
                self.punch(game)

    def jump(self, game):
        # if the player's allowed to let them jump with the spacebar; note that
        # wall-jumping could be allowed with an additional "touching a wall"
        # flag
        if self.resting:
            game.jump.play()
            # we jump by setting the player's velocity to something large going
            # up (positive Y is down the screen)
            self.dy = -500
            self.mid_air = True
            self.jump_cooldown = 0.25

        elif self.mid_air and not self.already_double_jumped and not self.jump_cooldown:
            game.double_jump.play()
            self.dy = -500
            self.already_double_jumped = True
            self.jump_cooldown = 0.25

    def update(self, dt, game):
        self.animate_time += dt
        # take a copy of the current position of the player before movement for
        # use in movement collision response
        last = self.collide_rect

        self.on_ladder = False
        for cell in game.tilemap.layers['triggers'].collide(last, 'ladder'):
            self.on_ladder = True

        # handle the player movement left/right keys
        key = pygame.key.get_pressed()
        move = 0
        if key[pygame.K_LEFT]:
            move = -300 * dt
        if key[pygame.K_RIGHT]:
            move += 300 * dt

        if move > 0:
            self.rect.x += move
            self.animate("walk 1", "walk 2", .20)
            self.direction = 1
        elif move < 0:
            self.rect.x += move
            self.animate("walk 1", "walk 2", .20, flip=True)
            self.direction = -1
        elif self.direction > 0:
            self.set_image("stand")
        else:
            self.set_image("stand", flip=True)

        # decrement the time since the player last shot to a minimum of 0 (so
        # boolean checks work)
        self.gun_cooldown = max(0, self.gun_cooldown - dt)
        self.hurt_cooldown = max(0, self.hurt_cooldown - dt)
        self.jump_cooldown = max(0, self.jump_cooldown - dt)
        self.punch_cooldown = max(0, self.punch_cooldown - dt)

        self.set_color = None
        if self.hurt_cooldown > 0:
            if (self.hurt_cooldown % 0.25) > 0.125:
                self.set_color = (255, 255, 255)

        if self.on_ladder:
            if key[pygame.K_UP]:
                self.animate('climb 1', 'climb 2', .20)
                self.dy = -200
                # def animate(frame1, frame2, frame_time):
            elif key[pygame.K_DOWN]:
                self.animate('climb 1', 'climb 2', .30)
                self.dy = +200
            else:
                self.dy = 0
        else:
            # add gravity on to the currect vertical speed
            self.dy = min(400, self.dy + 40)

        if self.punch_cooldown > 0:
            if self.direction > 0:
                self.set_image("punch 1")
            else:
                self.set_image("punch 1", flip=True)

        # now add the distance travelled for this update to the player position
        self.rect.y += self.dy * dt

        # collide the player with the map's blockers
        new = self.collide_rect

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
                self.mid_air = False
                self.already_double_jumped = False
                new.bottom = cell.top
                # reset the vertical speed if we land or hit the roof; this
                # avoids strange additional vertical speed if there's a
                # collision and the player then leaves the platform
                self.dy = 0
            if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0

        if not self.resting and not self.on_ladder:
            if self.dy < 0:
                if self.direction > 0:
                    self.set_image("jumping")
                else:
                    self.set_image("jumping", flip=True)
            else:
                if self.direction > 0:
                    self.set_image("falling")
                else:
                    self.set_image("falling", flip=True)

        for cell in game.tilemap.layers['triggers'].collide(new, 'lava'):
            self.hurt()

        for cell in game.tilemap.layers['triggers'].collide(new, 'spikes'):
            self.hurt()

        for teleporter in game.tilemap.layers['triggers'].collide(new, 'teleport'):
            if teleporter['teleport_exit'] == 'true':
                continue
            for target in game.tilemap.layers['triggers'].match (teleport=teleporter['teleport'],
                                                                 teleport_exit='true'):
                 new.bottom = target.bottom
                 new.left = target.left

        for cell in game.tilemap.layers['triggers'].collide(new, 'shrink'):
            self.player_shrunk = True

        for cell in game.tilemap.layers['triggers'].collide(new, 'expand'):
            self.player_shrunk = False

        if self.is_dead:
            self.set_image("dead")

        # this reassignment of the image rect must be here at the bottom
        self.rect.midbottom = new.midbottom

        # re-focus the tilemap  viewport on the player's new position
        game.tilemap.set_focus(new.x, new.y)

    def shoot(self, game):

        # create a bullet at an appropriate position (the side of the player
        # sprite) and travelling in the correct direction
        if self.direction > 0:
            Bullet(self.rect.midright, 1, game.sprites)
        else:
            Bullet(self.rect.midleft, -1, game.sprites)
        # set the amount of time until the player can shoot again
        self.gun_cooldown = 1
        game.shoot.play()

    def punch(self, game):
        # ADD ANIMATION

        # create a bullet at an appropriate position (the side of the player
        # sprite) and travelling in the correct direction
        if self.direction > 0:
            Punch(self.rect.midright, 1, game.sprites)
        else:
            Punch(self.rect.midleft, -1, game.sprites)
        # set the amount of time until the player can shoot again
        self.punch_cooldown = 0.5
        game.punch.play()

