import pygame
from game import Game
from player import Player
from board import Board

def main():
    size = width, height = 935, 660
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Инициализация игры')
    running = True
    treasure_pos_y = None
    treasure_pos_x = None

    game = Game()

    sprite = pygame.sprite.Sprite()
    sprite.image = game.load_image('player.png')
    sprite.rect = sprite.image.get_rect(topleft=(game.board.cell_width * game.player.pos_x,
                                                 game.board.cell_height * (game.player.pos_y + 2)))

    move_direction = None
    last_move_time = pygame.time.get_ticks()
    move_interval = 800
    draw = False

    while running:
        if game.animation_treasure:
            treasure_pos_x, treasure_pos_y = sprite.rect.x, sprite.rect.y
            draw = True
            game.animation_treasure = False
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
        if treasure_pos_y == 0:
            draw = False
        if draw:
            treasure_pos_y -= 1

        current_time = pygame.time.get_ticks()

        game.update_camera()

        if move_direction and current_time - last_move_time >= move_interval:
            previous_pos_x, previous_pos_y = game.player.pos_x, game.player.pos_y

            if move_direction == 'left':
                game.player.move('left')
            elif move_direction == 'right':
                game.player.move('right')
            elif move_direction == 'bottom':
                game.player.move('bottom')

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
        game.update()

        if draw:
            screen.blit(game.treasure_image, (treasure_pos_x, treasure_pos_y))

        game.draw_money_counter()
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()