import os
import sys
import pygame
import random

pygame.init()

FPS = 10
WIDTH = HEIGHT = 420
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
running = True


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
    with open(filename, 'rt', encoding='utf-8') as f:
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


def congratulations(winner):
    # load_music('final.wav')
    message = "Вы выиграли!" if winner else "Вы проиграли!"
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, pygame.Color("#000080"))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill(pygame.Color("#4682B4"))
        screen.blit(text, (text_x, text_y))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(20)
        pygame.display.flip()


def start_screen():
    global load_map
    load_music('first one.wav')
    x, y = None, None
    intro_text = ["Игра 'Линеечки'", "",
                  "Правила игры",
                  "Чтобы начать нажмите любую клавишу"]

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


COLORS_SELECTION = {'1': (255, 255, 255), '2': (243, 184, 177),
                    '3': (185, 219, 147),
                    '4': (127, 165, 248), '5': (222, 120, 157),
                    '6': (247, 206, 70), '7': (196, 94, 245)}


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # cell - кортеж (x, y)
    def on_click(self, cell):
        # заглушка для реальных игровых полей
        pass

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell and cell < (self.width, self.height):
            self.on_click(cell)


class Lines(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.selected_cell = None
        self.kol = 0

    def has_path(self, x1, y1, x2, y2):
        # словарь расстояний
        d = {(x1, y1): 0}
        v = [(x1, y1)]  # список возможных маршрутов
        while len(v) > 0:
            x, y = v.pop(0)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    # по вертикали либо горизонтали
                    if dx * dy != 0:
                        continue
                    # за пределы поля не выходим
                    if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                        continue
                    if self.board[y + dy][x + dx] == 0:
                        dn = d.get((x + dx, y + dy), -1)
                        # обратно в точки посещенные не возвращаемся
                        if dn == -1:
                            d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                            v.append((x + dx, y + dy))
                            if v[-1] == (x2, y2):
                                return True
        return False

    def on_click(self, cell):
        # "распаковка" координат клетки
        x = cell[0]
        y = cell[1]

        if self.selected_cell is None:
            # если в выбранной клетке совсем ничего нет, то
            if self.board[y][x] != 0:  # содержимого нет
                self.selected_cell = x, y
            else:
                self.board[y][x] = random.randint(1, 7)  # заполняется клетка шариком рандомного цвета
                # расстановка 2 шариков рандомных цветов
                self.board[random.randrange(10)][random.randrange(10)] = random.randint(1, 7)
                self.board[random.randrange(10)][random.randrange(10)] = random.randint(1, 7)
        else:
            if self.selected_cell == (x, y):
                self.selected_cell = None
                return
            # перемещение
            x2 = self.selected_cell[0]
            y2 = self.selected_cell[1]
            if self.has_path(x2, y2, x, y):
                # меняем местами содержимое клеток
                self.board[y][x], self.board[y2][x2] = self.board[y2][x2], self.board[y][x]
                # self.board[y][x] = colors_selection
                # self.board[y2][x2] = 0
                self.selected_cell = None

    # проверка на "3 в ряд"
    def check(self, x, y):
        global kol
        try:
            if self.board[y][x] == self.board[y][x + 1] == self.board[y][x + 2]:  # если в ряду 3 одинаковых
                self.kol += 1
                self.board[y][x], self.board[y][x + 1], self.board[y][x + 2] = 0, 0, 0  # удаляем их
            elif self.board[y][x] == self.board[y + 1][x] == self.board[y + 2][x]:  # если в столбце 3 одинаковых
                self.kol += 1
                self.board[y][x], self.board[y + 1][x], self.board[y + 2][x] = 0, 0, 0  # удаляем их
            kol = self.kol
            return
        except IndexError:  # если за границы поля выходим
            pass  # заглушка, чтобы ничего не происходило

    # воспроизведение отрисовки шариков / прямоугольников на пустых местах
    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 0:  # если ячейка не пуста
                    color = pygame.Color(COLORS_SELECTION[str(self.board[y][x])])  # придаем шарику опред. цвет
                    self.check(x, y)  # делаем проверку на схожесть соседних шариков
                    if self.selected_cell == (x, y):  # если выбранная клетка соответствует заполненной
                        color = pygame.Color(207, 57, 31)  # красим в красный
                    # отрисовка кружочка на поле
                    pygame.draw.ellipse(screen, color,
                                        (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                         self.cell_size))
                # отрисовка прямоугольника в образовавшемся пустом месте
                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  self.cell_size), 1)


load_map = False
start_screen()
# load_music('base.wav')
winner, kol = False, 0
screen = pygame.display.set_mode((420, 420))
clock = pygame.time.Clock()
board = Lines(10, 10)
board.set_view(10, 10, 40)

while running == True:
    while kol != 10:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)

        screen.fill((0, 0, 0))
        board.render()
        pygame.display.flip()
        clock.tick(50)
    if pygame.time.get_ticks() < 60000 and kol == 10:
        winner = True
    else:
        winner = False
    congratulations(winner)
terminate()
