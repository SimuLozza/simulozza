import pygame


def color_surface(surface, color):
    image = surface.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(color + (0, ), None, pygame.BLEND_RGBA_ADD)

    return image
