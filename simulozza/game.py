import pygame
import kezmenu

from simulozza.level import Level
from simulozza.data_file import data_file, level_names


class Menu(object):
    running = True

    def rungame(self):
        for level in level_names():
            succeeded = Level(self.screen, data_file(level), data_file('background.png')).run()
            if succeeded == False:
                return
        return

    def main(self, screen):
        clock = pygame.time.Clock()
        self.screen = screen
        background = pygame.image.load(data_file('background.png'))
        menu = kezmenu.KezMenu(
            ['Play!', self.rungame],
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
    screen = pygame.display.set_mode((1280, 760), pygame.FULLSCREEN)
    Menu().main(screen)

