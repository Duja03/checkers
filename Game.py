import time
from copy import deepcopy

import pygame

from Algorithm import minimax
from Board import Board
from Constants import *
from Move import Move


class Game(object):
    def __init__(self, window: pygame.Surface) -> None:
        self._window = window
        self._text_font = pygame.font.SysFont("Arial", 30, True)
        self._header_font = pygame.font.SysFont("Arial", 72, True)
        self.single_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
        self.single_y = SCREEN_HEIGHT // 2 - BUTTON_HEIGHT - 20
        self.multi_x = self.single_x
        self.multi_y = self.single_y + BUTTON_HEIGHT + 20
        self.mode_x = self.multi_x
        self.mode_y = self.multi_y + BUTTON_HEIGHT + 70
        self.play_again_x = self.multi_x
        self.play_again_y = self.multi_y + 50
        
        self.reset()

    def reset(self) -> None:
        self._board = Board()
        self._turn_color = WHITE_COLOR
        self._selected_piece = None
        self._current_turn_moves = []
        self.move_stack = []
        self.show_main_menu = True
        self.show_game = False
        self.forced_jumping = False
        self.singleplayer = True
        self.game_over = False
        self.white_won = False

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
        if self.show_main_menu:
            self.draw_main_menu()
        if self.show_game:
            self.draw_board()
            self.draw_pieces()
            self.draw_valid_moves()
        if self.game_over:
            self.draw_game_over()
        pygame.display.update()

    def draw_game_over(self) -> None:
        self._window.fill(MAIN_MENU_COLOR)
        if self.white_won:
            text = "White won!"
        else:
            text = "Black won!"
        text_surface = self._header_font.render(text, True, HEADER_COLOR)
        text_x = SCREEN_WIDTH // 2 - 150
        text_y = SCREEN_HEIGHT // 2 - 80
        self._window.blit(text_surface, (text_x, text_y))
        # Drawing return button:
        pygame.draw.rect(
            self._window,
            BUTTON_COLOR,
            (
                self.play_again_x,
                self.play_again_y,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
        )
        # Render the text
        return_surface = self._text_font.render("Play again", True, TEXT_COLOR)
        return_btn_x = self.single_x + BUTTON_WIDTH // 2 - 60
        return_btn_y = self.multi_y + 65
        self._window.blit(return_surface, (return_btn_x, return_btn_y))

    def draw_board(self) -> None:
        pygame.draw.rect(
            self._window, BOARD_OUTLINE_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        for tile_number in range(ROWS * COLS):
            row = tile_number // COLS
            col = tile_number % COLS
            color = WHITE_TILE_COLOR if (row + col) % 2 == 0 else BLACK_TILE_COLOR

            pygame.draw.rect(
                self._window,
                color,
                (
                    col * TILE_SIZE + BOARD_OUTLINE_SIZE,
                    row * TILE_SIZE + BOARD_OUTLINE_SIZE,
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
            shadow = (
                WHITE_PIECE_SHADOW_COLOR
                if piece.is_white()
                else BLACK_PIECE_SHADOW_COLOR
            )

            # Shadow of piece:
            pygame.draw.circle(
                self._window,
                shadow,
                (
                    col * TILE_SIZE + TILE_SIZE // 2 + BOARD_OUTLINE_SIZE,
                    row * TILE_SIZE
                    + TILE_SIZE // 2
                    + BOARD_OUTLINE_SIZE
                    + SHADOW_SIZE // 2,
                ),
                TILE_SIZE // 2 - 10,
            )
            pygame.draw.circle(
                self._window,
                color,
                (
                    col * TILE_SIZE + TILE_SIZE // 2 + BOARD_OUTLINE_SIZE,
                    row * TILE_SIZE
                    + TILE_SIZE // 2
                    + BOARD_OUTLINE_SIZE
                    - SHADOW_SIZE // 2,
                ),
                TILE_SIZE // 2 - 10,
            )

            queen_color = (
                WHITE_PIECE_SHADOW_COLOR
                if piece.is_white()
                else BLACK_PIECE_SHADOW_COLOR
            )

            # Drawing queen:
            if piece.is_queen():
                pygame.draw.circle(
                    self._window,
                    queen_color,
                    (
                        col * TILE_SIZE + TILE_SIZE // 2 + BOARD_OUTLINE_SIZE,
                        row * TILE_SIZE
                        + TILE_SIZE // 2
                        + BOARD_OUTLINE_SIZE
                        - SHADOW_SIZE // 2,
                    ),
                    TILE_SIZE // 2 - 15,
                )
                pygame.draw.circle(
                    self._window,
                    color,
                    (
                        col * TILE_SIZE + TILE_SIZE // 2 + BOARD_OUTLINE_SIZE,
                        row * TILE_SIZE
                        + TILE_SIZE // 2
                        + BOARD_OUTLINE_SIZE
                        - SHADOW_SIZE // 2,
                    ),
                    TILE_SIZE // 2 - 18,
                )

    def draw_valid_moves(self) -> None:
        for move in self._current_turn_moves:
            target_piece = self._board.get_piece(move.target_tile)
            pygame.draw.circle(
                self._window,
                VALID_MOVE_COLOR,
                (
                    target_piece.col * TILE_SIZE + TILE_SIZE // 2 + BOARD_OUTLINE_SIZE,
                    target_piece.row * TILE_SIZE + TILE_SIZE // 2 + BOARD_OUTLINE_SIZE,
                ),
                TILE_SIZE // 10,
            )

    def draw_main_menu(self) -> None:
        # Background:
        pygame.draw.rect(
            self._window, MAIN_MENU_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        # Drawing header:
        header_surface = self._header_font.render("Checkers", True, HEADER_COLOR)
        header_x = SCREEN_WIDTH // 2 - 135
        header_y = SCREEN_HEIGHT // 10
        self._window.blit(header_surface, (header_x, header_y))
        # Single player button:
        pygame.draw.rect(
            self._window,
            BUTTON_COLOR,
            (
                self.single_x,
                self.single_y,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
        )
        # Render the text
        single_surface = self._text_font.render("1 Player", True, TEXT_COLOR)
        single_btn_x = self.single_x + BUTTON_WIDTH // 2 - 50
        single_btn_y = self.single_y + 16
        self._window.blit(single_surface, (single_btn_x, single_btn_y))
        # Multi player button:
        pygame.draw.rect(
            self._window,
            BUTTON_COLOR,
            (
                self.multi_x,
                self.multi_y,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
        )
        # Render the text
        multi_surface = self._text_font.render("2 Player", True, TEXT_COLOR)
        multi_btn_x = self.multi_x + BUTTON_WIDTH // 2 - 50
        multi_btn_y = self.multi_y + 16
        self._window.blit(multi_surface, (multi_btn_x, multi_btn_y))
        # Render mode selection text:
        mode_surface = self._text_font.render("Forced jumping", True, BUTTON_COLOR)
        mode_x = self.mode_x
        mode_y = self.mode_y - 45
        self._window.blit(mode_surface, (mode_x, mode_y))
        # Drawing button for selecting game mode:
        pygame.draw.rect(
            self._window,
            ACTIVE_BUTTON_COLOR if self.forced_jumping else BUTTON_COLOR,
            (
                self.mode_x,
                self.mode_y,
                BUTTON_WIDTH // 2 - 10,
                BUTTON_HEIGHT,
            ),
        )
        # Render the YES text:
        yes_surface = self._text_font.render("YES", True, TEXT_COLOR)
        yes_btn_x = self.mode_x + BUTTON_WIDTH // 4 - 30
        yes_btn_y = self.mode_y + 16
        self._window.blit(yes_surface, (yes_btn_x, yes_btn_y))
        pygame.draw.rect(
            self._window,
            BUTTON_COLOR if self.forced_jumping else ACTIVE_BUTTON_COLOR,
            (
                self.mode_x + BUTTON_WIDTH // 2 + 10,
                self.mode_y,
                BUTTON_WIDTH // 2 - 10,
                BUTTON_HEIGHT,
            ),
        )
        # Render the NO text:
        no_surface = self._text_font.render("NO", True, TEXT_COLOR)
        no_btn_x = self.mode_x + BUTTON_WIDTH // 2 + BUTTON_WIDTH // 4 - 12
        no_btn_y = self.mode_y + 16
        self._window.blit(no_surface, (no_btn_x, no_btn_y))

    def change_turn(self):
        self._turn_color = (
            BLACK_COLOR if self._turn_color == WHITE_COLOR else WHITE_COLOR
        )

    def play_next_move(self) -> bool:
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
            self.forced_jumping,
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        # Bring back old board state:
        self._board.board = board
        # Checking game state:
        if move is not None:
            self.make_move(move)
            my_moves = self._board.calculate_all_turn_moves(self._turn_color)
            if not my_moves:
                print("Game over! Black won!")
                self.game_over = True
                self.show_game = False
                self.white_won = False
        else:
            print("Game over! White won!")
            self.game_over = True
            self.show_game = False
            self.white_won = True

        print(f"It took it: {elapsed_time} seconds to find a move.")

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
            self._current_turn_moves = self._board.calculate_next_moves(
                selected_tile, self.forced_jumping
            )
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
