
'''Basic platforming game.

Developed for the Intro to Game Programming tutorial at US PyCon 2012.

Copyright 2012 Richard Jones <richard@mechanicalcat.net>
This code is placed in the Public Domain.
'''
import pygame
from simulozza import tmx
from simulozza.data_file import data_file
from simulozza.health import HealthIcon
from simulozza.npc import Enemy
from simulozza.player import Player
from simulozza.text import text_to_screen


class Level(object):
    def __init__(self, screen, level_map, background):
        self.screen = screen

        # we draw the background as a static image so we can just load it in the
        # main loop
        self.background = pygame.image.load(background)

        # load our tilemap and set the viewport for rendering to the screen's
        # size
        self.tilemap = tmx.load(level_map, screen.get_size())

        # add a layer for our sprites controlled by the tilemap scrolling
        self.sprites = tmx.SpriteLayer()
        self.tilemap.layers.append(self.sprites)
        # fine the player start cell in the triggers layer
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        # use the "pixel" x and y coordinates for the player start
        self.player = Player((start_cell.px, start_cell.py), self.sprites)

        self.gui = pygame.sprite.Group()
        [self.gui.add(HealthIcon(i)) for i in range(3)]

        # add a separate layer for enemies so we can find them more easily later
        self.enemies = tmx.SpriteLayer()
        self.tilemap.layers.append(self.enemies)
        # add an enemy for each "enemy" trigger in the map
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            Enemy((enemy.px, enemy.py), self.enemies)

        # load the sound effects used in playing a level of the game
        self.jump = pygame.mixer.Sound(data_file('jump.wav'))
        self.shoot = pygame.mixer.Sound(data_file('shoot.wav'))
        self.explosion = pygame.mixer.Sound(data_file('explosion.wav'))

        self.level_complete = False

    def run(self):
        # grab a clock so we can limit and measure the passing of time
        clock = pygame.time.Clock()

        while 1:
            # limit updates to 30 times per second and determine how much time
            # passed since the last update
            dt = clock.tick(30)

            # handle basic game events; terminate this main loop if the window
            # is closed or the escape key is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return
                self.player.handle_event(self, event)

            if not (self.player.is_dead or self.level_complete):
                # update the tilemap and everything in it passing the elapsed time
                # since the last update (in seconds) and this Game object
                self.tilemap.update(dt / 1000., self)
                self.gui.update(dt / 1000., self)

            # construct the scene by drawing the background and then the rest of
            # the game imagery over the top
            self.screen.fill((0, 0, 0))
            self.tilemap.draw(self.screen)
            self.gui.draw(self.screen)

            # terminate this main loop if the player dies; a simple change here
            # could be to replace the "print" with the invocation of a simple
            # "game over" scene
            if self.player.is_dead:
                x, y = self.screen.get_size()
                text_to_screen(self.screen, 'You Died!', x//2, y//2, align='center')

            if self.tilemap.layers['triggers'].collide(self.player.collide_rect, 'exit'):
                self.level_complete = True
                x, y = self.screen.get_size()
                text_to_screen(self.screen, 'Well done!', x//2, y//2, align='center')

            pygame.display.flip()


if __name__ == '__main__':
    # if we're invoked as a program then initialise pygame, create a window and
    # run the game
    import sys
    pygame.init()
    screen = pygame.display.set_mode((1280, 760))  # , pygame.FULLSCREEN)
    Level(screen, data_file(sys.argv[1]), data_file('background.png')).run()
