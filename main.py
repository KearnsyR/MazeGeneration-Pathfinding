import pygame
from maze_generation import MazeGeneration

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 500
        self.screen_height = 500
        self.grid_size = 10
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

    def run(self):
        maze = MazeGeneration(self.grid_size, self.screen, self.screen_width)
        maze.generate_maze()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
