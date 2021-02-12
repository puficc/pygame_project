import os
import pygame

pygame.init()

fps = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((720, 720))


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Level(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image = pygame.transform.scale(
            load_image('main_map.png', -1), (720, 720))
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = -3050
        self.mask = pygame.mask.from_surface(self.image)
