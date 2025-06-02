from core.snake import Snake
from core.food import Food
from core.renderer import Renderer

class Game:
    def __init__(self, screen):
        self.snake = Snake()
        self.food = Food()
        self.renderer = Renderer(screen)
        self.score = 0

    def update(self):
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.relocate()
            self.score += 1
        if self.snake.check_collision():
            return False
        return True

    def draw(self):
        self.renderer.render(self.snake, self.food)