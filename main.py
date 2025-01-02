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
        self.cell_width = 68  # Ширина клетки изменена на 108 пикселей
        self.cell_height = 52  # Высота клетки изменена на 78 пикселей
        self.cell_image = pygame.transform.scale(self.load_image('aufgeräumt.png'), (
        self.cell_width, self.cell_height))  # Загружаем и изменяем размер изображения клетки

    def load_image(self, name, colorkey=None):
        if not os.path.isfile(name):
            print(f"Файл с изображением '{name}' не найден")
            sys.exit()

        image = pygame.image.load(name)

        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()

        return image

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top

    def render(self, screen, offset_x, offset_y):
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                if elem == 1:
                    # Здесь можно добавить логику для отрисовки заполненной клетки (если необходимо)
                    pass
                else:
                    # Отрисовка клетки с использованием загруженного изображения
                    rect = (
                        offset_x + j * self.cell_width,
                        offset_y + i * self.cell_height,
                        self.cell_width,
                        self.cell_height
                    )
                    screen.blit(self.cell_image, rect)  # Отрисовываем изображение клетки на экране


class Player:
    def __init__(self, pos_x, pos_y, board):
        self.pos_x = pos_x
        self.pos_y = pos_y
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
        i_width = 51  # Исходная ширина поля
        i_height = 50  # Исходная высота поля

        # Инициализация объектов игры с новыми размерами поля.
        self.board = Board(i_width, i_height)
        self.board.set_view(0, 165, 55)

        # Устанавливаем начальную позицию игрока на одну клетку ниже поля.
        initial_pos_x = (self.board.width // 2) - 1  # Центрируем по X
        initial_pos_y = -1  # На одну клетку выше поля

        # Создаем игрока с новыми координатами.
        self.player = Player(initial_pos_x, initial_pos_y, self.board)

        # Инициализация группы спрайтов.
        self.all_sprites = pygame.sprite.Group()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()

        image = pygame.image.load(fullname)

        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()

        return image

    def set_player(self):
        # Метод для установки позиции игрока на доске.
        pass


if __name__ == '__main__':
    size = width, height = 935, 660
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    running = True

    game = Game()

    sprite = pygame.sprite.Sprite()
    sprite.image = game.load_image('player.png')

    # Устанавливаем начальную позицию спрайта с учетом того,
    # что он должен быть на одной клетке ниже поля.
    sprite.rect = sprite.image.get_rect(topleft=(game.board.cell_width * game.player.pos_x,
                                                 game.board.cell_height * (game.player.pos_y + 2)))

    game.all_sprites.add(sprite)

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
            if move_direction == 'left':
                game.player.move('left')
            elif move_direction == 'right':
                game.player.move('right')
            elif move_direction == 'bottom':
                game.player.move('bottom')

            last_move_time = current_time

        screen.fill((2, 137, 255))  # Изменяем цвет фона ниже поля

        # Вычисляем смещение для центрации камеры на игроке.
        offset_x = width // 2 - sprite.rect.width // 2 - game.board.cell_width * game.player.pos_x
        offset_y = height // 2 - sprite.rect.height // 2 - game.board.cell_height * (game.player.pos_y + 2)

        # Отрисовка доски с учетом смещения.
        game.board.render(screen, offset_x, offset_y)

        # Обновляем позицию спрайта игрока с учетом смещения.
        sprite.rect.topleft = (game.board.cell_width * game.player.pos_x,
                               game.board.cell_height * (game.player.pos_y))

        # Отрисовка спрайтов с учетом смещения.

        for s in game.all_sprites:
            s.rect.x += offset_x
            s.rect.y += offset_y

        game.all_sprites.draw(screen)

        pygame.display.flip()

pygame.quit()