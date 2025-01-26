import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы игры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
DISPLAY_DURATION = 2000  # Время отображения изображения в миллисекундах (например, 2000 мс = 2 секунды)


# Загрузка изображения
def load_image(filename):
    return pygame.image.load(filename)


# Основной класс игры
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Скрытие изображения через время")
        self.clock = pygame.time.Clock()

        self.image = load_image('treasure_1.png')  # Замените 'your_image.png' на путь к вашему изображению
        self.x = SCREEN_WIDTH // 2 - self.image.get_width() // 2
        self.y = SCREEN_HEIGHT // 2 - self.image.get_height() // 2
        self.visible = True  # Переменная для отслеживания видимости изображения
        self.start_time = pygame.time.get_ticks()  # Время, когда изображение было показано

    def update(self):
        current_time = pygame.time.get_ticks()  # Получаем текущее время в миллисекундах
        if self.visible and (current_time - self.start_time >= DISPLAY_DURATION):
            self.visible = False  # Убираем изображение после заданного времени

    def draw(self):
        self.screen.fill((0, 0, 0))  # Очистка экрана

        if self.visible:  # Если изображение видно, отрисовываем его
            self.screen.blit(self.image, (self.x, self.y))

        pygame.display.flip()  # Обновление экрана

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Проверка на закрытие окна
                    pygame.quit()
                    sys.exit()

            self.update()  # Обновление состояния игры
            self.draw()  # Отрисовка объектов
            self.clock.tick(FPS)  # Ограничение FPS


# Запуск игры
if __name__ == '__main__':
    game = Game()
    game.run()
