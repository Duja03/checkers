import time
from copy import deepcopy

import pygame

from Algorithm import minimax
from Board import Board
from Constants import *
from Move import Move


class Game(object):
    def __init__(self, window: pygame.Surface) -> None:
        self._board = Board()
        self._window = window
        self._turn_color: int = WHITE_COLOR
        self._selected_piece: int = None
        self._current_turn_moves: list[Move] = []
        self.move_stack: list[Move] = []

    @property
    def turn_color(self) -> int:
        return self._turn_color

    @turn_color.setter
    def turn_color(self, turn: int) -> None:
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
        for tile_number in range(ROWS * COLS):
            row = tile_number // COLS
            col = tile_number % COLS
            color = WHITE_TILE_COLOR if (row + col) % 2 == 0 else BLACK_TILE_COLOR

            pygame.draw.rect(
                self._window,
                color,
                (
                    col * TILE_SIZE,
                    row * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE,
                ),
            )

    def draw_pieces(self) -> None:
        for tile_number in range(ROWS * COLS):
            row = tile_number // COLS
            col = tile_number % COLS
            piece = self._board.get_piece(tile_number)
            if piece.is_empty():
                continue

            color = WHITE_PIECE_COLOR if piece.is_white() else BLACK_PIECE_COLOR

            pygame.draw.circle(
                self._window,
                color,
                (
                    col * TILE_SIZE + TILE_SIZE // 2,
                    row * TILE_SIZE + TILE_SIZE // 2,
                ),
                TILE_SIZE // 2 - 10,
            )

            # Drawing queen:
            if piece.is_queen():
                pygame.draw.circle(
                    self._window,
                    QUEEN_COLOR,
                    (
                        col * TILE_SIZE + TILE_SIZE // 2,
                        row * TILE_SIZE + TILE_SIZE // 2,
                    ),
                    TILE_SIZE // 5,
                )

    def draw_valid_moves(self) -> None:
        for move in self._current_turn_moves:
            target_piece = self._board.get_piece(move.target_tile)
            pygame.draw.circle(
                self._window,
                VALID_MOVE_COLOR,
                (
                    target_piece.col * TILE_SIZE + TILE_SIZE // 2,
                    target_piece.row * TILE_SIZE + TILE_SIZE // 2,
                ),
                TILE_SIZE // 10,
            )

    def change_turn(self):
        self._turn_color = (
            BLACK_COLOR if self._turn_color == WHITE_COLOR else WHITE_COLOR
        )

    def play_next_move(self):
        print("Computer is thinking...")
        start_time = time.time()
        # Save the current state of the board:
        board = deepcopy(self._board.board)
        value, move = minimax(
            self._board,
            6,
            float("-inf"),
            float("inf"),
            self._turn_color == BLACK_COLOR,
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        # Bring back old board state:
        self._board.board = board
        print(f"Value: {value}, Move: {move}")
        print(f"Elapsed time: {elapsed_time} seconds")

        self.make_move(move)

    def make_move(self, move: Move):
        self._board.make_move(move)
        self.change_turn()
        self.move_stack.append(move)

    def undo(self):
        if self.move_stack:
            move = self.move_stack.pop()
            self._board.undo_move(move)
            self.change_turn()

    def select_piece(self, cords: tuple[int, int]) -> None:
        selected_tile = cords[0] * COLS + cords[1]
        if self._selected_piece is None:
            turn_pieces = self._board.get_all_piece_tiles(self._turn_color)
            # If we selected wrong piece, do nothing
            if selected_tile not in turn_pieces:
                self._selected_piece = None
                self._current_turn_moves = []
                return
            self._current_turn_moves = self._board.calculate_next_moves(selected_tile)
            print(self._current_turn_moves)
            self._selected_piece = selected_tile
        else:
            for move in self._current_turn_moves:
                if (
                    move.start_tile == self._selected_piece
                    and move.target_tile == selected_tile
                ):
                    self._board.make_move(move)
                    self._selected_piece = None
                    self._current_turn_moves = []
                    self.change_turn()
                    self.move_stack.append(move)
                    break
            else:
                self._selected_piece = None
                self._current_turn_moves = []
