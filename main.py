import pygame
import os
import random
import time
from game import Game
from player import Player
from board import Board

# Список цитат
quotes = [
    ("Единственное ограничение для нашего будущего – это сомнения в настоящем.", "Рузвельт, Ф. Д."),
    ("Посреди каждой трудности кроется возможность.", "Эйнштейн, А."),
    ("Жизнь – это то, что происходит, пока вы заняты другими планами.", "Леннон, Дж."),
    # Добавь больше цитат по необходимости
]

def load_images():
    images = []
    for filename in os.listdir('boot_images'):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image_path = os.path.join('boot_images', filename)
            image = pygame.image.load(image_path)
            images.append(image)
            print(f"Загружено: {filename}")  # Отладочный вывод
    if not images:
        print("Не найдено изображений.")
    return images

def scale_image(image, scale_factor):
    new_size = (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor))
    return pygame.transform.scale(image, new_size)


def display_loading_screen(screen, images, quotes):
    screen.fill((0, 0, 0))  # Залить экран черным, чтобы понять, какой цвет отображается
    pygame.display.flip()
    pygame.time.delay(1000)  # Задержка на 1 секунду для проверки



#                                                 !!!ACHTUNG!!!
#                                             !!!НЕРАБОЧАЯ ХУЙНЯ!!!
#                                            !!!ПРОСЬБА ПОФИКСИТЬ!!!



# def display_loading_screen(screen, images, quotes):
#     font = pygame.font.Font(None, 36)
#     loading_duration = 5  # Установим на 5 секунд для проверки
#     start_time = time.time()
#
#     while time.time() - start_time < loading_duration:
#         screen.fill((2, 137, 255))
#
#         # Случайно выбираем изображение и масштабируем его
#         image = random.choice(images)
#         scaled_image = scale_image(image, 1)
#         screen.blit(scaled_image, (0, 0))
#
#         # Случайно выбираем цитату
#         quote = random.choice(quotes)
#         text_surface = font.render(quote[0], True, (255, 255, 255))
#         author_surface = font.render(quote[1], True, (255, 255, 255))
#
#         # Позиционирование текста
#         text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))
#         author_rect = author_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() - 60))
#
#         # Регулировка текста по ограничению
#         while text_rect.width > 300 and len(quote[0]) > 1:
#             quote_text = quote[0][:-1]
#             text_surface = font.render(quote_text, True, (255, 255, 255))
#             text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))
#
#         screen.blit(text_surface, text_rect)
#         screen.blit(author_surface, author_rect)
#
#         # Рисуем светло-серый троббер (круг)
#         trober_radius = 20
#         trober_center = (screen.get_width() - 100, screen.get_height() - 100)
#         pygame.draw.circle(screen, (211, 211, 211), trober_center, trober_radius)
#
#         pygame.display.flip()
#         pygame.time.delay(15000)

def main():
    pygame.init()
    size = width, height = 935, 660
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')

    images = load_images()
    display_loading_screen(screen, images, quotes)

    fullscreen = False
    game = Game()

    sprite = pygame.sprite.Sprite()
    sprite.rect = pygame.Rect(game.board.cell_width * game.player.pos_x,
                              game.board.cell_height * (game.player.pos_y + 1),
                              game.board.cell_width,
                              game.board.cell_height)

    move_direction = None
    draw = False
    treasure_pos_y = None
    treasure_pos_x = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:  # Переключение в полноэкранный режим
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
                    else:
                        screen = pygame.display.set_mode((width, height))
                elif event.key == pygame.K_ESCAPE and fullscreen:  # Выход из полноэкранного режима
                    fullscreen = False
                    screen = pygame.display.set_mode((width, height))

                elif event.key == pygame.K_LEFT:
                    move_direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    move_direction = 'right'
                elif event.key == pygame.K_DOWN:
                    move_direction = 'bottom'
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN):
                    move_direction = None

        if game.animation_treasure:
            treasure_pos_x, treasure_pos_y = sprite.rect.x, sprite.rect.y
            draw = True
            game.animation_treasure = False

        if treasure_pos_y == 0:
            draw = False
        if draw:
            treasure_pos_y -= 1

        game.update_camera()

        if move_direction:
            if move_direction == 'left':
                game.player.move('left')
            elif move_direction == 'right':
                game.player.move('right')
            elif move_direction == 'bottom':
                game.player.move('bottom')

        screen.fill((2, 137, 255))

        offset_x = width // 2 - sprite.rect.width // 2 - game.board.cell_width * game.player.pos_x
        offset_y = height // 2 - sprite.rect.height // 2 - game.board.cell_height * (game.player.pos_y + 2)

        game.board.render(screen, offset_x, offset_y)

        sprite.rect.topleft = (game.board.cell_width * game.player.pos_x,
                               game.board.cell_height * (game.player.pos_y) + 7)

        for s in [sprite]:
            s.rect.x += offset_x
            s.rect.y += offset_y

        screen.blit(game.player.image, sprite.rect)
        game.player.update()
        game.update()

        if draw:
            screen.blit(game.treasure_image, (treasure_pos_x, treasure_pos_y))

        game.draw_money_counter()
        game.draw_health()
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
