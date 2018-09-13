import pygame

from simulozza.data_file import data_file


def text_to_screen(surface, text, x, y, size=50, color=(255, 255, 255), align='left',
                   font_type=data_file('VT220-mod.ttf')):
    font = pygame.font.Font(font_type, size)
    text = font.render(text, True, color)
    if align == 'center':
        w, h = text.get_size()
        x -= w // 2
        h -= h // 2
    surface.blit(text, (x, y))
