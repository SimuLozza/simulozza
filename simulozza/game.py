import pygame
import kezmenu

from simulozza.level import Level
from simulozza.data_file import data_file


class Menu(object):
    running = True

    def main(self, screen):
        clock = pygame.time.Clock()
        background = pygame.image.load(data_file('background.png'))
        menu = kezmenu.KezMenu(
            ['Play!', lambda: Level(screen, data_file('level-01.tmx'), data_file('background.png')).run()],
            ['Quit', lambda: setattr(self, 'running', False)],
        )
        menu.x = 200
        menu.y = 100
        menu.enableEffect('raise-col-padding-on-focus', enlarge_time=0.1)

        while self.running:
            menu.update(pygame.event.get(), clock.tick(30)/1000.)
            screen.blit(background, (0, 0))
            menu.draw(screen)
            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    Menu().main(pygame.display.set_mode((640, 480)))
