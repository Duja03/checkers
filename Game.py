import pygame

from Board import Board
from TileState import TileState


class Game(object):
    TILE_SIZE = 80

    WHITE_TILE_COLOR = (255, 255, 255)
    BLACK_TILE_COLOR = (0, 0, 0)

    WHITE_PIECE_COLOR = (255, 0, 0)
    BLACK_PIECE_COLOR = (0, 100, 255)

    VALID_MOVE_COLOR = (0, 255, 0)

    def __init__(self, window: pygame.Surface) -> None:
        self._board = Board()
        self._window = window
        self._turn_color = TileState.WHITE_COLOR
        self._selected_piece = None
        self._current_turn_moves = []

    @property
    def turn_color(self) -> TileState:
        return self._turn_color

    @turn_color.setter
    def turn(self, turn: TileState) -> None:
        self._turn_color = turn

    @property
    def board(self) -> Board:
        return self._board

    @board.setter
    def board(self, board: Board) -> None:
        self._board = board

    def draw(self) -> None:
        self.draw_board()
        self.draw_pieces()
        self.draw_valid_moves()
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
                    color,
                    (
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

    def draw_valid_moves(self) -> None:
        for move in self._current_turn_moves:
            pygame.draw.circle(
                self._window,
                (0, 255, 0),
                (
                    move.target_cords[1] * Game.TILE_SIZE + Game.TILE_SIZE // 2,
                    move.target_cords[0] * Game.TILE_SIZE + Game.TILE_SIZE // 2,
                ),
                Game.TILE_SIZE // 10,
            )

    def change_turn(self):
        self._turn_color = (
            TileState.WHITE_COLOR
            if self._turn_color == TileState.BLACK_COLOR
            else TileState.BLACK_COLOR
        )

    def select_piece(self, cords: tuple) -> None:
        if self._selected_piece is None:
            turn_pieces = self._board.get_all_pieces(self._turn_color)
            # If we selected wrong piece, do nothing
            if cords not in turn_pieces:
                self._selected_piece = None
                self._current_turn_moves = []
                return
            self._board.calculate_next_moves(cords, self._current_turn_moves)
            self._selected_piece = cords
        else:
            for move in self._current_turn_moves:
                if (
                    move.start_cords == self._selected_piece
                    and move.target_cords == cords
                ):
                    self._board.make_move(move)
                    self._selected_piece = None
                    self._current_turn_moves = []
                    self.change_turn()
                    break
            else:
                self._selected_piece = None
                self._current_turn_moves = []
