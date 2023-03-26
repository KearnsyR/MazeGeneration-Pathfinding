import pygame
from settings import *

class DisplayGrid:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
    
    def display_grid(self, grid):
        self.display_surface.fill(BACKGROUND_COLOUR)
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if(grid[x][y].border_side['North']):
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, (y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, BORDER_WIDTH))
                if(grid[x][y].border_side['South']):
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, (y * TILE_SIZE, (x + 1) * TILE_SIZE, TILE_SIZE, BORDER_WIDTH))
                if(grid[x][y].border_side['East']):
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, ((y + 1) * TILE_SIZE, x * TILE_SIZE, BORDER_WIDTH, TILE_SIZE))
                if(grid[x][y].border_side['West']):
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, (y * TILE_SIZE, x * TILE_SIZE, BORDER_WIDTH, TILE_SIZE))
        pygame.display.update()