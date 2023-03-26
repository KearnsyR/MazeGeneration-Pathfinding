import pygame, sys
from maze import Maze
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Procedurally Generated Maze and Pathfinding')
        self.clock = pygame.time.Clock()
        self.maze = Maze()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            self.maze.generate_maze()
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()