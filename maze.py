import random

import pygame
from settings import *
from tile import Tile
from display_grid import DisplayGrid

class Maze:
    def __init__(self):
        self.grid = [[Tile(x, y) for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
        self.renderGrid = DisplayGrid()

    def get_unvisited_neighbours(self, x, y):
        neighbours = []
        if y > 0 and all(self.grid[x][y-1].border_side.values()): # Gets neighbour to the North
            neighbours.append((x, y-1))
        if y < GRID_SIZE - 1 and all(self.grid[x][y+1].border_side.values()): # Gets neighbour to the South
            neighbours.append((x, y+1))
        if x < GRID_SIZE - 1 and all(self.grid[x+1][y].border_side.values()): # Gets neighbour to East
            neighbours.append((x+1, y))
        if x > 0 and all(self.grid[x-1][y].border_side.values()): # Gets neighbour to West
            neighbours.append((x-1, y))
        return neighbours
    
    def generate_maze(self):
        self.renderGrid.display_grid(self.grid)
        tile_stack = [(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))]
        visited_tile = set()
        
        while tile_stack:
            x, y = tile_stack.pop()
            visited_tile.add((x, y))
            unvisited_neighbours = [neighbour for neighbour in self.get_unvisited_neighbours(x, y) if neighbour not in visited_tile]
            if unvisited_neighbours:
                tile_stack.append((x, y))
                neighbour_x, neighbour_y = random.choice(unvisited_neighbours)
                if neighbour_x < x:
                    self.grid[x][y].border_side['West'] = False
                    self.grid[neighbour_x][neighbour_y].border_side['East'] = False
                elif neighbour_x > x:
                    self.grid[x][y].border_side['East'] = False
                    self.grid[neighbour_x][neighbour_y].border_side['West'] = False
                elif neighbour_y < y:
                    self.grid[x][y].border_side['North'] = False
                    self.grid[neighbour_x][neighbour_y].border_side['South'] = False
                elif neighbour_y > y:
                    self.grid[x][y].border_side['South'] = False
                    self.grid[neighbour_x][neighbour_y].border_side['North'] = False
                
                self.renderGrid.display_grid(self.grid)
                pygame.time.wait(50)
                tile_stack.append((neighbour_x, neighbour_y))