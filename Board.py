from Constants import *
from Move import Move
from Piece import Piece


class Board(object):
    def __init__(self):
        self._board: list[Piece] = []
        self._whites_left: int = 12
        self._blacks_left: int = 12
        self._white_queens: int = 0
        self._black_queens: int = 0

        self.create_new_board()

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board: list):
        self._board = board

    def is_game_over(self):
        return self._blacks_left == 0 or self._whites_left == 0

    def evaluate(self):
        whites = [0, 0, 0, 0, 0, 0, 0]
        blacks = [0, 0, 0, 0, 0, 0, 0]

        for tile_number in range(ROWS * COLS):
            row = tile_number // COLS
            col = tile_number % COLS
            if (row + col) % 2 == 0:
                continue

            piece = self.get_piece(tile_number)
            if piece.is_empty():
                continue

            if piece.is_white():
                if not piece.is_queen():
                    whites[0] += 1
                else:
                    whites[1] += 1
                if row == BOTTOM_BORDER:
                    whites[2] += 1
                    whites[6] += 1
                    continue
                if row == 3 or row == 4:
                    if 2 <= col <= 5:
                        whites[3] += 1
                    else:
                        whites[4] += 1
                if row > TOP_BORDER and LEFT_BORDER < col < RIGHT_BORDER:
                    if (
                        self.get_piece((row - 1) * COLS + col - 1).is_black()
                        and self.get_piece((row + 1) * COLS + col + 1).is_empty()
                    ):
                        whites[5] += 1
                    if (
                        self.get_piece((row - 1) * COLS + col + 1).is_black()
                        and self.get_piece((row + 1) * COLS + col - 1).is_empty()
                    ):
                        whites[5] += 1
                if row < BOTTOM_BORDER:
                    if col == LEFT_BORDER or col == RIGHT_BORDER:
                        whites[6] += 1
                    elif (
                        self.get_piece((row + 1) * COLS + col - 1).is_white()
                        or not self.get_piece((row + 1) * COLS + col - 1).is_queen()
                    ) and (
                        self.get_piece((row + 1) * COLS + col + 1).is_white()
                        or not self.get_piece((row + 1) * COLS + col + 1).is_queen()
                    ):
                        whites[6] += 1
            else:
                if piece.is_black():
                    blacks[0] += 1
                else:
                    blacks[1] += 1
                if row == TOP_BORDER:
                    blacks[2] += 1
                    blacks[6] += 1
                    continue
                if row == 3 or row == 4:
                    if 2 <= col <= 5:
                        blacks[3] += 1
                    else:
                        blacks[4] += 1
                if row < BOTTOM_BORDER and LEFT_BORDER < col < RIGHT_BORDER:
                    if (
                        self.get_piece((row + 1) * COLS + col - 1).is_white()
                        and self.get_piece((row - 1) * COLS + col + 1).is_empty()
                    ):
                        blacks[5] += 1
                    if (
                        self.get_piece((row + 1) * COLS + col + 1).is_white()
                        and self.get_piece((row - 1) * COLS + col - 1).is_empty()
                    ):
                        blacks[5] += 1
                if row > TOP_BORDER:
                    if col == LEFT_BORDER or col == RIGHT_BORDER:
                        blacks[6] += 1
                    elif (
                        self.get_piece((row - 1) * COLS + col - 1).is_black()
                        or not self.get_piece((row - 1) * COLS + col - 1).is_queen()
                    ) and (
                        self.get_piece((row - 1) * COLS + col + 1).is_black()
                        or not self.get_piece((row - 1) * COLS + col + 1).is_queen()
                    ):
                        blacks[6] += 1
        weights = [5, 7.5, 4, 2.5, 0.5, -3, 3]
        score = 0
        for i in range(7):
            score += weights[i] * (blacks[i] - whites[i])
        return score

    def create_new_board(self):
        self._board = [None] * ROWS * COLS
        # Set the initial state of the board:
        for tile_number in range(ROWS * COLS):
            row = tile_number // COLS
            col = tile_number % COLS
            self._board[tile_number] = Piece(row, col, EMPTY_TILE)
            if (row + col) % 2 == 1:
                if row <= 2:
                    self._board[tile_number].piece = BLACK_PIECE
                elif row >= 5:
                    self._board[tile_number].piece = WHITE_PIECE

    def get_piece(self, tile_number: int) -> Piece:
        return self._board[tile_number]

    def _calculate_next_jumps(
        self,
        org_tile: int,
        piece_tile: int,
        dir: tuple[int, int],
        all_moves: list[Move],
        eaten: list,
    ):
        org_piece = self.get_piece(org_tile)
        cur_piece = self.get_piece(piece_tile)

        short_dirs = (
            [(dir[0], dir[1]), (dir[0], -dir[1]), (-dir[0], dir[1])]
            if org_piece.is_queen()
            else [(dir[0], dir[1]), (dir[0], -dir[1])]
        )

        for sh_dir in short_dirs:
            short_cords = (cur_piece.row + sh_dir[0], cur_piece.col + sh_dir[1])
            if (
                TOP_BORDER <= short_cords[0] <= BOTTOM_BORDER
                and LEFT_BORDER <= short_cords[1] <= RIGHT_BORDER
            ):
                # Getting the piece on the short diagonal tile:
                short_tile = short_cords[0] * COLS + short_cords[1]
                short_piece = self.get_piece(short_tile)

                if short_piece.is_empty():
                    continue
                if short_piece.is_opposite_color(org_piece):
                    adv_cords = (
                        cur_piece.row + 2 * sh_dir[0],
                        cur_piece.col + 2 * sh_dir[1],
                    )
                    if (
                        TOP_BORDER <= adv_cords[0] <= BOTTOM_BORDER
                        and LEFT_BORDER <= adv_cords[1] <= RIGHT_BORDER
                    ):
                        # Getting the piece on the longer diagonal tile:
                        adv_tile = adv_cords[0] * COLS + adv_cords[1]
                        adv_piece = self.get_piece(adv_tile)

                        if adv_piece.is_empty():
                            new_eaten = eaten + [(short_tile, short_piece.piece)]
                            all_moves.append(Move(org_tile, adv_tile, new_eaten))
                            self._calculate_next_jumps(
                                adv_tile, adv_tile, sh_dir, all_moves, new_eaten
                            )

    def calculate_next_moves(self, piece_tile: int) -> list[Move]:
        all_moves = []
        # Basic data:
        piece = self.get_piece(piece_tile)
        if piece.is_empty():
            return

        row_dir = -1 if piece.is_white() else 1
        short_dirs = (
            [(row_dir, 1), (row_dir, -1), (-row_dir, 1), (-row_dir, -1)]
            if piece.is_queen()
            else [(row_dir, 1), (row_dir, -1)]
        )

        for sh_dir in short_dirs:
            short_cords = (piece.row + sh_dir[0], piece.col + sh_dir[1])
            if (
                TOP_BORDER <= short_cords[0] <= BOTTOM_BORDER
                and LEFT_BORDER <= short_cords[1] <= RIGHT_BORDER
            ):
                # Getting the piece on the short diagonal tile:
                short_tile = short_cords[0] * COLS + short_cords[1]
                short_piece = self.get_piece(short_tile)

                if short_piece.is_empty():
                    # Adding a simple move:
                    all_moves.append(Move(piece_tile, short_tile))
                elif short_piece.is_opposite_color(piece):
                    adv_cords = (
                        short_piece.row + sh_dir[0],
                        short_piece.col + sh_dir[1],
                    )
                    if (
                        TOP_BORDER <= adv_cords[0] <= BOTTOM_BORDER
                        and LEFT_BORDER <= adv_cords[1] <= RIGHT_BORDER
                    ):
                        # Getting the piece on the longer diagonal tile:
                        adv_tile = adv_cords[0] * COLS + adv_cords[1]
                        adv_piece = self.get_piece(adv_tile)
                        if adv_piece.is_empty():
                            # Adding a piece to eat:
                            eaten = [(short_tile, short_piece.piece)]
                            all_moves.append(Move(piece_tile, adv_tile, eaten))
                            self._calculate_next_jumps(
                                piece_tile, adv_tile, sh_dir, all_moves, eaten
                            )
        # Sorting moves by the number of eaten pieces:
        all_moves.sort(key=lambda mov: len(mov.eaten_tiles), reverse=True)
        return all_moves

    def get_all_piece_tiles(self, color: int) -> list[int]:
        """
        Returns a list of tile numbers of pieces of the given color.
        """
        assert color == WHITE_COLOR or color == BLACK_COLOR

        pieces = []
        for piece in self._board:
            if not piece.is_empty() and piece.is_color(color):
                pieces.append(piece.row * COLS + piece.col)
        return pieces

    def calculate_all_turn_moves(self, color: int) -> list[Move]:
        assert color == WHITE_COLOR or color == BLACK_COLOR
        all_turn_moves = []
        piece_tiles = self.get_all_piece_tiles(color)
        for piece_tile in piece_tiles:
            all_turn_moves += self.calculate_next_moves(piece_tile)
        # Sorting moves by the number of eaten pieces:
        all_turn_moves.sort(key=lambda mov: len(mov.eaten_tiles), reverse=True)
        return all_turn_moves

    def make_move(self, move: Move):
        start_piece = self.get_piece(move.start_tile)
        target_piece = self.get_piece(move.target_tile)
        # Potential queen promotion:
        if target_piece.row == TOP_BORDER or target_piece.row == BOTTOM_BORDER:
            target_piece.piece = start_piece.promoted_to_queen()
            if start_piece.is_white():
                self._white_queens += 1
            else:
                self._black_queens += 1
        else:
            target_piece.piece = start_piece.piece

        start_piece.piece = EMPTY_TILE

        # Removing eaten pieces:
        for eaten_tile, piece_type in move.eaten_tiles:
            eaten_piece = self.get_piece(eaten_tile)
            # Decreasing number of pieces:
            if eaten_piece.is_queen():
                if eaten_piece.is_white():
                    self._white_queens -= 1
                    self._whites_left -= 1
                else:
                    self._black_queens -= 1
                    self._blacks_left -= 1
            else:
                if eaten_piece.is_white():
                    self._whites_left -= 1
                else:
                    self._blacks_left -= 1

            eaten_piece.piece = EMPTY_TILE

    def undo_move(self, move: Move):
        start_piece = self.get_piece(move.start_tile)
        target_piece = self.get_piece(move.target_tile)
        # Potential queen demotion:
        if target_piece.row == TOP_BORDER or target_piece.row == BOTTOM_BORDER:
            if target_piece.is_white():
                self._white_queens -= 1
            else:
                self._black_queens -= 1
            start_piece.piece = target_piece.demoted_to_piece()
        else:
            start_piece.piece = target_piece.piece

        target_piece.piece = EMPTY_TILE

        # Adding eaten pieces:
        for eaten_tile, piece_type in move.eaten_tiles:
            eaten_piece = self.get_piece(eaten_tile)
            # Increase number of pieces:
            if Piece.is_piece_queen(piece_type):
                if Piece.is_piece_white(piece_type):
                    self._white_queens += 1
                    self._whites_left += 1
                else:
                    self._black_queens += 1
                    self._blacks_left += 1
            else:
                if Piece.is_piece_white(piece_type):
                    self._whites_left += 1
                else:
                    self._blacks_left += 1

            eaten_piece.piece = piece_type

    def __str__(self) -> str:
        ans = ""
        for tile_number in range(ROWS * COLS):
            ans += str(self._board[tile_number])
            if tile_number % COLS == RIGHT_BORDER:
                ans += "\n"
        return ans

    def __repr__(self) -> str:
        return self.__str__()


if __name__ == "__main__":
    brd = Board()
    print(brd)
    print(brd.calculate_all_turn_moves(BLACK_COLOR))
