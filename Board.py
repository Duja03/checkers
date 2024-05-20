from Move import Move
from TileState import TileState


class Board(object):
    # Static variables:
    ROWS = 8
    COLS = 8

    LEFT_BORDER = 0
    RIGHT_BORDER = COLS - 1
    TOP_BORDER = 0
    BOTTOM_BORDER = ROWS - 1

    def __init__(self):
        self._board = []
        self._whites_left = 12
        self._blacks_left = 12
        self._white_queens = 0
        self._black_queens = 0

        self.create_new_board()

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board: list):
        self._board = board

    def create_new_board(self):
        self._board = [[TileState.EMPTY for i in range(8)] for j in range(8)]
        # Set the initial state of the board:
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self._board[row][col] = TileState.BLACK_PIECE
                    elif row > 4:
                        self._board[row][col] = TileState.WHITE_PIECE

    def get_piece(self, cords: tuple) -> TileState:
        return self._board[cords[0]][cords[1]]

    def set_piece(self, cords: tuple, type: TileState) -> None:
        self._board[cords[0]][cords[1]] = type

    def _calculate_next_jumps(
        self,
        org_cords: tuple,
        piece_cords: tuple,
        dir: tuple,
        all_turn_moves: list,
        eaten: list,
    ):
        piece = self.get_piece(org_cords)
        is_queen = piece.is_queen()
        short_dirs = (
            [(dir[0], dir[1]), (dir[0], -dir[1]), (-dir[0], dir[1])]
            if is_queen
            else [(dir[0], dir[1]), (dir[0], -dir[1])]
        )

        for sh_dir in short_dirs:
            short_cords = (piece_cords[0] + sh_dir[0], piece_cords[1] + sh_dir[1])
            if (
                Board.TOP_BORDER <= short_cords[0] <= Board.BOTTOM_BORDER
                and Board.LEFT_BORDER <= short_cords[1] <= Board.RIGHT_BORDER
            ):
                short_piece = self.get_piece(short_cords)

                if short_piece.is_empty():
                    continue
                if short_piece.get_color() == piece.opposite_color():
                    adv_cords = (
                        piece_cords[0] + 2 * sh_dir[0],
                        piece_cords[1] + 2 * sh_dir[1],
                    )
                    if (
                        Board.TOP_BORDER <= adv_cords[0] <= Board.BOTTOM_BORDER
                        and Board.LEFT_BORDER <= adv_cords[1] <= Board.RIGHT_BORDER
                    ):
                        adv_piece = self.get_piece(adv_cords)
                        if adv_piece.is_empty():
                            new_eaten = eaten + [
                                (short_cords[0], short_cords[1], short_piece)
                            ]
                            all_turn_moves.append(Move(org_cords, adv_cords, new_eaten))
                            self._calculate_next_jumps(
                                org_cords, adv_cords, sh_dir, all_turn_moves, new_eaten
                            )

    def calculate_next_moves(self, piece_cords: tuple, all_turn_moves: list):
        # Basic data:
        piece = self.get_piece(piece_cords)
        if piece.is_empty():
            return

        is_queen = piece.is_queen()
        row_dir = -1 if piece == TileState.WHITE_PIECE else 1
        short_dirs = (
            [(row_dir, 1), (row_dir, -1), (-row_dir, 1), (-row_dir, -1)]
            if is_queen
            else [(row_dir, 1), (row_dir, -1)]
        )

        for sh_dir in short_dirs:
            short_cords = (piece_cords[0] + sh_dir[0], piece_cords[1] + sh_dir[1])
            if (
                Board.TOP_BORDER <= short_cords[0] <= Board.BOTTOM_BORDER
                and Board.LEFT_BORDER <= short_cords[1] <= Board.RIGHT_BORDER
            ):
                short_piece = self.get_piece(short_cords)
                if short_piece.is_empty():
                    all_turn_moves.append(Move(piece_cords, short_cords))
                elif short_piece.get_color() == piece.opposite_color():
                    adv_cords = (
                        short_cords[0] + sh_dir[0],
                        short_cords[1] + sh_dir[1],
                    )
                    if (
                        Board.TOP_BORDER <= adv_cords[0] <= Board.BOTTOM_BORDER
                        and Board.LEFT_BORDER <= adv_cords[1] <= Board.RIGHT_BORDER
                    ):
                        adv_piece = self.get_piece(adv_cords)
                        if adv_piece.is_empty():
                            eaten = [(short_cords[0], short_cords[1], short_piece)]
                            all_turn_moves.append(Move(piece_cords, adv_cords, eaten))
                            self._calculate_next_jumps(
                                piece_cords, adv_cords, sh_dir, all_turn_moves, eaten
                            )

    def get_all_pieces(self, color: TileState) -> list:
        """
        Returns a list of all cordinates of pieces of the given color.
        """
        assert color == TileState.WHITE_COLOR or color == TileState.BLACK_COLOR

        pieces = []
        for row in range(Board.ROWS):
            for col in range(Board.COLS):
                piece = self.get_piece((row, col))
                if not piece.is_empty() and piece.get_color() == color:
                    pieces.append((row, col))
        return pieces

    def calculate_all_turn_moves(self, color: TileState):
        assert color == TileState.WHITE_COLOR or color == TileState.BLACK_COLOR
        all_turn_moves = []
        pieces = self._get_all_pieces(color)
        for piece in pieces:
            self.calculate_next_moves(piece, all_turn_moves)
        return all_turn_moves

    def make_move(self, move: Move):
        start_cords = move.start_cords
        target_cords = move.target_cords
        eaten_cords = move.eaten_cords
        # Potential queen promotion:
        start_piece = self.get_piece(start_cords)
        if (
            target_cords[0] == Board.TOP_BORDER
            or target_cords[0] == Board.BOTTOM_BORDER
        ):
            self.set_piece(target_cords, start_piece.promote_to_queen())
            if start_piece.is_white():
                self._white_queens += 1
            else:
                self._black_queens += 1
        else:
            self.set_piece(target_cords, start_piece)

        self.set_piece(start_cords, TileState.EMPTY)
        # Removing eaten pieces:
        for cords in eaten_cords:
            eaten_piece = cords[2]
            is_queen = eaten_piece.is_queen()
            # Decreasing number of pieces:
            if is_queen:
                if eaten_piece.is_white():
                    self._white_queens -= 1
                else:
                    self._black_queens -= 1
            else:
                if eaten_piece.is_white():
                    self._whites_left -= 1
                else:
                    self._blacks_left -= 1

            self.set_piece((cords[0], cords[1]), TileState.EMPTY)

    def undo_move(self, move: Move):
        start_cords = move.start_cords
        target_cords = move.target_cords
        eaten_cords = move.eaten_cords
        # Potential queen demotion:
        end_piece = self.get_piece(target_cords)
        if (
            target_cords[0] == Board.TOP_BORDER
            or target_cords[0] == Board.BOTTOM_BORDER
        ):
            if end_piece.is_white():
                self._white_queens -= 1
            else:
                self._black_queens -= 1
            self.set_piece(start_cords, end_piece.demote_to_piece())
        else:
            self.set_piece(start_cords, end_piece)

        self.set_piece(target_cords, TileState.EMPTY)
        # Adding eaten pieces:
        for cords in eaten_cords:
            eaten_piece = cords[2]
            is_queen = eaten_piece.is_queen()
            # Increase number of pieces:
            if is_queen:
                if eaten_piece.is_white():
                    self._white_queens += 1
                else:
                    self._black_queens += 1
            else:
                if eaten_piece.is_white():
                    self._whites_left += 1
                else:
                    self._blacks_left += 1

            self.set_piece((cords[0], cords[1]), cords[2])

    def print_state(self):
        print(f"W: {self._whites_left}, B: {self._blacks_left}, WQ: {self._white_queens}, BQ: {self._black_queens}")

    def __str__(self):
        ans = ""
        row_num = 0
        for row in self._board:
            ans += (str(row) + "\n") if row_num != 7 else str(row)
            row_num += 1
        return ans

    def __eq__(self, other):
        return self._board == other._board

    def __hash__(self):
        return hash(self._board)


if __name__ == "__main__":
    state = Board()
    print(state.calculate_all_turn_moves(TileState.WHITE_COLOR))
    print("\n", state, "\n")
    state.make_move(Move((5, 2), (3, 4), [(4, 3, TileState.BLACK_QUEEN)]))
    print(state, "\n")
    state.undo_move(Move((5, 2), (3, 4), [(4, 3, TileState.BLACK_QUEEN)]))
    print(state)
