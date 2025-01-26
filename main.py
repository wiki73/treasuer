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
    sprite.rect = pygame.Rect(game.board.cell_width * game.player.pos_x,
                            game.board.cell_height * (game.player.pos_y + 1),
                            game.board.cell_width,
                            game.board.cell_height)

    move_direction = None
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
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()