import pygame
from utils import load_image
import random


class Player:
    def __init__(self, pos_x, pos_y, board, game):
        self.index = 0
        self.frame_count = 0
        self.frame_delay = 15

        self.list_image_r = [
            pygame.transform.scale(load_image('image_player/r_normal_1.png'), (60, 43)),
            pygame.transform.scale(load_image('image_player/r_drag_1.png'), (60, 43)),
            pygame.transform.scale(load_image('image_player/r_drag_2.png'), (60, 43))
        ]
        self.list_image_l = [
            pygame.transform.scale(load_image('image_player/l_normal_1.png'), (60, 43)),
            pygame.transform.scale(load_image('image_player/l_drag_2.png'), (60, 43)),
            pygame.transform.scale(load_image('image_player/l_drag_3.png'), (60, 43))
        ]
        self.list_image_b = [
            pygame.transform.scale(load_image('image_player/l_normal_1.png'), (60, 43)),
            pygame.transform.scale(load_image('image_player/l_drag_2.png'), (60, 43)),
            pygame.transform.scale(load_image('image_player/l_drag_3.png'), (60, 43)),
            pygame.transform.scale(load_image('image_player/result_fall01.png'), (60, 43))
        ]
        self.image = self.list_image_r[self.index]
        self.pos_x = pos_x
        self.pos_y = pos_y + 1
        self.board = board
        self.game = game
        self.dirr = ''
        self.animation_running = False
        self.target_x = pos_x
        self.target_y = pos_y
        self.is_moving = False

    def check_surrounding_enemies(self, x, y):
        # Проверяем все соседние клетки на наличие врагов
        neighbors = [
            (x-1, y),  # слева
            (x+1, y),  # справа
            (x, y+1),  # снизу
            (x-1, y+1),  # слева снизу
            (x+1, y+1)  # справа снизу
        ]
        
        enemy_count = 0
        for nx, ny in neighbors:
            if (0 <= nx < len(self.board.board[0]) and 
                0 <= ny < len(self.board.board) and 
                self.board.cell_states[ny][nx] and 
                self.board.cell_enemies[ny][nx]):
                enemy_count += 1
        
        return enemy_count

    def move(self, direction):
        new_x, new_y = self.pos_x, self.pos_y

        if direction == 'right':
            new_x += 1
            self.dirr = 'right'
            self.index = 0
            self.image = self.list_image_r[self.index]
        elif direction == 'left':
            new_x -= 1
            self.dirr = 'left'
            self.index = 0
            self.image = self.list_image_l[self.index]
        elif direction == 'bottom':
            new_y += 1
            self.dirr = 'bottom'

        if new_x >= 0 and new_x < len(self.board.board[0]) and new_y >= 0 and new_y < len(self.board.board):
            if not (new_x == 0 or new_x == len(self.board.board[0]) - 1 or new_y == len(self.board.board) - 1 or (
                    new_y == 0 and (new_x == 0 or new_x == len(self.board.board[0]) - 1))):

                # Не активируем клетки верхнего ряда, но продолжаем движение
                if new_y != 0:
                    # Если блок не активирован
                    if not self.board.cell_states[new_y][new_x]:
                        self.board.activate_cell(new_x, new_y)

                chance = random.random()
                enemy_chance = random.random()

                # Проверка количества врагов вокруг
                surrounding_enemies = self.check_surrounding_enemies(self.pos_x, self.pos_y)

                # Размещаем врага только если рядом с игроком не больше одного врага
                if enemy_chance < 0.30 and surrounding_enemies < 2:
                    self.board.place_enemy(new_x, new_y)

                # Логика размещения предметов
                if new_y <= 4:
                    if chance < 0.20:
                        if random.random() < 0.8:
                            self.board.place_item(new_x, new_y, 1)
                        else:
                            self.board.place_item(new_x, new_y, 2)
                elif 5 <= new_y <= 10:
                    if chance < 0.25:
                        if random.random() < 0.85:
                            self.board.place_item(new_x, new_y, 1)
                        else:
                            self.board.place_item(new_x, new_y, 2)
                elif 11 <= new_y <= 30:
                    if chance < 0.35:
                        if random.random() < 0.9:
                            self.board.place_item(new_x, new_y, 1)
                        else:
                            self.board.place_item(new_x, new_y, 2)
                elif 31 <= new_y:
                    if chance < 0.45:
                        if random.random() < 0.95:
                            self.board.place_item(new_x, new_y, 1)
                        else:
                            self.board.place_item(new_x, new_y, 2)

            # Если блок активирован и на нём враг, наносим урон
            if self.board.cell_enemies[new_y][new_x]:
                self.game.take_damage()  # Вызываем метод урона
                self.game.decrease_health(1)  # Уменьшение здоровья на 1
                self.board.remove_enemy_with_timeout(new_x, new_y, 0.3)  # Удаляем врага через 0.3 секунды

            # Обновляемся после взаимодействия
            self.pos_x = new_x
            self.target_x = new_x
            self.target_y = new_y
            self.last_move_time = time.time()  # Обновляем время последнего движения
            return True

        return False

    def update(self):
        if self.animation_running:
            self.frame_count += 1
            if self.frame_count >= self.frame_delay:
                self.frame_count = 0
                self.index += 1
                
                if self.dirr == 'right' and self.index < len(self.list_image_r):
                    self.image = self.list_image_r[self.index]
                elif self.dirr == 'left' and self.index < len(self.list_image_l):
                    self.image = self.list_image_l[self.index]
                elif self.dirr == 'bottom' and self.index < len(self.list_image_b):
                    self.image = self.list_image_b[self.index]
                else:
                    self.animation_running = False
                    self.index = 0
                    if self.is_moving:
                        self.pos_x = self.target_x
                        self.pos_y = self.target_y
                        self.is_moving = False
                    self.image = self.list_image_r[self.index] if self.dirr == 'right' else self.list_image_l[self.index]

    def enter_cell(self):
        if self.pos_y > 0:
            self.board.activate_cell(self.pos_x, self.pos_y)
