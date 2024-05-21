import pygame

from Algorithm import minimax
from Board import Board
from Constants import *
from Game import Game

FPS = 60
WIN = pygame.display.set_mode((TILE_SIZE * COLS, TILE_SIZE * ROWS))
pygame.display.set_caption("Checkers")


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // TILE_SIZE
    col = x // TILE_SIZE
    return row, col


def main():
    run = True

    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        game.draw()

        if game.turn_color == BLACK_COLOR:
            game.play_next_move()
        #game.play_next_move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    game.undo()
                elif event.button == 1:
                    cords = get_row_col_from_mouse(pygame.mouse.get_pos())
                    game.select_piece(cords)

        # game.update()

    pygame.quit()


# Pokretanje igre:
if __name__ == "__main__":
    main()
