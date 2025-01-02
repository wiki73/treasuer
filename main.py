import os
import sys
import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 30

        # Создаем массив спрайтов для каждой клетки
        self.sprites = [[None] * width for _ in range(height)]

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, offset_x, offset_y):
        for i in range(self.height):
            for j in range(self.width):
                # Если в клетке есть спрайт, отрисовываем его
                if self.sprites[i][j] is not None:
                    screen.blit(self.sprites[i][j], (offset_x + j * self.cell_size, offset_y + i * self.cell_size))
                else:
                    # Отрисовка пустой клетки (можно изменить цвет или оставить как есть)
                    pygame.draw.rect(screen, (60, 210, 92),
                                     (offset_x + j * self.cell_size,
                                      offset_y + i * self.cell_size,
                                      self.cell_size,
                                      self.cell_size), 1)


class Player:
    def __init__(self, pos_x, pos_y, board):
        self.pos_x = pos_x
        self.pos_y = pos_y  # Логическая позиция игрока
        self.board = board

    def move(self, direction):
        if direction == 'right':
            if self.pos_x < len(self.board.board[0]) - 1:
                self.pos_x += 1
                return True
        if direction == 'left' and self.pos_x > 0:
            self.pos_x -= 1
            return True
        if direction == 'bottom':
            if self.pos_y < len(self.board.board) - 1:
                self.pos_y += 1
                return True


class Game:
    def __init__(self):
        # Инициализация всех атрибутов игры
        pygame.init()
        size = width, height = 935, 660
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Инициализация игры')

        # Увеличиваем ширину на 34 клетки и высоту на еще 38 клеток.
        original_width = 17   # Исходная ширина поля
        original_height = 12   # Исходная высота поля

        new_width = original_width + 34   # Новая ширина поля
        new_height = original_height + 38   # Новая высота поля

        # Инициализация объектов игры с новыми размерами поля.
        self.board = Board(new_width, new_height)
        self.board.set_view(0, 165, 55)

        # Устанавливаем начальную позицию игрока.
        initial_pos_x = (self.board.width // 2) - 1   # Центрируем по X
        initial_pos_y = -1                             # На одну клетку выше поля

        # Создаем игрока с новыми координатами.
        self.player = Player(initial_pos_x, initial_pos_y, self.board)

    def load_image(self, name):
        fullname = os.path.join('', name)  # Используем только имя файла для загрузки изображения
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()

        image = pygame.image.load(fullname).convert_alpha()
        return image


if __name__ == '__main__':
    size = width, height = 935, 660
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    running = True

    game = Game()

    # Укажите только название файла для спрайта игрока и клеток.
    player_sprite_name = "player.png"      # Название файла спрайта игрока
    cell_sprite_name = "aufgeräumt.png"   # Название файла спрайта для клеток

    player_sprite_image = game.load_image(player_sprite_name)
    cell_sprite_image = game.load_image(cell_sprite_name)

    # Заполняем массив спрайтов для каждой клетки одним и тем же изображением.
    for i in range(game.board.height):
        for j in range(game.board.width):
            game.board.sprites[i][j] = cell_sprite_image

    move_direction = None
    last_move_time = pygame.time.get_ticks()
    move_interval = 800

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    move_direction = 'right'
                elif event.key == pygame.K_DOWN:
                    move_direction = 'bottom'

            if event.type == pygame.KEYUP:
                move_direction = None

        current_time = pygame.time.get_ticks()

        if move_direction and current_time - last_move_time >= move_interval:
            game.player.move(move_direction)

            last_move_time = current_time

        screen.fill((2, 137, 255))   # Устанавливаем цвет фона ниже поля

        # Вычисляем смещение для центрации камеры на игроке.
        offset_x = width // 2 - game.player.pos_x * game.board.cell_size
        offset_y = height // 2 - game.player.pos_y * game.board.cell_size

        # Отрисовка доски с учетом смещения.
        game.board.render(screen, offset_x, offset_y)

                               # Отрисовка спрайта игрока на логической позиции.
        sprite_rect_topleft = (game.player.pos_x * game.board.cell_size,
                               game.player.pos_y * game.board.cell_size)
        screen.blit(player_sprite_image, sprite_rect_topleft)

        pygame.display.flip()

    pygame.quit()