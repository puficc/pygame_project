import pygame
import random

pygame.init()
size = 420, 420
winner = False
kol = 0
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

colors_selection = {'1': (243, 183, 86), '2': (0, 0, 0),
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


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------


class Lines(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.selected_cell = None

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
                self.board[y][x] = 1  # заполняется клетка шариком цвета 1
                # расстановка 2 шариков рандомных цветов
                self.board[random.randrange(10)][random.randrange(10)] = random.randrange(7)
                self.board[random.randrange(10)][random.randrange(10)] = random.randrange(7)
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
        try:
            if self.board[y][x] == self.board[y][x + 1] == self.board[y][x + 2]:  # если в ряду 3 одинаковых
                # kol += 1
                self.board[y][x], self.board[y][x + 1], self.board[y][x + 2] = 0, 0, 0  # удаляем их
            elif self.board[y][x] == self.board[y + 1][x] == self.board[y + 2][x]:  # если в столбце 3 одинаковых
                # kol += 1
                self.board[y][x], self.board[y + 1][x], self.board[y + 2][x] = 0, 0, 0  # удаляем их
            return
        except IndexError:  # если за границы поля выходим
            pass  # заглушка, чтобы ничего не происходило

    # воспроизведение отрисовки шариков / прямоугольников на пустых местах
    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 0:  # если ячейка не пуста
                    color = pygame.Color(colors_selection[str(self.board[y][x])])  # придаем шарику опред. цвет
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


board = Lines(10, 10)
board.set_view(10, 10, 40)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)

    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
    clock.tick(50)
pygame.quit()
