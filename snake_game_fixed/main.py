import pygame
from core.game import Game
from core.direction import Direction

pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
FPS = 10

game = Game(screen)
MOVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(MOVE_EVENT, 150)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.snake.set_direction(Direction.UP)
            elif event.key == pygame.K_DOWN:
                game.snake.set_direction(Direction.DOWN)
            elif event.key == pygame.K_LEFT:
                game.snake.set_direction(Direction.LEFT)
            elif event.key == pygame.K_RIGHT:
                game.snake.set_direction(Direction.RIGHT)
        elif event.type == MOVE_EVENT:
            game.snake.move()
            if not game.update():
                print(f"Game Over! Score: {game.score}")
                running = False

    game.draw()
    clock.tick(FPS)
pygame.quit()