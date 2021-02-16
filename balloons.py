import pygame
import random

pygame.init()
size = 420, 420
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

colors_selection = {'orange': (246, 201, 130), 'white': (0, 0, 0),
                    'green': (185, 219, 147),
                    'blue': (127, 165, 248), 'pink': (222, 120, 157),
                    'yellow': (247, 206, 70), 'purple': (196, 94, 245)}


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

        x = cell[0]
        y = cell[1]

        if self.selected_cell is None:
            if self.board[y][x] == 1:
                self.selected_cell = x, y
            else:
                self.board[y][x] = 1

        else:
            if self.selected_cell == (x, y):
                self.selected_cell = None
                return

            x2 = self.selected_cell[0]
            y2 = self.selected_cell[1]
            if self.has_path(x2, y2, x, y):
                self.board[y][x] = 1
                self.board[y2][x2] = 0
                self.selected_cell = None

    # def help_color_choice(self):
    #     return random.choice(list(colors_selection.keys()))

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 1:
                    color = pygame.Color(colors_selection['blue'])
                    if self.selected_cell == (x, y):
                        color = pygame.Color(207, 57, 31)
                    pygame.draw.ellipse(screen, color,
                                        (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                         self.cell_size))

                pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                                 (x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                                  self.cell_size), 1)

    def check_pos(self):
        pass



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
