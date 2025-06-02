from enum import Enum

class Direction(Enum):
    UP = (0, -20)
    DOWN = (0, 20)
    LEFT = (-20, 0)
    RIGHT = (20, 0)