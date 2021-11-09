import random

from consts import CELLSIZE

class Spawner:
    current_pos = (0, 0)

    def __init__(self, max_height, max_weight) -> None:
        self.max_height = max_height
        self.max_weight = max_weight
        self.create_new_pos()
        print(self.current_pos)

    def _get_rundom_pos(self):
        x_pos = random.randrange(0, self.max_height, CELLSIZE)
        y_pos = random.randrange(0, self.max_weight, CELLSIZE)
        return x_pos, y_pos

    def create_new_pos(self):
        x_pos, y_pos = self._get_rundom_pos()
        while self.current_pos == (x_pos, y_pos):
            x_pos, y_pos = self._get_rundom_pos()

        self.current_pos = (x_pos, y_pos)
