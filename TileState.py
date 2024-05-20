from enum import Enum


class TileState(Enum):
    EMPTY = 0
    WHITE_COLOR = 1
    BLACK_COLOR = 2

    QUEEN = 4
    WHITE_PIECE = WHITE_COLOR
    BLACK_PIECE = BLACK_COLOR
    WHITE_QUEEN = WHITE_COLOR | QUEEN
    BLACK_QUEEN = BLACK_COLOR | QUEEN

    def is_empty(self) -> bool:
        return self == TileState.EMPTY

    def is_white(self) -> bool:
        return bool(self.value & TileState.WHITE_COLOR.value)

    def is_black(self) -> bool:
        return bool(self.value & TileState.BLACK_COLOR.value)

    def is_queen(self) -> bool:
        return bool(self.value & TileState.QUEEN.value)

    def get_color(self):
        if self.is_white():
            return TileState.WHITE_COLOR
        elif self.is_black():
            return TileState.BLACK_COLOR
        else:
            return TileState.EMPTY

    def promote_to_queen(self):
        if self.is_white():
            return TileState.WHITE_QUEEN
        elif self.is_black():
            return TileState.BLACK_QUEEN
        else:
            return TileState.EMPTY

    def demote_to_piece(self):
        if self.is_white():
            return TileState.WHITE_PIECE
        elif self.is_black():
            return TileState.BLACK_PIECE
        else:
            return TileState.EMPTY

    def opposite_color(self):
        if self.is_white():
            return TileState.BLACK_COLOR
        elif self.is_black():
            return TileState.WHITE_COLOR
        else:
            return TileState.EMPTY

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
