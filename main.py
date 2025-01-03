import os
import sys
import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.cell_states = [[0] * width for _ in range(height)]  # Отслеживание состояния клеток
        self.left = 0
        self.top = 0
        self.cell_width = 68
        self.cell_height = 52
        self.default_cell_image = pygame.transform.scale(self.load_image('einschlief.png'),
                                                         (self.cell_width, self.cell_height))
        self.activated_cell_image = pygame.transform.scale(self.load_image('aufgeräumt.png'), (
            self.cell_width, self.cell_height))  # Изображение для активированных клеток
        # Изменено имя файла на extra-depth.png
        self.blocked_cell_image = pygame.transform.scale(self.load_image('extra-depth.png'), (
            self.cell_width, self.cell_height))  # Изображение для недоступных клеток

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

    def activate_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cell_states[y][x] = 1  # Помечаем эту клетку как активированную

    def render(self, screen, offset_x, offset_y):
        for i in range(self.height):
            for j in range(self.width):
                # Отрисовка недоступных клеток по бокам и внизу
                if j == 0 or j == self.width - 1 or i == self.height - 1:
                    # Левый и правый край и нижний ряд
                    screen.blit(self.blocked_cell_image, (offset_x + j * self.cell_width,
                                                          offset_y + i * self.cell_height))
                elif i == 0 and (j == 0 or j == self.width - 1):
                    # Крайние клетки верхнего ряда как непроходимые
                    screen.blit(self.blocked_cell_image, (offset_x + j * self.cell_width,
                                                          offset_y + i * self.cell_height))
                elif i == 0:
                    # Пустые клетки верхнего ряда без спрайтов
                    continue
                elif self.cell_states[i][j] == 1:
                    # Отрисовка изображения активированной клетки
                    screen.blit(self.activated_cell_image, (offset_x + j * self.cell_width,
                                                            offset_y + i * self.cell_height))
                else:
                    # Отрисовка изображения обычной клетки
                    screen.blit(self.default_cell_image, (offset_x + j * self.cell_width,
                                                          offset_y + i * self.cell_height))


class Player:
    def __init__(self, pos_x, pos_y, board):
        self.index = 0
        self.frame_count = 0  # Счетчик кадров для анимации
        self.frame_delay = 15  # Увеличиваем количество кадров, необходимых для смены изображения

        # Списки изображений для анимации
        self.list_image_r = [pygame.transform.scale(board.load_image('image_player/r_normal_1.png'), (53, 43)),
                             pygame.transform.scale(board.load_image('image_player/r_drag_1.png'), (53, 43)),
                             pygame.transform.scale(board.load_image('image_player/r_drag_2.png'), (53, 43))]
        self.list_image_l = [pygame.transform.scale(board.load_image('image_player/l_normal_1.png'), (53, 43)),
                             pygame.transform.scale(board.load_image('image_player/l_drag_2.png'), (53, 43)),
                             pygame.transform.scale(board.load_image('image_player/l_drag_3.png'), (53, 43))]

        self.image = self.list_image_r[self.index]  # Первоначальное изображение
        self.pos_x = pos_x
        self.pos_y = pos_y + 1
        self.board = board
        self.dirr = ''
        self.animation_running = False  # Анимация не запущена по умолчанию

    def move(self, direction):
        new_x, new_y = self.pos_x, self.pos_y
        if direction == 'right':
            new_x += 1
            self.dirr = 'right'
            self.animation_running = True  # Запускаем анимацию при движении вправо
            self.index = 0  # Сбрасываем индекс анимации вправо
            self.image = self.list_image_r[self.index]  # Устанавливаем первое изображение для движения вправо
        elif direction == 'left':
            new_x -= 1
            self.dirr = 'left'
            self.animation_running = True  # Запускаем анимацию при движении влево
            self.index = 0  # Сбрасываем индекс анимации влево
            self.image = self.list_image_l[self.index]  # Устанавливаем первое изображение для движения влево
        elif direction == 'bottom':
            new_y += 1
            self.dirr = 'bottom'
            self.animation_running = False  # Остановка анимации при движении вниз

        # Проверка на доступность новой позиции
        if new_x >= 0 and new_x < len(self.board.board[0]) and new_y >= 0 and new_y < len(self.board.board):
            # Проверяем недоступные клетки (боковые и нижний ряд)
            if not (new_x == 0 or new_x == len(self.board.board[0]) - 1 or new_y == len(self.board.board) - 1 or (
                    new_y == 0 and (new_x == 0 or new_x == len(self.board.board[0]) - 1))):
                self.pos_x = new_x
                self.pos_y = new_y
                return True

    def update(self):
        if self.animation_running:  # Проверяем, идет ли анимация
            # Увеличиваем счетчик кадров
            self.frame_count += 1

            # Меняем изображение, если счетчик кадров достиг предела
            if self.frame_count >= self.frame_delay:
                self.frame_count = 0  # Сбрасываем счетчик
                self.index += 1

                # Проверяем, какой список используется и обновляем изображение
                if self.dirr == 'right' and self.index < len(self.list_image_r):

                    self.image = self.list_image_r[self.index]  # Обновляем текущее изображение для движения вправо
                elif self.dirr == 'left' and self.index < len(self.list_image_l):
                    self.image = self.list_image_l[self.index]  # Обновляем текущее изображение для движения влево
                else:
                    self.animation_running = False  # Останавливаем анимацию, если все кадры были показаны
                    self.index = 0  # Сбрасываем индекс на первую картинку
                    # Возвращаем к первому изображению в зависимости от направления
                    self.image = self.list_image_r[self.index] if self.dirr == 'right' else self.list_image_l[
                        self.index]

    def enter_cell(self):
        # Активировать клетку при входе в нее только если это не верхний ряд без спрайтов.
        if self.pos_y > 0:
            self.board.activate_cell(self.pos_x, self.pos_y)


class Game:
    def __init__(self):
        pygame.init()
        size = width, height = 935, 660
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Инициализация игры')

        i_width = 53  # Увеличиваем ширину на две клетки
        i_height = 51  # Увеличиваем высоту на одну клетку

        self.board = Board(i_width, i_height)
        self.board.set_view(0, 165, 55)

        initial_pos_x = (self.board.width // 2) - 1
        initial_pos_y = -1

        self.player = Player(initial_pos_x, initial_pos_y, self.board)
        # Состояние блокировки камеры
        self.camera_locked = {'left': False, 'right': False, 'down': False}

    def update_camera(self):
        # Проверяем положение игрока относительно границ
        if self.player.pos_x <= 7:  # Если игрок на первом до восьмого ряду слева
            self.camera_locked['left'] = True
        elif self.player.pos_x > 7:  # Если игрок покинул область
            self.camera_locked['left'] = False

        if self.player.pos_x >= self.board.width - 8:  # Если игрок на восьмом ряду справа
            self.camera_locked['right'] = True
        elif self.player.pos_x < self.board.width - 8:  # Если игрок покинул область
            self.camera_locked['right'] = False

        if self.player.pos_y >= 8:  # Если игрок на девятом ряду снизу
            self.camera_locked['down'] = True
        elif self.player.pos_y < 8:  # Если игрок покинул область
            self.camera_locked['down'] = False

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


if __name__ == '__main__':
    size = width, height = 935, 660
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    running = True

    game = Game()

    sprite = pygame.sprite.Sprite()
    sprite.image = game.load_image('player.png')
    sprite.rect = sprite.image.get_rect(topleft=(game.board.cell_width * game.player.pos_x,
                                                 game.board.cell_height * (game.player.pos_y + 2)))

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

        # Обновляем состояние камеры
        game.update_camera()

        if move_direction and current_time - last_move_time >= move_interval:
            previous_pos_x, previous_pos_y = game.player.pos_x, game.player.pos_y

            if move_direction == 'left':
                game.player.move('left')
            elif move_direction == 'right':
                game.player.move('right')
            elif move_direction == 'bottom':
                game.player.move('bottom')

            # Проверяем, вошел ли игрок в новую клетку и активируем ее.
            if (previous_pos_x != game.player.pos_x) or (previous_pos_y != game.player.pos_y):
                game.player.enter_cell()

            last_move_time = current_time

        screen.fill((2, 137, 255))

        offset_x = width // 2 - sprite.rect.width // 2 - game.board.cell_width * game.player.pos_x
        offset_y = height // 2 - sprite.rect.height // 2 - game.board.cell_height * (game.player.pos_y + 2)

        game.board.render(screen, offset_x, offset_y)

        sprite.rect.topleft = (game.board.cell_width * game.player.pos_x,
                               game.board.cell_height * (game.player.pos_y))

        for s in [sprite]:
            s.rect.x += offset_x
            s.rect.y += offset_y

        screen.blit(game.player.image, sprite.rect)
        game.player.update()
        pygame.display.flip()

pygame.quit()