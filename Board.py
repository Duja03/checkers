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
        # If I'm not mistaken this is the order of scoring
        # for victory state of the board, depending on color:
        if self._whites_left <= 0:
            return float("inf")
        elif self._blacks_left <= 0:
            return float("-inf")

        # There are 7 criteriums for good heuristics...
        # index 0: number of regular pieces
        # index 1: number of queens
        # index 2: number of pieces in back row
        # index 3: number of pieces in middle box
        # index 4: number of pieces in middle 2 rows, but not in box
        # index 5: number of pieces that can be taken this turn
        # index 6: number of pieces that are protected:
        whites = [0, 0, 0, 0, 0, 0, 0]
        blacks = [0, 0, 0, 0, 0, 0, 0]

        whites[0] = self._whites_left - self._white_queens
        blacks[0] = self._blacks_left - self._black_queens

        whites[1] = self._white_queens
        blacks[1] = self._black_queens

        # Now lookup every piece on the board:
        for tile_number in range(ROWS * COLS):
            # row, col are used for transforming 1D to 2D:
            row = tile_number // COLS
            col = tile_number % COLS

            # We skip white tiles:
            if (row + col) % 2 == 0:
                continue

            # Current piece:
            piece = self.get_piece(tile_number)
            if piece.is_empty():
                continue

            if piece.is_white():
                # Now back rows:
                if row == BOTTOM_BORDER:
                    whites[2] += 1
                    whites[6] += 1
                    continue

                # Middle area of the board:
                if row == 3 or row == 4:
                    # Checking for middle box:
                    if 2 <= col <= 5:
                        whites[3] += 1
                    else:
                        whites[4] += 1

                # Checking for pieces that can be taken this turn:
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

                # Checking for protected pieces:
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

                # This time top side:
                if row == TOP_BORDER:
                    blacks[2] += 1
                    blacks[6] += 1
                    continue

                # Middle area...
                if row == 3 or row == 4:
                    # Box in the middle:
                    if 2 <= col <= 5:
                        blacks[3] += 1
                    else:
                        blacks[4] += 1

                # Pieces that can be eaten:
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

                # Protected pieces:
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

        # Every criteria has more or less impact on the game
        # so we need to 'weight' them:
        weights = [5, 7.5, 4, 2.5, 0.5, -3, 3]

        # Accumulating final score:
        score = 0
        for i in range(7):
            score += weights[i] * (blacks[i] - whites[i])

        return score

    def create_new_board(self):
        self._board = [None] * ROWS * COLS
        # Setting the initial state of the board:
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
        # Save data of original piece:
        org_piece = self.get_piece(org_tile)
        cur_piece = self.get_piece(piece_tile)

        # Now short_dirs will also depend on direction we came from
        # so we won't go back and forth, and that is why
        # there are only 3 directions for queens:
        short_dirs = (
            [(dir[0], dir[1]), (dir[0], -dir[1]), (-dir[0], dir[1])]
            if org_piece.is_queen()
            else [(dir[0], dir[1]), (dir[0], -dir[1])]
        )

        # Iterating over all possible short diagonal moves:
        for sh_dir in short_dirs:
            short_cords = (cur_piece.row + sh_dir[0], cur_piece.col + sh_dir[1])
            if (
                TOP_BORDER <= short_cords[0] <= BOTTOM_BORDER
                and LEFT_BORDER <= short_cords[1] <= RIGHT_BORDER
            ):
                # Getting the piece on the short diagonal tile:
                short_tile = short_cords[0] * COLS + short_cords[1]
                short_piece = self.get_piece(short_tile)

                # Now if the tile is empty, we won't move there:
                if short_piece.is_empty():
                    continue

                # We only jump if the piece is of the opposite color:
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

                        # If the longer diagonal tile is empty, we can jump there:
                        if adv_piece.is_empty():
                            new_eaten = eaten + [(short_tile, short_piece.piece)]
                            all_moves.append(Move(org_tile, adv_tile, new_eaten))

                            # Now recursively checking for more jumps:
                            self._calculate_next_jumps(
                                org_tile, adv_tile, sh_dir, all_moves, new_eaten
                            )

    def calculate_next_moves(
        self, piece_tile: int, forced_jumping: bool = False
    ) -> list[Move]:
        # Lists of possible moves:
        short_moves = []
        jumping_moves = []

        # Getting the piece:
        piece = self.get_piece(piece_tile)
        if piece.is_empty():
            return short_moves

        # Direction is different for white and black pieces:
        row_dir = -1 if piece.is_white() else 1
        # short_dirs => directions for short diagonal moves:
        short_dirs = (
            [(row_dir, 1), (row_dir, -1), (-row_dir, 1), (-row_dir, -1)]
            if piece.is_queen()
            else [(row_dir, 1), (row_dir, -1)]
        )

        # Iterating over all possible short diagonal moves:
        for sh_dir in short_dirs:
            short_cords = (piece.row + sh_dir[0], piece.col + sh_dir[1])
            if (
                TOP_BORDER <= short_cords[0] <= BOTTOM_BORDER
                and LEFT_BORDER <= short_cords[1] <= RIGHT_BORDER
            ):
                # Getting the piece on the short diagonal tile:
                short_tile = short_cords[0] * COLS + short_cords[1]
                short_piece = self.get_piece(short_tile)

                # If the tile is empty, we can move there:
                if short_piece.is_empty():
                    short_moves.append(Move(piece_tile, short_tile))
                elif short_piece.is_opposite_color(piece):
                    # Since the tile is not empty, we can check
                    # the longer diagonal tile for potential jumps:
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

                        # If the longer diagonal tile is empty, we can jump there:
                        if adv_piece.is_empty():
                            # Adding a piece to eat:
                            eaten = [(short_tile, short_piece.piece)]
                            jumping_moves.append(Move(piece_tile, adv_tile, eaten))

                            # Now recursively checking for more jumps:
                            self._calculate_next_jumps(
                                piece_tile, adv_tile, sh_dir, jumping_moves, eaten
                            )

        # Depending on the forced_jumping flag, we return different moves:
        if forced_jumping:
            if len(jumping_moves) == 0:
                # Short if there are no jumps:
                return short_moves
            # Otherwise, we return only the jumping moves:
            return jumping_moves

        # This is the 'default' case, where we return combined moves:
        return jumping_moves + short_moves

    def get_all_piece_tiles(self, color: int) -> list[int]:
        # We will store the tiles of the pieces in this list:
        pieces = []
        for piece in self._board:
            # Only possible pieces are the ones that are not empty
            # and have the desired color:
            if not piece.is_empty() and piece.is_color(color):
                pieces.append(piece.row * COLS + piece.col)

        return pieces

    def calculate_all_turn_moves(
        self, color: int, forced_jumping: bool = False
    ) -> list[Move]:
        # We will get them by iterating over all pieces of the desired color
        # and accumulating their possible moves, in this list:
        all_turn_moves = []
        piece_tiles = self.get_all_piece_tiles(color)

        # Iterating over all pieces:
        for piece_tile in piece_tiles:
            all_turn_moves += self.calculate_next_moves(piece_tile, forced_jumping)

        # If there are forced jumps, we need to filter out the moves that are not jumps:
        if forced_jumping:
            filtered = list(
                filter(lambda mov: len(mov.eaten_tiles) > 0, all_turn_moves)
            )
            if len(filtered) > 0:
                all_turn_moves = filtered

        # Sorting moves by the number of eaten pieces
        # this might speed up the alpha-beta pruning algorithm:
        all_turn_moves.sort(key=lambda mov: len(mov.eaten_tiles), reverse=True)
        return all_turn_moves

    def make_move(self, move: Move):
        # We get data about the move:
        start_piece = self.get_piece(move.start_tile)
        target_piece = self.get_piece(move.target_tile)

        # Potential queen promotion:
        if target_piece.row == TOP_BORDER or target_piece.row == BOTTOM_BORDER:
            # promoted_to_queen() is not modifying the piece in place:
            target_piece.piece = start_piece.promoted_to_queen()

            # Increasing number of queens:
            if start_piece.is_white():
                self._white_queens += 1
            else:
                self._black_queens += 1
        else:
            # Moving the piece, that is not a queen:
            target_piece.piece = start_piece.piece
        # Removing the piece from the start tile:
        start_piece.piece = EMPTY_TILE

        # Removing eaten pieces:
        for eaten_tile, piece_type in move.eaten_tiles:
            eaten_piece = self.get_piece(eaten_tile)

            # Decreasing number of pieces depending on the type of the eaten piece:
            if eaten_piece.is_queen():
                if eaten_piece.is_white():
                    self._white_queens -= 1
                    # Mustn't forget to decrease the number of regular pieces:
                    self._whites_left -= 1
                else:
                    self._black_queens -= 1
                    self._blacks_left -= 1
            else:
                if eaten_piece.is_white():
                    self._whites_left -= 1
                else:
                    self._blacks_left -= 1

            # Making the eaten piece eaten:
            eaten_piece.piece = EMPTY_TILE

    def undo_move(self, move: Move):
        # Undo is inverse of make_move...
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
            # Now we bring back eaten piece type:
            eaten_piece.piece = piece_type

    def __str__(self) -> str:
        ans = ""
        for tile_number in range(ROWS * COLS):
            ans += str(self._board[tile_number])
        return ans

    def __repr__(self) -> str:
        return self.__str__()
