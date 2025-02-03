import pygame
from game import Game
from player import Player
from board import Board
from utils import load_image
from database import Database
import time

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

def show_game_over_screen(screen, size, score, time_played):
    # Затемнение фона
    overlay = pygame.Surface(size)
    overlay.fill((0, 0, 0))
    overlay.set_alpha(200)
    screen.blit(overlay, (0, 0))
    
    # Цвета
    brown = (139, 69, 19)
    light_brown = (160, 82, 45)
    gold = (218, 165, 32)
    red = (178, 34, 34)
    
    # Создаем панель для контента
    panel_width = 350
    panel_height = 280
    panel_rect = pygame.Rect(
        (size[0] - panel_width) // 2,
        (size[1] - panel_height) // 2,
        panel_width,
        panel_height
    )
    
    # Тень панели
    shadow_rect = panel_rect.copy()
    shadow_rect.x += 5
    shadow_rect.y += 5
    pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=15)
    
    # Основная панель
    pygame.draw.rect(screen, brown, panel_rect, border_radius=15)
    
    # Добавляем текстурные детали на панель
    for i in range(panel_height // 40):  # Горизонтальные полосы
        y = panel_rect.top + i * 40 + 20
        if y < panel_rect.bottom - 20:  # Не рисуем близко к краям
            pygame.draw.line(screen, light_brown,
                           (panel_rect.left + 20, y),
                           (panel_rect.right - 20, y), 1)
    
    # Добавляем декоративные уголки
    corner_size = 20
    for x, y in [
        (panel_rect.left + 5, panel_rect.top + 5),
        (panel_rect.right - corner_size - 5, panel_rect.top + 5),
        (panel_rect.left + 5, panel_rect.bottom - corner_size - 5),
        (panel_rect.right - corner_size - 5, panel_rect.bottom - corner_size - 5)
    ]:
        pygame.draw.line(screen, gold, (x, y), (x + corner_size, y), 2)
        pygame.draw.line(screen, gold, (x, y), (x, y + corner_size), 2)
    
    # Рамка панели
    pygame.draw.rect(screen, gold, panel_rect, 3, border_radius=15)
    
    # Кнопки
    button_width = 140
    button_height = 40
    restart_button = pygame.Rect(
        panel_rect.centerx - button_width - 10,
        panel_rect.bottom - 60,
        button_width,
        button_height
    )
    record_button = pygame.Rect(
        panel_rect.centerx + 10,
        panel_rect.bottom - 60,
        button_width,
        button_height
    )
    
    # Шрифты
    font_big = pygame.font.Font(None, 56)
    font = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 24)
    
    # Заголовок с декоративной подложкой
    header_bg = pygame.Rect(
        panel_rect.left + 20,
        panel_rect.top + 20,
        panel_width - 40,
        50
    )
    pygame.draw.rect(screen, light_brown, header_bg, border_radius=8)
    pygame.draw.rect(screen, gold, header_bg, 1, border_radius=8)
    
    game_over_text = font_big.render("Вы проиграли!", True, red)
    game_over_shadow = font_big.render("Вы проиграли!", True, (30, 30, 30))
    game_over_rect = game_over_text.get_rect(center=header_bg.center)
    
    screen.blit(game_over_shadow, (game_over_rect.x + 2, game_over_rect.y + 2))
    screen.blit(game_over_text, game_over_rect)
    
    # Разделительная линия с декоративными элементами
    line_y = header_bg.bottom + 15
    line_length = panel_width - 60
    center_x = panel_rect.centerx
    
    pygame.draw.line(screen, gold,
                    (center_x - line_length//2, line_y),
                    (center_x + line_length//2, line_y), 2)
    
    # Декоративные точки на линии
    for x in [center_x - line_length//2, center_x, center_x + line_length//2]:
        pygame.draw.circle(screen, gold, (x, line_y), 4)
    
    # Статистика (теперь без иконок)
    money_text = font.render(f"Money: {score:,}", True, (255, 215, 0))
    money_rect = money_text.get_rect(
        centerx=panel_rect.centerx,
        top=line_y + 25
    )
    screen.blit(money_text, money_rect)
    
    time_text = font.render(f"Time: {int(time_played)} sec", True, (255, 215, 0))
    time_rect = time_text.get_rect(
        centerx=panel_rect.centerx,
        top=money_rect.bottom + 10
    )
    screen.blit(time_text, time_rect)
    
    # Отрисовка кнопок с текстурой
    for button, text, font_obj in [
        (restart_button, "Начать заново", font_small),
        (record_button, "Записать рекорд", font_small)
    ]:
        # Тень кнопки
        shadow_btn = button.copy()
        shadow_btn.x += 2
        shadow_btn.y += 2
        pygame.draw.rect(screen, (30, 30, 30), shadow_btn, border_radius=8)
        
        # Основная кнопка
        if button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, light_brown, button, border_radius=8)
        else:
            pygame.draw.rect(screen, brown, button, border_radius=8)
        
        # Текстура кнопки
        for i in range(3):
            y = button.top + (i + 1) * button.height // 4
            pygame.draw.line(screen, light_brown,
                           (button.left + 5, y),
                           (button.right - 5, y), 1)
        
        # Рамка кнопки
        pygame.draw.rect(screen, gold, button, 2, border_radius=8)
        
        # Текст кнопки
        button_text = font_obj.render(text, True, (255, 215, 0))
        text_rect = button_text.get_rect(center=button.center)
        screen.blit(button_text, text_rect)
    
    # Обработка событий
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    return True, False
                if record_button.collidepoint(event.pos):
                    return True, True
        
        pygame.display.flip()
    
    return False, False

def draw_money_counter(screen, money):
    # Размеры и позиция (теперь в левом верхнем углу)
    counter_width = 200
    counter_height = 55
    counter_rect = pygame.Rect(15, 15, counter_width, counter_height)
    
    # Цвета
    brown = (139, 69, 19)  # основной коричневый
    light_brown = (160, 82, 45)  # светлый коричневый
    gold = (218, 165, 32)  # золотой
    
    # Тень
    shadow_rect = counter_rect.copy()
    shadow_rect.x += 3
    shadow_rect.y += 3
    pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=12)
    
    # Основной фон
    pygame.draw.rect(screen, brown, counter_rect, border_radius=12)
    
    # Рамка
    pygame.draw.rect(screen, gold, counter_rect, 3, border_radius=12)
    
    # Иконка монеты
    coin_font = pygame.font.Font(None, 40)
    coin_icon = coin_font.render("money:", True, (255, 215, 0))
    coin_rect = coin_icon.get_rect(left=counter_rect.left + 15, 
                                 centery=counter_rect.centery)
    screen.blit(coin_icon, coin_rect)
    
    # Сумма
    money_font = pygame.font.Font(None, 36)
    money_text = f"{money:,}"
    money_surface = money_font.render(money_text, True, (255, 215, 0))
    
    # Тень текста
    money_shadow = money_font.render(money_text, True, (30, 30, 30))
    money_rect = money_surface.get_rect(right=counter_rect.right - 15, 
                                      centery=counter_rect.centery)
    shadow_rect = money_rect.copy()
    shadow_rect.x += 1
    shadow_rect.y += 1
    
    screen.blit(money_shadow, shadow_rect)
    screen.blit(money_surface, money_rect)
    
    return counter_rect

def draw_records_button(screen, records_open, records=None):
    # Кнопка теперь располагается под счетчиком денег
    button_size = 55
    button_rect = pygame.Rect(15, 85, button_size, button_size)
    
    # Цвета
    brown = (139, 69, 19)
    light_brown = (160, 82, 45)
    gold = (218, 165, 32)
    dark_brown = (101, 67, 33)
    
    # Тень кнопки
    shadow_rect = button_rect.copy()
    shadow_rect.x += 3
    shadow_rect.y += 3
    pygame.draw.rect(screen, (30, 30, 30), shadow_rect, border_radius=12)
    
    # Основная кнопка
    if button_rect.collidepoint(pygame.mouse.get_pos()):
        main_color = light_brown
        # Эффект свечения при наведении
        glow_rect = button_rect.copy()
        glow_rect.inflate_ip(4, 4)
        pygame.draw.rect(screen, gold, glow_rect, border_radius=12, width=2)
    else:
        main_color = brown
    
    pygame.draw.rect(screen, main_color, button_rect, border_radius=12)
    pygame.draw.rect(screen, gold, button_rect, 3, border_radius=12)
    
    # Иконка кубка
    font = pygame.font.Font(None, 30)
    text = font.render("RES", True, (255, 215, 0))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    
    # Если панель открыта, показываем рекорды
    if records_open and records:
        panel_width = 300
        panel_height = min(400, len(records) * 40 + 70)
        panel_rect = pygame.Rect(15, 155, panel_width, panel_height)  # Изменена позиция Y
        
        # Тень панели
        shadow_panel = pygame.Surface((panel_width + 6, panel_height + 6))
        shadow_panel.fill((30, 30, 30))
        shadow_panel.set_alpha(100)
        screen.blit(shadow_panel, (panel_rect.x + 3, panel_rect.y + 3))
        
        # Фон панели с градиентом
        s = pygame.Surface((panel_width, panel_height))
        for i in range(panel_height):
            alpha = 255 - (i / panel_height * 30)  # Мягкий градиент сверху вниз
            current_color = (
                brown[0] + int((light_brown[0] - brown[0]) * (i / panel_height)),
                brown[1] + int((light_brown[1] - brown[1]) * (i / panel_height)),
                brown[2] + int((light_brown[2] - brown[2]) * (i / panel_height))
            )
            pygame.draw.line(s, current_color, (0, i), (panel_width, i))
        s.set_alpha(240)
        screen.blit(s, panel_rect)
        
        # Двойная рамка панели
        pygame.draw.rect(screen, gold, panel_rect, 2)
        pygame.draw.rect(screen, gold, panel_rect.inflate(-8, -8), 1)
        
        # Заголовок
        title_font = pygame.font.Font(None, 40)
        title = title_font.render("Рекорды", True, (255, 215, 0))
        title_rect = title.get_rect(centerx=panel_rect.centerx, top=panel_rect.top + 15)
        
        # Тень заголовка
        title_shadow = title_font.render("Рекорды", True, (30, 30, 30))
        screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        screen.blit(title, title_rect)
        
        # Разделитель
        pygame.draw.line(screen, gold,
                        (panel_rect.left + 20, title_rect.bottom + 10),
                        (panel_rect.right - 20, title_rect.bottom + 10), 2)
        
        # Список рекордов
        record_font = pygame.font.Font(None, 32)
        y_offset = 70
        for i, (score, time) in enumerate(records[:8]):
            # Фон строки
            row_rect = pygame.Rect(panel_rect.x + 10, panel_rect.y + y_offset - 5,
                                 panel_width - 20, 35)
            if i % 2 == 0:
                s = pygame.Surface((row_rect.width, row_rect.height))
                s.fill(light_brown)
                s.set_alpha(30)
                screen.blit(s, row_rect)
            
            # Номер и данные рекорда
            rank_text = f"#{i+1}"
            score_text = f"{score:,}"
            time_text = f"{time} сек"
            
            # Отрисовка номера
            rank_surface = record_font.render(rank_text, True, (255, 215, 0))
            screen.blit(rank_surface, (panel_rect.x + 20, panel_rect.y + y_offset))
            
            # Отрисовка счета
            score_surface = record_font.render(score_text, True, (255, 215, 0))
            score_rect = score_surface.get_rect(x=panel_rect.x + 70, y=panel_rect.y + y_offset)
            screen.blit(score_surface, score_rect)
            
            # Отрисовка времени
            time_surface = record_font.render(time_text, True, (255, 215, 0))
            time_rect = time_surface.get_rect(right=panel_rect.right - 20, y=panel_rect.y + y_offset)
            screen.blit(time_surface, time_rect)
            
            y_offset += 40
    
    return button_rect

def main():
    pygame.init()
    size = width, height = 935, 660
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    
    db = Database()
    records_open = False
    records = db.get_top_records()
    
    if not show_title_screen(screen, size):
        pygame.quit()
        return
        
    while True:
        running = True
        game = Game()
        start_time = None
        
        while running:
            if game.player.has_moved and start_time is None:
                start_time = time.time()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Проверяем клик по кнопке рекордов
                    records_button_rect = draw_records_button(screen, records_open, records)
                    if records_button_rect.collidepoint(event.pos):
                        records_open = not records_open
                        if records_open:
                            records = db.get_top_records()  # Обновляем список рекордов
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.player.move('left')
                    elif event.key == pygame.K_RIGHT:
                        game.player.move('right')
                    elif event.key == pygame.K_DOWN:
                        game.player.move('bottom')
                if event.type == pygame.KEYUP:
                    game.player.move(None)

            game.update_camera()

            if game.current_health <= 0:
                time_played = time.time() - start_time if start_time else 0
                restart, save_record = show_game_over_screen(screen, size, game.money, time_played)
                
                if save_record:
                    db.add_record(game.money, int(time_played))
                    records = db.get_top_records()  # Обновляем список рекордов
                
                if restart:
                    break
                else:
                    pygame.quit()
                    return

            screen.fill((2, 137, 255))

            offset_x = width // 2 - game.board.cell_width * game.player.pos_x
            offset_y = height // 2 - game.board.cell_height * (game.player.pos_y + 2)

            game.board.render(screen, offset_x, offset_y)

            sprite = pygame.sprite.Sprite()
            sprite.rect = pygame.Rect(game.board.cell_width * game.player.pos_x,
                                    game.board.cell_height * (game.player.pos_y) +7,
                                    game.board.cell_width,
                                    game.board.cell_height)

            for s in [sprite]:
                s.rect.x += offset_x
                s.rect.y += offset_y

            screen.blit(game.player.image, sprite.rect)
            game.player.update()
            game.update()

            if game.animation_treasure:
                treasure_pos_x, treasure_pos_y = game.player.pos_x, game.player.pos_y
                game.animation_treasure = False
                
            # Отрисовка счетчика денег
            draw_money_counter(screen, game.money)
            
            # Отрисовка кнопки рекордов
            draw_records_button(screen, records_open, records)

            game.draw_health()

            pygame.display.flip()
            
    pygame.quit()

if __name__ == '__main__':
    main()