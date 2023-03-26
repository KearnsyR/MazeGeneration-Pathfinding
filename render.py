import pygame

class Render:
    def __init__(self, screen, grid, grid_size, tile_colour):
        self.screen = screen
        self.grid = grid
        self.grid_size = grid_size
        self.tile_colour = tile_colour

    def update_screen(self, grid):
        self.screen.fill(self.tile_colour)
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                grid[x][y].draw_tile(self.screen)
        pygame.display.flip()