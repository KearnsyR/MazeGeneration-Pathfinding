import random
import pygame
from render import Render
from tile import Tile

class MazeGeneration:
    def __init__(self, grid_size, screen, screen_width):
        self.tile_colour = (255, 255, 255)
        self.grid_size = grid_size
        self.grid = [[Tile(x, y, screen_width, self.grid_size) for y in range(self.grid_size)] for x in range(self.grid_size)]
        self.update = Render(screen, self.grid, self.grid_size, self.tile_colour)

    def get_pos(self, side):
        x = random.randint(0, self.grid_size-1)
        y = random.randint(0, self.grid_size-1)
        if side == 'North':
            self.grid[0][y].border_side['North'] = False
            return (0, y)
        elif side == 'South':
            self.grid[self.grid_size-1][y].border_side['South'] = False
            return (self.grid_size-1, y)
        elif side == 'East':
            self.grid[x][self.grid_size-1].border_side['East'] = False
            return (x, self.grid_size-1)
        elif side == 'West':
            self.grid[x][0].border_side['West'] = False
            return (x, 0)

    def get_unvisited_neighbours(self, x, y):
        neighbours = []
        if x > 0 and all(self.grid[x-1][y].border_side.values()):
            neighbours.append((x-1, y))
        if x < self.grid_size - 1 and all(self.grid[x+1][y].border_side.values()):
            neighbours.append((x+1, y))
        if y > 0 and all(self.grid[x][y-1].border_side.values()):
            neighbours.append((x, y-1))
        if y < self.grid_size - 1 and all(self.grid[x][y+1].border_side.values()):
            neighbours.append((x, y+1))
        return neighbours
    
    def generate_maze(self):
        tile_stack = [(random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1))]
        visited_tile = set()
        start_side = random.choice(['North', 'South', 'East', 'West'])
        opposite_sides = {'North': 'South', 'South': 'North', 'East': 'West', 'West': 'East'}

        while tile_stack:
            x, y = tile_stack.pop()
            visited_tile.add((x, y))
            unvisited_neighbours = [neighbour for neighbour in self.get_unvisited_neighbours(x, y) if neighbour not in visited_tile]
            if unvisited_neighbours:
                tile_stack.append((x, y))
                neighbour_x, neighbour_y = random.choice(unvisited_neighbours)
                if neighbour_x < x:
                    self.grid[x][y].border_side['North'] = False
                    self.grid[neighbour_x][neighbour_y].border_side['South'] = False
                elif neighbour_x > x:
                    self.grid[x][y].border_side['South'] = False
                    self.grid[neighbour_x][neighbour_y].border_side['North'] = False
                elif neighbour_y < y:
                    self.grid[x][y].border_side['East'] = False
                    self.grid[neighbour_x][neighbour_y].border_side['West'] = False
                else:
                    self.grid[x][y].border_side['West'] = False
                    self.grid[neighbour_x][neighbour_y].border_side['East'] = False
                
                self.update.update_screen(self.grid)
                pygame.time.wait(50)
                tile_stack.append((neighbour_x, neighbour_y))

        self.get_pos(start_side)
        self.get_pos(opposite_sides[start_side])
        return self.grid

        