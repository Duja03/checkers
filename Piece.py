from Constants import *


class Piece(object):
    # Static methods:
    def is_piece_queen(piece) -> bool:
        return bool(piece & QUEEN)

    def is_piece_empty(piece) -> bool:
        return piece == EMPTY_TILE

    def is_piece_white(piece) -> bool:
        return bool(piece & WHITE_COLOR)

    def is_piece_black(piece) -> bool:
        return bool(piece & BLACK_COLOR)

    def __init__(self, row: int, col: int, piece: int) -> None:
        self._row = row
        self._col = col
        self._piece = piece

    def __str__(self) -> str:
        if self.is_queen():
            return " W " if self.is_white() else " B "
        elif self.is_empty():
            return " . "
        else:
            return " w " if self.is_white() else " b "

    @property
    def row(self) -> int:
        return self._row

    @row.setter
    def row(self, row: int) -> None:
        self._row = row

    @property
    def col(self) -> int:
        return self._col

    @col.setter
    def col(self, col: int) -> None:
        self._col = col

    @property
    def piece(self) -> int:
        return self._piece

    @piece.setter
    def piece(self, piece: int) -> None:
        self._piece = piece

    def is_queen(self) -> bool:
        return bool(self._piece & QUEEN)

    def is_empty(self) -> bool:
        return self._piece == EMPTY_TILE

    def is_white(self) -> bool:
        return bool(self._piece & WHITE_COLOR)

    def is_black(self) -> bool:
        return bool(self._piece & BLACK_COLOR)

    def is_color(self, color) -> bool:
        return bool(self._piece & color)

    def is_opposite_color(self, piece) -> bool:
        return self.is_white() != piece.is_white()

    def get_color(self):
        if self.is_white():
            return WHITE_COLOR
        elif self.is_black():
            return BLACK_COLOR
        else:
            return EMPTY_TILE

    def promote(self) -> None:
        if self.is_white():
            self._piece = WHITE_QUEEN
        elif self.is_black():
            self._piece = BLACK_QUEEN

    def demote(self) -> None:
        if self.is_white():
            self._piece = WHITE_PIECE
        elif self.is_black():
            self._piece = BLACK_PIECE

    def promoted_to_queen(self) -> int:
        if self.is_white():
            return WHITE_QUEEN
        elif self.is_black():
            return BLACK_QUEEN
        else:
            return EMPTY_TILE

    def demoted_to_piece(self) -> int:
        if self.is_white():
            return WHITE_PIECE
        elif self.is_black():
            return BLACK_PIECE
        else:
            return EMPTY_TILE
