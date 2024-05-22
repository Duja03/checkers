import pygame

from Constants import *
from Game import Game

FPS = 60
pygame.init()

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Checkers")


def get_row_col_from_mouse(pos):
    x, y = pos
    row = (y - BOARD_OUTLINE_SIZE) // TILE_SIZE
    col = (x - BOARD_OUTLINE_SIZE) // TILE_SIZE
    return row, col


def main():
    run = True

    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        game.draw()

        if game.show_game and not game.game_over:
            if game.singleplayer and game.turn_color == BLACK_COLOR:
                game.play_next_move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    if game.show_game:
                        game.undo()
                        if game.singleplayer:
                            game.undo()
                elif event.button == 1:
                    cords = pygame.mouse.get_pos()
                    if game.show_game:
                        cords = get_row_col_from_mouse(cords)
                        game.select_piece(cords)
                    elif game.game_over:
                        x, y = cords
                        if (
                            x >= game.play_again_x
                            and x <= game.play_again_x + BUTTON_WIDTH
                            and y >= game.play_again_y
                            and y <= game.play_again_y + BUTTON_HEIGHT
                        ):
                            game.reset()
                            continue

                    else:
                        x, y = cords
                        if (
                            x >= game.single_x
                            and x <= game.single_x + BUTTON_WIDTH
                            and y >= game.single_y
                            and y <= game.single_y + BUTTON_HEIGHT
                        ):
                            game.show_main_menu = False
                            game.show_game = True
                            game.singleplayer = True
                            game.game_over = False
                            continue
                        if (
                            x >= game.multi_x
                            and x <= game.multi_x + BUTTON_WIDTH
                            and y >= game.multi_y
                            and y <= game.multi_y + BUTTON_HEIGHT
                        ):
                            game.show_main_menu = False
                            game.show_game = True
                            game.singleplayer = False
                            game.game_over = False
                            continue
                        # Checking for mode button:
                        if (
                            x >= game.mode_x
                            and x <= game.mode_x + BUTTON_WIDTH // 2 - 10
                            and y >= game.mode_y
                            and y <= game.mode_y + BUTTON_HEIGHT
                        ):
                            game.forced_jumping = True
                            continue
                        if (
                            x >= game.mode_x + BUTTON_WIDTH // 2 + 10
                            and x <= game.mode_x + 2 * BUTTON_WIDTH // 2
                            and y >= game.mode_y
                            and y <= game.mode_y + BUTTON_HEIGHT
                        ):
                            game.forced_jumping = False
                            continue

    pygame.quit()


# Pokretanje igre:
if __name__ == "__main__":
    main()
