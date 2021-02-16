import os
import sys
import pygame

pygame.init()

FPS = 10
WIDTH = 400
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

def terminate():
    sys.exit()

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


def readfile(filename):
    screen.fill(pygame.Color("#333333"))
    text_coord = 3
    font = pygame.font.Font(None, 20)
    with open(filename,'rt') as f:
        read_data = list(map(str.strip, f.readlines()))
        for line in read_data:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()



def load_music(name):
    fullname = os.path.join('data', name)
    try:
        pygame.mixer.music.load(fullname)
        pygame.mixer.music.play(-1)
    except pygame.error as message:
        print('Cannot load music:', name)
        raise SystemExit(message)


def load_map_file(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def start_screen():
    global load_map
    # load_music('start.wav')
    x, y = None, None
    intro_text = ["Игра 'Морской бой'", "",
                  "Правила игры",
                  "Произвольно расставить шары",
                  "Начать игру"]

    menu_border = pygame.sprite.Group()
    fon = pygame.transform.scale(load_image('firstpctr.jfif'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 180
    for line in intro_text:
        sprite = pygame.sprite.Sprite()
        sprite.string_rendered = font.render(line, True, pygame.Color('white'))
        sprite.intro_rect = sprite.string_rendered.get_rect()
        menu_border.add(sprite)
        text_coord += 10
        sprite.intro_rect.top = text_coord
        sprite.intro_rect.x = 10
        text_coord += sprite.intro_rect.height
        screen.blit(sprite.string_rendered, sprite.intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for spr in menu_border:
                    if spr.intro_rect.collidepoint(event.pos):
                        index_in_nenu = menu_border.sprites().index(spr)
                        if index_in_nenu == 0:
                            return
                        elif index_in_nenu == 2:
                            readfile('data/Rules.txt')
                        # elif index_in_nenu == 4:
                        #     color = '#4169E1' if load_map else 'black'
                        #     pygame.draw.line(screen, pygame.Color(color), (10, 255), (287, 255), 2)
                        #     load_map = not load_map
                        elif index_in_nenu == 7:
                            return
        pygame.display.flip()


load_map, my_hero_image = False, None
start_screen()
# load_music('base.wav')
running, move, can_arrange = True, True, True
one = two = three = four = right = None
