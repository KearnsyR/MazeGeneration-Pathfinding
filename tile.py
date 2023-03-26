import pygame

class Tile:
    def __init__(self, x, y, screen_width, grid_size):
        self.border_side = {
            'North': True,
            'East': True,
            'South': True,
            'West': True
        }
        self.x = x
        self.y = y
        self.total_border_width = 10
        self.border_width = self.total_border_width // grid_size
        self.border_colour = (0, 0, 0)
        self.tile_size = (screen_width - self.total_border_width - 10) // grid_size
    
    def draw_tile(self, screen):
        if(self.border_side['North']):
            pygame.draw.rect(screen, self.border_colour, (self.y * self.tile_size + 10, self.x * self.tile_size + 10, self.tile_size, self.border_width))
        if(self.border_side['East']):
            pygame.draw.rect(screen, self.border_colour, ((self.y + 1) * self.tile_size - self.border_width + 10, self.x * self.tile_size + 10, self.border_width, self.tile_size))
        if(self.border_side['South']):
            pygame.draw.rect(screen, self.border_colour, (self.y * self.tile_size + 10, (self.x + 1) * self.tile_size - self.border_width + 10, self.tile_size, self.border_width))
        if(self.border_side['West']):
            pygame.draw.rect(screen, self.border_colour, (self.y * self.tile_size + 10, self.x * self.tile_size + 10, self.border_width, self.tile_size))