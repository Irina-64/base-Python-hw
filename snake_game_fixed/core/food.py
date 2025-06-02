import random

class Food:
    def __init__(self):
        self.position = self._random_position()

    def _random_position(self):
        x = random.randint(0, 29) * 20
        y = random.randint(0, 19) * 20
        return (x, y)

    def relocate(self):
        self.position = self._random_position()