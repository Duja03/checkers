class Move(object):
    def __init__(
        self,
        start_tile: int,
        target_tile: int,
        eaten_tiles: list[tuple[int, int]] = [],
    ) -> None:
        self._start_tile: int = start_tile
        self._target_tile: int = target_tile
        self._eaten_tiles: list[tuple[int, int]] = eaten_tiles

    def __str__(self) -> str:
        return f"{self._start_tile} => {self._target_tile}: {self._eaten_tiles}"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def start_tile(self):
        return self._start_tile

    @start_tile.setter
    def start_tile(self, start_tile: tuple):
        self._start_tile = start_tile

    @property
    def target_tile(self):
        return self._target_tile

    @target_tile.setter
    def target_tile(self, target_tile: tuple):
        self._target_tile = target_tile

    @property
    def eaten_tiles(self):
        return self._eaten_tiles

    @eaten_tiles.setter
    def eaten_tiles(self, eaten_tiles: list):
        self._eaten_tiles = eaten_tiles
