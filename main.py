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
        print(self.board)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                if elem == 1:
                    rect = (
                        self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(screen, (0, 0, 0), rect)
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
                    pygame.draw.line(screen, (0, 0, 255),
                                     (self.left + j * self.cell_size + self.cell_size - 4,
                                      self.top + i * self.cell_size + 4),
                                     (self.left + j * self.cell_size + 4,
                                      self.top + i * self.cell_size + self.cell_size - 4),
                                     width=2)
                    pygame.draw.line(screen, (0, 0, 255),
                                     (self.left + j * self.cell_size + 4,
                                      self.top + i * self.cell_size + 4),
                                     (self.left + j * self.cell_size + self.cell_size - 4,
                                      self.top + i * self.cell_size + self.cell_size - 4),
                                     width=2)
                else:
                    pygame.draw.rect(screen, (60, 210, 92),
                                     (self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size,
                                      self.cell_size), 1)

    # def set_cell(self, cell_x, cell_y):
    #     self.board[cell_y][cell_x] = 1


class Player:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def move(self, direction):
        if direction == 'right':
            self.pos_x += 1
            return True
        if direction == 'left' and self.pos_x > 0:
            self.pos_x -= 1
            return True
        if direction == 'top' and self.pos_y > 0:
            self.pos_y -= 1
            return True
        if direction == 'bottom':
            self.pos_y += 1
            return True


class Game:
    def __init__(self):
        self.board = Board(17, 12)
        self.board.set_view(0, 165, 55)
        self.player = Player(2, 0)
        # self.board.set_cell(self.player.pos_x, self.player.pos_y)

        self.all_sprites = pygame.sprite.Group()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('', name)
        # если файл не существует, то выходим
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
        self.board.set_cell(self.player.pos_x, self.player.pos_y)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 935, 660
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    running = True
    game = Game()
    sprite = pygame.sprite.Sprite()
    sprite.image = game.load_image('player.png', -1)
    sprite.rect = sprite.image.get_rect(topleft=(game.board.cell_size * game.player.pos_x,
                                                 game.board.cell_size * (game.player.pos_y + 3)))
    game.all_sprites.add(sprite)
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if sprite.rect.left != 0:
                        game.player.move('left')
                        sprite.rect.left -= game.board.cell_size
                    print(game.player.pos_x, game.player.pos_y)
                elif event.key == pygame.K_RIGHT:
                    if sprite.rect.left != 880:
                        game.player.move('right')
                        sprite.rect.left += game.board.cell_size
                    print(game.player.pos_x, game.player.pos_y)
                elif event.key == pygame.K_UP:
                    if sprite.rect.top != 0:
                        game.player.move('top')
                        sprite.rect.top -= game.board.cell_size
                    print(game.player.pos_x, game.player.pos_y)
                elif event.key == pygame.K_DOWN:

                    if sprite.rect.top != 605:
                        game.player.move('bottom')
                        sprite.rect.top += game.board.cell_size

                    print(game.player.pos_x, game.player.pos_y)
        screen.fill((0, 0, 0))

        game.board.render(screen)
        game.all_sprites.draw(screen)
        pygame.display.flip()
