import time

import pygame

from Algorithm import minimax
from Board import Board
from Game import Game
from TileState import TileState

FPS = 60
WIN = pygame.display.set_mode(
    (Game.TILE_SIZE * Board.COLS, Game.TILE_SIZE * Board.ROWS)
)
pygame.display.set_caption("Checkers")

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // Game.TILE_SIZE
    col = x // Game.TILE_SIZE
    return row, col

def main():
    run = True

    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        game.draw()

        if game.turn_color == TileState.BLACK_COLOR:
            game.play_next_move()

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
