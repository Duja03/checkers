import random
import time
from copy import deepcopy

import pygame

from Board import Board
from Constants import *
from Move import Move
from Piece import Piece


class Game(object):
    transposition_table = {}

    def __init__(self, window: pygame.Surface) -> None:
        self._window = window
        self._text_font = pygame.font.SysFont("Arial", TEXT_SIZE)
        self._header_font = pygame.font.SysFont("Arial", HEADER_SIZE)
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
        self.played_move: Move = None
        self.selected_color = SELECTED_TILE_WHITE_COLOR
        self.start_time = time.time()

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
            self.draw_played_move()
            self.draw_selected_tile()
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
        text_x = SCREEN_WIDTH // 2 - 140
        text_y = SCREEN_HEIGHT // 4
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
        return_btn_y = self.multi_y + 70
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
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        alpha = (80,)

        for move in self._current_turn_moves:
            move_tile = move.target_tile
            org_tile = move.start_tile

            row = move_tile // COLS
            col = move_tile % COLS

            piece = self._board.get_piece(org_tile)

            color = (
                WHITE_PIECE_COLOR + alpha
                if piece.is_white()
                else BLACK_PIECE_COLOR + alpha
            )
            shadow = (
                WHITE_PIECE_SHADOW_COLOR + alpha
                if piece.is_white()
                else BLACK_PIECE_SHADOW_COLOR + alpha
            )

            # Shadow of piece:
            pygame.draw.circle(
                surf,
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
                surf,
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
                WHITE_PIECE_SHADOW_COLOR + alpha
                if piece.is_white()
                else BLACK_PIECE_SHADOW_COLOR + alpha
            )

            # Drawing queen:
            if piece.is_queen():
                pygame.draw.circle(
                    surf,
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
                    surf,
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

        self._window.blit(surf, (0, 0))

    def draw_selected_tile(self) -> None:
        if self._selected_piece is None:
            return
        row = self._selected_piece // COLS
        col = self._selected_piece % COLS

        pygame.draw.rect(
            self._window,
            SELECTED_TILE_BASE_COLOR,
            (
                col * TILE_SIZE + BOARD_OUTLINE_SIZE,
                row * TILE_SIZE + BOARD_OUTLINE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            ),
        )

    def draw_played_move(self) -> None:
        if self.played_move is None:
            return
        # Outline tile on which the piece was moved:
        start_tile = self.played_move.start_tile
        start_row = start_tile // COLS
        start_col = start_tile % COLS
        # Fill inside of the tile:
        pygame.draw.rect(
            self._window,
            self.selected_color,
            (
                start_col * TILE_SIZE + BOARD_OUTLINE_SIZE,
                start_row * TILE_SIZE + BOARD_OUTLINE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            ),
        )
        pygame.draw.rect(
            self._window,
            BLACK_TILE_COLOR,
            (
                start_col * TILE_SIZE + BOARD_OUTLINE_SIZE + PLAYED_TILE_OUTLINE_SIZE,
                start_row * TILE_SIZE + BOARD_OUTLINE_SIZE + PLAYED_TILE_OUTLINE_SIZE,
                TILE_SIZE - 2 * PLAYED_TILE_OUTLINE_SIZE,
                TILE_SIZE - 2 * PLAYED_TILE_OUTLINE_SIZE,
            ),
        )
        # Fill inside of the tile:
        end_tile = self.played_move.target_tile
        end_row = end_tile // COLS
        end_col = end_tile % COLS
        # Outline tile from which the piece was moved:
        pygame.draw.rect(
            self._window,
            self.selected_color,
            (
                end_col * TILE_SIZE + BOARD_OUTLINE_SIZE,
                end_row * TILE_SIZE + BOARD_OUTLINE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            ),
        )
        pygame.draw.rect(
            self._window,
            BLACK_TILE_COLOR,
            (
                end_col * TILE_SIZE + BOARD_OUTLINE_SIZE + PLAYED_TILE_OUTLINE_SIZE,
                end_row * TILE_SIZE + BOARD_OUTLINE_SIZE + PLAYED_TILE_OUTLINE_SIZE,
                TILE_SIZE - 2 * PLAYED_TILE_OUTLINE_SIZE,
                TILE_SIZE - 2 * PLAYED_TILE_OUTLINE_SIZE,
            ),
        )

    def draw_main_menu(self) -> None:
        # Background:
        pygame.draw.rect(
            self._window, MAIN_MENU_COLOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        # Drawing header:
        header_surface = self._header_font.render("Checkers", True, HEADER_COLOR)
        header_x = SCREEN_WIDTH // 2 - 130
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
        single_btn_y = self.single_y + 20
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
        multi_btn_y = self.multi_y + 20
        self._window.blit(multi_surface, (multi_btn_x, multi_btn_y))
        # Render mode selection text:
        mode_surface = self._text_font.render("Forced jumping?", True, BUTTON_COLOR)
        mode_x = self.mode_x + 15
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
        yes_btn_y = self.mode_y + 20
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
        no_btn_y = self.mode_y + 20
        self._window.blit(no_surface, (no_btn_x, no_btn_y))

    def change_turn(self):
        self._turn_color = (
            BLACK_COLOR if self._turn_color == WHITE_COLOR else WHITE_COLOR
        )

    def make_move(self, move: Move):
        self._board.make_move(move)
        self.change_turn()
        self.move_stack.append(move)
        self.played_move = move

    def undo(self):
        if self.move_stack:
            move = self.move_stack.pop()
            self.selected_color = UNDO_SELECTED_TILE_COLOR
            self._board.undo_move(move)
            self.change_turn()
            self.played_move = move

    def select_piece(self, cords: tuple[int, int]) -> None:
        selected_tile = cords[0] * COLS + cords[1]
        if self._selected_piece is None:
            turn_pieces = self._board.get_all_piece_tiles(self._turn_color)
            # If we selected wrong piece, do nothing
            if selected_tile not in turn_pieces:
                self._selected_piece = None
                self._current_turn_moves = []
                return
            all_turn_color_moves = self._board.calculate_all_turn_moves(
                self._turn_color, self.forced_jumping
            )
            # Now we only want to show moves for selected piece:
            for move in all_turn_color_moves:
                if move.start_tile == selected_tile:
                    self._current_turn_moves.append(move)
            self._selected_piece = selected_tile
        else:
            for move in self._current_turn_moves:
                if (
                    move.start_tile == self._selected_piece
                    and move.target_tile == selected_tile
                ):
                    self.selected_color = (
                        SELECTED_TILE_WHITE_COLOR
                        if Piece.is_piece_white(self.turn_color)
                        else SELECTED_TILE_BLACK_COLOR
                    )
                    self.make_move(move)
                    self._selected_piece = None
                    self._current_turn_moves = []
                    break
            else:
                self._selected_piece = None
                self._current_turn_moves = []

    def determine_depth(self) -> int:
        # Example logic for determining depth:
        num_pieces = self._board._whites_left + self._board._blacks_left
        if self.forced_jumping:
            if num_pieces >= 20:
                return 6
            elif num_pieces >= 10:
                return 7
            else:
                return 8
        else:
            if num_pieces >= 20:
                return 5
            elif num_pieces >= 10:
                return 6
            else:
                return 7

    def play_next_move(self) -> bool:
        print("Computer is thinking...")
        self.start_time = time.time()

        # Variable depth depending on pieces left:
        depth = self.determine_depth()
        print(f"Using search depth: {depth}")

        # Save the current state of the board:
        board = deepcopy(self._board.board)
        value, move = self.minimax(
            self._board,
            depth,
            float("-inf"),
            float("inf"),
            self._turn_color == BLACK_COLOR,
            self.forced_jumping,
        )
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        # Bring back old board state:
        self._board.board = board
        # Checking game state:

        print(f"Move: {move}")
        if move is not None:
            self.make_move(move)
            my_moves = self._board.calculate_all_turn_moves(
                self._turn_color, self.forced_jumping
            )
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

        self.selected_color = SELECTED_TILE_BLACK_COLOR
        print(f"It took it: {elapsed_time} seconds to find a move.")

    def minimax(
        self,
        state: Board,
        depth: int,
        alpha: float,
        beta: float,
        is_maximising_player: bool,
        forced_jumping: bool = False,
    ):
        state_str = str(state)
        if state_str not in self.transposition_table:
            self.transposition_table[state_str] = state.evaluate()

        if time.time() - self.start_time > 3:
            return self.transposition_table[state_str], None

        if depth == 0 or state.is_game_over():
            return self.transposition_table[state_str], None

        maximizing = not is_maximising_player

        if is_maximising_player:
            max_eval = float("-inf")
            best_move = None
            for move in state.calculate_all_turn_moves(BLACK_COLOR, forced_jumping):
                state.make_move(move)
                eval = self.minimax(
                    state, depth - 1, alpha, beta, maximizing, forced_jumping
                )[0]
                state.undo_move(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move
        else:
            min_eval = float("inf")
            best_move = None
            for move in state.calculate_all_turn_moves(WHITE_COLOR, forced_jumping):
                state.make_move(move)
                eval = self.minimax(
                    state,
                    depth - 1,
                    alpha,
                    beta,
                    maximizing,
                    forced_jumping,
                )[0]
                state.undo_move(move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move
