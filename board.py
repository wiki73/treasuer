import pygame
from utils import load_image
class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.cell_states = [[0] * width for _ in range(height)]  # Отслеживание состояния клеток
        self.cell_items = [[None] * width for _ in range(height)]  # Отслеживание предметов в клетках
        self.cell_enemies = [[None] * width for _ in range(height)]  # Для отслеживания врагов
        self.left = 0
        self.top = 0
        self.cell_width = 45
        self.cell_height = 45
        self.default_cell_image = pygame.transform.scale(load_image('einschlief.png'), (self.cell_width, self.cell_height))
        self.activated_cell_image = pygame.transform.scale(load_image('aufgeräumt.png'), (self.cell_width, self.cell_height))
        self.blocked_cell_image = pygame.transform.scale(load_image('extra-depth.png'), (self.cell_width, self.cell_height))
        # Делаем дом в 7 раз шире и в 5 раз выше обычной клетки
        house_width = self.cell_width * 7
        house_height = self.cell_height * 5
        self.house = pygame.transform.scale(load_image('дом_2.png'), (house_width, house_height))
        self.enemy_images = [
            pygame.transform.scale(load_image('enemy/L01.png'), (self.cell_width, self.cell_height)),
            pygame.transform.scale(load_image('enemy/L02.png'), (self.cell_width, self.cell_height))
        ]
        self.enemy_frame = 0
        self.enemy_animation_counter = 0
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
    def activate_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cell_states[y][x] = 1
    def place_item(self, x, y, item_type):
        self.cell_items[y][x] = item_type
    def remove_item(self, x, y):
        item = self.cell_items[y][x]
        self.cell_items[y][x] = None
        return item
    def place_enemy(self, x, y):
        self.cell_enemies[y][x] = True
    def remove_enemy(self, x, y):
        self.cell_enemies[y][x] = None
    def render(self, screen, offset_x, offset_y):
        for i in range(self.height):
            for j in range(self.width):
                if j == 0 or j == self.width - 1 or i == self.height - 1 or (i == 0 and (j == 0 or j == self.width - 1)):
                    screen.blit(self.blocked_cell_image, (offset_x + j * self.cell_width, offset_y + i * self.cell_height))
                elif i == 0:
                    continue
                elif self.cell_states[i][j] == 1:
                    screen.blit(self.activated_cell_image, (offset_x + j * self.cell_width, offset_y + i * self.cell_height))
                else:
                    screen.blit(self.default_cell_image, (offset_x + j * self.cell_width, offset_y + i * self.cell_height))
        
        # Отрисовываем дом по центру сверху
        house_x = offset_x + (self.width * self.cell_width - self.house.get_width()) // 2
        house_y = offset_y - self.house.get_height() + self.cell_height
        screen.blit(self.house, (house_x, house_y))
        
        # Отрисовка предметов
        for i in range(self.height):
            for j in range(self.width):
                if self.cell_items[i][j] == 1:  # Камень
                    screen.blit(pygame.transform.scale(load_image('treasure_1.png'), (self.cell_width, self.cell_height)),
                              (offset_x + j * self.cell_width, offset_y + i * self.cell_height))
                elif self.cell_items[i][j] == 2:  # Сундук
                    screen.blit(pygame.transform.scale(load_image('treasure_2.png'), (self.cell_width, self.cell_height)),
                              (offset_x + j * self.cell_width, offset_y + i * self.cell_height))
        # Анимация врагов
        self.enemy_animation_counter += 1
        if self.enemy_animation_counter >= 15:  # Скорость анимации
            self.enemy_animation_counter = 0
            self.enemy_frame = (self.enemy_frame + 1) % 2
        # Отрисовка врагов
        for i in range(self.height):
            for j in range(self.width):
                if self.cell_enemies[i][j]:
                    screen.blit(self.enemy_images[self.enemy_frame],
                              (offset_x + j * self.cell_width, offset_y + i * self.cell_height))