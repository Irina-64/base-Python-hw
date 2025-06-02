from core.direction import Direction

class Snake:
    def __init__(self):
        self.body = [(100, 100)]
        self.direction = Direction.RIGHT

    def set_direction(self, new_direction):
        dx, dy = self.direction.value
        ndx, ndy = new_direction.value
        if (dx + ndx, dy + ndy) != (0, 0):
            self.direction = new_direction

    def move(self):
        x, y = self.body[0]
        dx, dy = self.direction.value
        new_head = (x + dx, y + dy)
        self.body.insert(0, new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self):
        head = self.body[0]
        return (
            head in self.body[1:] or
            not (0 <= head[0] < 600 and 0 <= head[1] < 400)
        )