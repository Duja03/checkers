import pygame

from Board import Board


class Game(object):
    TILE_SIZE = 80

    WHITE_TILE_COLOR = (255, 255, 255)
    BLACK_TILE_COLOR = (0, 0, 0)

    WHITE_PIECE_COLOR = (255, 0, 0)
    BLACK_PIECE_COLOR = (0, 100, 255)

    def __init__(self, window: pygame.Surface) -> None:
        self._board = Board()
        self._window = window

    def draw(self) -> None:
        self.draw_board()
        self.draw_pieces()
        pygame.display.update()

    def draw_board(self) -> None:
        for row in range(Board.ROWS):
            for col in range(Board.COLS):
                color = (
                    Game.WHITE_TILE_COLOR
                    if (row + col) % 2 == 0
                    else Game.BLACK_TILE_COLOR
                )

                pygame.draw.rect(
                    self._window,
                    color,(
                        col * Game.TILE_SIZE,
                        row * Game.TILE_SIZE,
                        Game.TILE_SIZE,
                        Game.TILE_SIZE,
                    ),
                )

    def draw_pieces(self) -> None:
        for row in range(Board.ROWS):
            for col in range(Board.COLS):
                piece = self._board.get_piece((row, col))
                if piece.is_empty():
                    continue

                color = (
                    Game.WHITE_PIECE_COLOR
                    if piece.is_white()
                    else Game.BLACK_PIECE_COLOR
                )

                pygame.draw.circle(
                    self._window,
                    color,
                    (
                        col * Game.TILE_SIZE + Game.TILE_SIZE // 2,
                        row * Game.TILE_SIZE + Game.TILE_SIZE // 2,
                    ),
                    Game.TILE_SIZE // 2 - 10,
                )
