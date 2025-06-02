import pygame

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def render(self, snake, food):
        self.screen.fill((0, 0, 0))
        for segment in snake.body:
            pygame.draw.rect(self.screen, (0, 255, 0), (*segment, 20, 20))
        pygame.draw.rect(self.screen, (255, 0, 0), (*food.position, 20, 20))
        pygame.display.flip()