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
        self.cell_width, self.cell_height))  # Новое изображение для активированных клеток

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
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                if self.cell_states[i][j] == 1:
                    # Отрисовка изображения активированной клетки
                    screen.blit(self.activated_cell_image, (offset_x + j * self.cell_width,
                                                            offset_y + i * self.cell_height))
                else:
                    # Отрисовка изображения обычной клетки
                    screen.blit(self.default_cell_image, (offset_x + j * self.cell_width,
                                                          offset_y + i * self.cell_height))


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
        elif direction == 'left':
            if self.pos_x > 0:
                self.pos_x -= 1
                return True
        elif direction == 'bottom':
            if self.pos_y < len(self.board.board) - 1:
                self.pos_y += 1
                return True

    def enter_cell(self):
        # Активировать клетку при входе в нее
        self.board.activate_cell(self.pos_x, self.pos_y)


class Game:
    def __init__(self):
        pygame.init()
        size = width, height = 935, 660
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Инициализация игры')

        i_width = 51
        i_height = 50

        self.board = Board(i_width, i_height)
        self.board.set_view(0, 165, 55)

        initial_pos_x = (self.board.width // 2) - 1
        initial_pos_y = -1

        self.player = Player(initial_pos_x, initial_pos_y, self.board)

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

        screen.blit(sprite.image, sprite.rect)

        pygame.display.flip()

pygame.quit()