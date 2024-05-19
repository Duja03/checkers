class State(object):
    # Static variables:
    EMPTY = 0
    QUEEN = 4
    WHITE_PIECE = 1
    BLACK_PIECE = 2
    WHITE_QUEEN = WHITE_PIECE | QUEEN
    BLACK_QUEEN = BLACK_PIECE | QUEEN

    def __init__(self):
        self._board = []
        self._next_to_move = State.WHITE_PIECE

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board: list):
        self._board = board

    def create_new_board(self):
        self._board = [[State.EMPTY for i in range(8)] for j in range(8)]
        # Set the initial state of the board:
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self._board[row][col] = State.BLACK_PIECE
                    elif row > 4:
                        self._board[row][col] = State.WHITE_PIECE

    def __str__(self):
        for row in self._board:
            print(row)

    def __eq__(self, other):
        return self._board == other._board

    def __hash__(self):
        return hash(self._board)
