import random
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
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, (STARTING_COORDINATE + x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE + 5, BORDER_WIDTH))
                if(grid[x][y].border_side['South']):
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, (STARTING_COORDINATE + x * TILE_SIZE, (y + 1) * TILE_SIZE, TILE_SIZE + 5, BORDER_WIDTH))
                if(grid[x][y].border_side['East']):
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, (STARTING_COORDINATE + (x + 1) * TILE_SIZE, y * TILE_SIZE, BORDER_WIDTH, TILE_SIZE + 5))
                if(grid[x][y].border_side['West']):
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, (STARTING_COORDINATE + x * TILE_SIZE, y * TILE_SIZE, BORDER_WIDTH, TILE_SIZE + 5))
        pygame.display.update()