class Move(object):
    def __init__(self, start_cords: tuple, target_cords: tuple, eaten_cords=[]) -> None:
        self._start_cords = start_cords
        self._target_cords = target_cords
        self._eaten_cords = eaten_cords

    def __str__(self) -> str:
        return f"{self.start_cords} => {self.target_cords}: {self.eaten_cords}"

    def __repr__(self) -> str:
        return self.__str__()

    def add_eaten_piece(self, cords: tuple) -> None:
        self._eaten_cords.append(cords)

    @property
    def start_cords(self):
        return self._start_cords

    @start_cords.setter
    def start_cords(self, start_cords: tuple):
        self._start_cords = start_cords

    @property
    def target_cords(self):
        return self._target_cords

    @target_cords.setter
    def target_cords(self, target_cords: tuple):
        self._target_cords = target_cords

    @property
    def eaten_cords(self):
        return self._eaten_cords

    @eaten_cords.setter
    def eaten_cords(self, eaten_cords: list):
        self._eaten_cords = eaten_cords
