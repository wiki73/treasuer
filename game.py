import os
import sys
import pygame
from board import Board
from player import Player
from utils import load_image, create_heart_surface
import random
class Game:
    def __init__(self):
        pygame.init()
        self.size = 935, 660
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Инициализация игры')
        i_width = 53
        i_height = 51
        self.board = Board(i_width, i_height)
        self.board.set_view(0, 165, 55)
        initial_pos_x = (self.board.width // 2) - 1
        initial_pos_y = -1
        self.player = Player(initial_pos_x, initial_pos_y, self.board, self)
        self.camera_locked = {'left': False, 'right': False, 'down': False}
        self.money = 0
        self.animation_treasure = False
        self.show_time = 0
        self.treasure_shown = False
        self.treasure_image = None
        self.treasure_y = 0
        self.treasure_speed = 2
        self.treasure_visible = False
        self.num_treasure = None
        self.max_health = 5
        self.current_health = 5
        self.heart_image = create_heart_surface()
        self.empty_heart_image = create_heart_surface(empty=True)
        self.player.has_moved = False
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
    def plus_summ(self, chance_fro_pos):
        print(chance_fro_pos)
        chance = random.random()
        if chance < chance_fro_pos:
            print("сундук")
            self.animation_treasure = True
            self.num_treasure = 2
            self.money += 800
        else:
            chance_2 = random.random()
            if chance_2 < chance_fro_pos + 0.15:
                print('каменная хрень')
                self.animation_treasure = True
                self.num_treasure = 1
                self.money += 500
            else:
                print('ниче')
    def update_camera(self):
        if self.player.pos_x <= 7:
            self.camera_locked['left'] = True
        elif self.player.pos_x > 7:
            self.camera_locked['left'] = False
        if self.player.pos_x >= self.board.width - 8:
            self.camera_locked['right'] = True
        elif self.player.pos_x < self.board.width - 8:
            self.camera_locked['right'] = False
        if self.player.pos_y >= 8:
            self.camera_locked['down'] = True
        elif self.player.pos_y < 8:
            self.camera_locked['down'] = False
    def update(self):
        if self.animation_treasure:
            print(self.num_treasure)
            if self.num_treasure is not None and self.num_treasure == 1:
                self.treasure_image = pygame.transform.scale(load_image('treasure_1.png'), (53, 43))
            elif self.num_treasure is not None and self.num_treasure == 2:
                print(1)
                self.treasure_image = pygame.transform.scale(load_image('treasure_2.png'), (53, 43))
    def draw_money_counter(self):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f'Деньги: {self.money}', True, (30, 255, 30))
        self.screen.blit(text_surface, (10, 10))
    def draw_health(self):
        for i in range(self.max_health):
            if i < self.current_health:
                self.screen.blit(self.heart_image, 
                               (self.size[0] - (i + 1) * 40 - 10, 10))
            else:
                self.screen.blit(self.empty_heart_image, 
                               (self.size[0] - (i + 1) * 40 - 10, 10))
    def take_damage(self):
        if self.current_health > 0:
            self.current_health -= 1
            return True
        return False
        
    def add_health(self):
        if self.current_health < self.max_health:
            self.current_health += 1
            return True
        return False