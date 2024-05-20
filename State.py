from TileState import TileState


class State(object):
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

    def calculate_next_jumps(self, piece_cords: tuple, is_queen: bool, dir: tuple):
        piece = self.get_piece(piece_cords)
        short_dirs = (
            [(dir[0], dir[1]), (dir[0], -dir[1]), (-dir[0], dir[1])]
            if is_queen
            else [(dir[0], dir[1]), (dir[0], -dir[1])]
        )

        for sh_dir in short_dirs:
            short_cords = (piece_cords[0] + sh_dir[0], piece_cords[1] + sh_dir[1])
            if (
                State.TOP_BORDER <= short_cords[0] <= State.BOTTOM_BORDER
                and State.LEFT_BORDER <= short_cords[1] <= State.RIGHT_BORDER
            ):
                short_piece = self.get_piece(short_cords)
                if short_piece == TileState.EMPTY:
                    continue
                if short_piece.get_color() == piece.opposite_color():
                    adv_cords = (
                        short_cords[0] + sh_dir[0],
                        short_cords[1] + sh_dir[1],
                    )
                    if (
                        State.TOP_BORDER <= adv_cords[0] <= State.BOTTOM_BORDER
                        and State.LEFT_BORDER <= adv_cords[1] <= State.RIGHT_BORDER
                    ):
                        adv_piece = self.get_piece(adv_cords)
                        if adv_piece == TileState.EMPTY:
                            print(adv_cords)
                            self.calculate_next_jumps(adv_cords, is_queen, sh_dir)

                if short_piece == TileState.EMPTY:
                    print(short_cords)
                elif short_piece.opposite_color():
                    adv_cords = (
                        short_cords[0] + sh_dir[0],
                        short_cords[1] + sh_dir[1],
                    )
                    if (
                        State.TOP_BORDER == adv_cords[0]
                        or State.BOTTOM_BORDER == adv_cords[0]
                    ) and State.LEFT_BORDER <= adv_cords[1] <= State.RIGHT_BORDER:
                        # Promote to queen:
                        self.get_piece(adv_cords).promote_to_queen()
                    if (
                        State.TOP_BORDER <= adv_cords[0] <= State.BOTTOM_BORDER
                        and State.LEFT_BORDER <= adv_cords[1] <= State.RIGHT_BORDER
                    ):
                        adv_piece = self.get_piece(adv_cords)
                        if adv_piece == TileState.EMPTY:
                            print(adv_cords)
                            self.calculate_next_jumps(adv_cords, is_queen, sh_dir)

    def calculate_next_moves(self, piece_cords: tuple):
        # Basic data:
        piece = self.get_piece(piece_cords)
        if piece == TileState.EMPTY:
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
                State.TOP_BORDER <= short_cords[0] <= State.BOTTOM_BORDER
                and State.LEFT_BORDER <= short_cords[1] <= State.RIGHT_BORDER
            ):
                short_piece = self.get_piece(short_cords)
                if short_piece == TileState.EMPTY:
                    print(short_cords)
                elif short_piece.get_color() == piece.opposite_color():
                    adv_cords = (
                        short_cords[0] + sh_dir[0],
                        short_cords[1] + sh_dir[1],
                    )
                    if (
                        State.TOP_BORDER <= adv_cords[0] <= State.BOTTOM_BORDER
                        and State.LEFT_BORDER <= adv_cords[1] <= State.RIGHT_BORDER
                    ):
                        adv_piece = self.get_piece(adv_cords)
                        if adv_piece == TileState.EMPTY:
                            print(adv_cords)
                            self.calculate_next_jumps(adv_cords, is_queen, sh_dir)

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
    state = State()
    print(state)
    state.calculate_next_moves((0, 0))
