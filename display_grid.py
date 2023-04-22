import pygame
from settings import *

class DisplayGrid:
    def __init__(self, grid_size, starting_coordinate, tile_size):
        self.display_surface = pygame.display.get_surface()
        self.grid_size = grid_size
        self.starting_coordinate = starting_coordinate
        self.tile_size = tile_size
    
    def display_grid(self, grid):
        self.display_surface.fill(BACKGROUND_COLOUR)
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if(grid[x][y].border_side['North']):
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, (self.starting_coordinate + x * self.tile_size, y * self.tile_size, self.tile_size + 5, BORDER_WIDTH))
                if(grid[x][y].border_side['South']):
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, (self.starting_coordinate + x * self.tile_size, (y + 1) * self.tile_size, self.tile_size + 5, BORDER_WIDTH))
                if(grid[x][y].border_side['East']):
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, (self.starting_coordinate + (x + 1) * self.tile_size, y * self.tile_size, BORDER_WIDTH, self.tile_size + 5))
                if(grid[x][y].border_side['West']):
                    pygame.draw.rect(self.display_surface, BORDER_COLOUR, (self.starting_coordinate + x * self.tile_size, y * self.tile_size, BORDER_WIDTH, self.tile_size + 5))
        pygame.display.update()
        # pygame.time.wait(50)
    
    def draw_squares(self, grid):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if(grid[x][y].type == OPEN):
                    pygame.draw.rect(self.display_surface, OPEN, (self.starting_coordinate + BORDER_WIDTH + x * self.tile_size, y * self.tile_size + BORDER_WIDTH, self.tile_size - BORDER_WIDTH, self.tile_size - BORDER_WIDTH))
                elif(grid[x][y].type == CLOSED):
                    pygame.draw.rect(self.display_surface, CLOSED, (self.starting_coordinate + BORDER_WIDTH + x * self.tile_size, y * self.tile_size + BORDER_WIDTH, self.tile_size - BORDER_WIDTH, self.tile_size - BORDER_WIDTH))
                elif(grid[x][y].type == PATH):
                    pygame.draw.rect(self.display_surface, PATH, (self.starting_coordinate + BORDER_WIDTH + x * self.tile_size, y * self.tile_size + BORDER_WIDTH, self.tile_size - BORDER_WIDTH, self.tile_size - BORDER_WIDTH))
                elif(grid[x][y].type == START):
                    pygame.draw.rect(self.display_surface, START, (self.starting_coordinate + BORDER_WIDTH + x * self.tile_size, y * self.tile_size + BORDER_WIDTH, self.tile_size - BORDER_WIDTH, self.tile_size - BORDER_WIDTH))
                elif(grid[x][y].type == END):
                    pygame.draw.rect(self.display_surface, END, (self.starting_coordinate + BORDER_WIDTH + x * self.tile_size, y * self.tile_size + BORDER_WIDTH, self.tile_size - BORDER_WIDTH, self.tile_size - BORDER_WIDTH))
        pygame.display.update()
        # pygame.time.wait(50)