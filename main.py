import pygame
from game import Game
from player import Player
from board import Board
from utils import load_image

def show_title_screen(screen, size):
    # Загружаем и масштабируем фоновое изображение
    background = pygame.transform.scale(load_image('title.jpg'), size)
    
    # Создаем кнопку
    button_width = 200
    button_height = 50
    button_x = size[0] // 2 - button_width // 2
    button_y = size[1] // 2 + 200
    
    button_color = (50, 200, 50)
    button_hover_color = (70, 220, 70)
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    # Создаем текст кнопки
    font = pygame.font.Font(None, 36)
    text = font.render("Начать игру", True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True
                    
        # Отрисовка
        screen.blit(background, (0, 0))
        
        # Проверка наведения на кнопку
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, button_rect)
        else:
            pygame.draw.rect(screen, button_color, button_rect)
            
        pygame.draw.rect(screen, (30, 30, 30), button_rect, 2)  # Обводка кнопки
        screen.blit(text, text_rect)
        
        pygame.display.flip()
    
    return False

def show_game_over_screen(screen, size):
    # Создаем полупрозрачный черный фон
    overlay = pygame.Surface(size)
    overlay.fill((0, 0, 0))
    overlay.set_alpha(180)
    
    # Создаем кнопку
    button_width = 200
    button_height = 50
    button_x = size[0] // 2 - button_width // 2
    button_y = size[1] // 2 + 50
    
    button_color = (50, 200, 50)
    button_hover_color = (70, 220, 70)
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    # Создаем тексты
    font_big = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 36)
    
    game_over_text = font_big.render("Вы проиграли!", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(size[0] // 2, size[1] // 2 - 50))
    
    button_text = font.render("Начать заново", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=button_rect.center)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return True
                    
        # Отрисовка
        screen.blit(overlay, (0, 0))
        screen.blit(game_over_text, game_over_rect)
        
        # Проверка наведения на кнопку
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, button_hover_color, button_rect)
        else:
            pygame.draw.rect(screen, button_color, button_rect)
            
        pygame.draw.rect(screen, (30, 30, 30), button_rect, 2)
        screen.blit(button_text, button_text_rect)
        
        pygame.display.flip()
    
    return False

def main():
    pygame.init()
    size = width, height = 935, 660
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    
    # Показываем начальный экран
    if not show_title_screen(screen, size):
        pygame.quit()
        return
        
    while True:  # Основной цикл для перезапуска игры
        running = True
        treasure_pos_y = None
        treasure_pos_x = None
        draw = False
        move_direction = None

        game = Game()
        sprite = pygame.sprite.Sprite()
        sprite.rect = pygame.Rect(game.board.cell_width * game.player.pos_x,
                                game.board.cell_height * (game.player.pos_y + 1),
                                game.board.cell_width,
                                game.board.cell_height)

        # Добавляем обработку исключений при загрузке игры
        try:
            while running:
                if game.animation_treasure:
                    treasure_pos_x, treasure_pos_y = sprite.rect.x, sprite.rect.y
                    draw = True
                    game.animation_treasure = False
                    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            move_direction = 'left'
                        elif event.key == pygame.K_RIGHT:
                            move_direction = 'right'
                        elif event.key == pygame.K_DOWN:
                            move_direction = 'bottom'
                    if event.type == pygame.KEYUP:
                        move_direction = None
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
                                     game.board.cell_height * (game.player.pos_y) +7)

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

                # Проверка на проигрыш
                if game.current_health <= 0:
                    if show_game_over_screen(screen, size):
                        break  # Начать игру заново
                    else:
                        pygame.quit()
                        return

                pygame.display.flip()
                
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            pygame.quit()
            return

if __name__ == '__main__':
    main()