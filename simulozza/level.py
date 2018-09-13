
'''Basic platforming game.

Developed for the Intro to Game Programming tutorial at US PyCon 2012.

Copyright 2012 Richard Jones <richard@mechanicalcat.net>
This code is placed in the Public Domain.
'''
import pygame
from simulozza import tmx
from simulozza.data_file import data_file
from simulozza.npc import Enemy
from simulozza.player import Player
from simulozza.cloud import Cloud


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

        # add a separate layer for enemies so we can find them more easily later
        self.enemies = tmx.SpriteLayer()
        self.clouds = tmx.SpriteLayer()
        self.lightning = tmx.SpriteLayer()
        self.tilemap.layers.append(self.enemies)

        # add an enemy for each "enemy" trigger in the map
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            Enemy((enemy.px, enemy.py), self.enemies)
        # add an enemy for each "enemy" trigger in the map
        for cloud in self.tilemap.layers['triggers'].find('cloud'):
            Cloud((cloud.px, cloud.py), self.sprites)

        # load the sound effects used in playing a level of the game
        self.jump = pygame.mixer.Sound(data_file('jump.wav'))
        self.shoot = pygame.mixer.Sound(data_file('shoot.wav'))
        self.explosion = pygame.mixer.Sound(data_file('explosion.wav'))

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

            # update the tilemap and everything in it passing the elapsed time
            # since the last update (in seconds) and this Game object
            self.tilemap.update(dt / 1000., self)
            # construct the scene by drawing the background and then the rest of
            # the game imagery over the top
            self.screen.blit(self.background, (0, 0))
            self.tilemap.draw(self.screen)
            pygame.display.flip()

            # terminate this main loop if the player dies; a simple change here
            # could be to replace the "print" with the invocation of a simple
            # "game over" scene
            if self.player.is_dead:
                print('YOU DIED')
                return

            if self.tilemap.layers['triggers'].collide(self.player.rect, 'exit'):
                print('YOU WIN')
                return


if __name__ == '__main__':
    # if we're invoked as a program then initialise pygame, create a window and
    # run the game
    import sys
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Level(screen, data_file(sys.argv[1]), data_file('background.png')).run()
