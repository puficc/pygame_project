import os
import pygame

pygame.init()

FPS = 10
WIDTH = 400
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


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


tiles_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x + 10, tile_height * pos_y + 10)


def generate_map(my_map, my_board):
    for y in range(len(my_map)):
        for x in range(len(my_map[y])):
            if my_map[y][x] == '.':
                Tile('water', x, y)
            else:
                Tile('boat', x, y)
                my_board.board[y][x] = int(my_map[y][x])


def start_screen():
    global load_map
    load_music('start.wav')
    x, y = None, None
    intro_text = ["Игра 'Линеечки'", "",
                  "Правила игры",
                  "Произвольная карта",
                  "Начать игру"]
    menu_border = pygame.sprite.Group()
    fon = pygame.transform.scale(load_image('firstpctr.jfif'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font('bodoni', 30)
    text_coord = 100
    for line in intro_text:
        sprite = pygame.sprite.Sprite()
        sprite.string_rendered = font.render(line, True, pygame.Color('black'))
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
                    elif index_in_nenu == 3:
                        choose_hero(menu_hero)
                    elif index_in_nenu == 4:
                        color = '#4169E1' if load_map else 'black'
                        pygame.draw.line(screen, pygame.Color(color), (10, 255), (287, 255), 2)
                        load_map = not load_map
                    elif index_in_nenu == 5:
                        readfile('data/Help.txt')
                    elif index_in_nenu == 7:
                        return
    pygame.display.flip()

load_map, my_hero_image = False, None
start_screen()
load_music('base.wav')
en_board = EnemyBoard(10, 10)
my_board = MyBoard(10, 10)
en_board.take_a_cage()
running, move, can_arrange = True, True, True
one = two = three = four = right = None
if load_map:
    tile_width = tile_height = 40
    tile_images = {'water': pygame.transform.scale(load_image('water.jpg'),
                                                   (tile_width, tile_height)),
                   'boat': pygame.transform.scale(load_image('one.png'), (tile_width, tile_height))}

    generate_map(load_map_file(choice(['first_test_map.txt', 'second_test_map.txt'])), my_board)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not load_map and can_arrange:
                my_board.get_click(event.pos)
            else:
                if move:
                    en_board.get_click(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                right = True
            elif event.key == pygame.K_DOWN:
                right = False
            elif event.key == pygame.K_1:
                one, two, three, four = True, False, False, False
            elif event.key == pygame.K_2:
                one, two, three, four = False, True, False, False
            elif event.key == pygame.K_3:
                one, two, three, four = False, False, True, False
            elif event.key == pygame.K_4:
                one, two, three, four = False, False, False, True
    if not move:
        my_board.attack()
    screen.fill((0, 0, 0))
    if my_hero_image:
        screen.blit(pygame.transform.scale(load_image(my_hero_image), (120, 140)), (150, 440))
        screen.blit(pygame.transform.scale(load_image(HERO_LIST[1 - HERO_LIST.index(my_hero_image)]),
                                           (120, 140)),
                    (600, 440))
    else:
        screen.blit(pygame.transform.scale(load_image(HERO_LIST[0]), (120, 140)), (150, 440))
        screen.blit(pygame.transform.scale(load_image(HERO_LIST[1]), (120, 140)), (600, 440))
    if load_map:
        tiles_group.draw(screen)
    total_play(my_total=en_board.cnt_hit_enemy_board,
               enemy_total=my_board.cnt_my_board_kill)
    my_board.render()
    en_board.render()
    pygame.display.flip()
terminate()
