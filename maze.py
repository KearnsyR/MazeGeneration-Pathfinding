import random
import time
import pygame
from settings import *
from tile import Tile
from display_grid import DisplayGrid

class Maze:
    def __init__(self, maze_algorithm):
        self.grid = [[Tile(x, y) for y in range(GRID_SIZE)] for x in range(GRID_SIZE)]
        self.renderGrid = DisplayGrid()
        self.maze_algorithm = maze_algorithm
        self.start_side = random.choice(['North', 'South', 'East', 'West'])
        self.opposite_sides = {'North': 'South', 'South': 'North', 'East': 'West', 'West': 'East'}

        self.maze_algorithms = {
            'Recursive Backtracker': self.generate_recursive_backtracker,
            'Prim\'s Algorithm': self.generate_prim,
            'Kruskal\'s Algorithm': self.generate_kruskal,
        }

    def set_maze_algorithm(self, algorithm):
        self.maze_algorithm = algorithm

    def generate_maze(self):
        start_time = time.time()
        grid = self.maze_algorithms[self.maze_algorithm]()
        start_pos = self.get_pos(self.start_side)
        end_pos = self.get_pos(self.opposite_sides[self.start_side])
        self.renderGrid.display_grid(self.grid)
        end_time = time.time()
        print(f"The current algorithm is {self.maze_algorithm}")
        print(f"Maze Generation time taken: {end_time - start_time:.3f} seconds")
        return start_pos, end_pos, grid
    
    def get_pos(self, side):
        x = random.randint(0, GRID_SIZE-1)
        y = random.randint(0, GRID_SIZE-1)
        if side == 'North':
            self.grid[y][0].border_side['North'] = False
            return (y, 0)
        elif side == 'South':
            self.grid[y][GRID_SIZE-1].border_side['South'] = False
            return (y, GRID_SIZE-1)
        elif side == 'East':
            self.grid[GRID_SIZE-1][x].border_side['East'] = False
            return (GRID_SIZE-1, x)
        elif side == 'West':
            self.grid[0][x].border_side['West'] = False
            return (0, x)

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
    
    def generate_recursive_backtracker(self):
        self.renderGrid.display_grid(self.grid)
        tile_stack = [(random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))]
        visited_tile = set()
        
        while tile_stack:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
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
                tile_stack.append((neighbour_x, neighbour_y))
        return self.grid
    
    def generate_prim(self):
        self.renderGrid.display_grid(self.grid)

        visited = set()
        frontier = set()
        start_x, start_y = self.get_pos(self.start_side)
        visited.add((start_x, start_y))
        for neighbour_x, neighbour_y in self.get_unvisited_neighbours(start_x, start_y):
            frontier.add((neighbour_x, neighbour_y))

        while frontier:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            x, y = random.choice(list(frontier))
            frontier.remove((x, y))

            candidates = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            random.shuffle(candidates)
            for neighbour_x, neighbour_y in candidates:
                if (neighbour_x, neighbour_y) in visited:
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

                    visited.add((x, y))
                    for neighbour_x, neighbour_y in self.get_unvisited_neighbours(x, y):
                        if (neighbour_x, neighbour_y) not in visited:
                            frontier.add((neighbour_x, neighbour_y))

                    self.renderGrid.display_grid(self.grid)
                    break
            else:
                continue
        return self.grid
    
    def generate_kruskal(self):
        self.renderGrid.display_grid(self.grid)
        edges = []
        sets = [[(x,y)] for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if y > 0:
                    edges.append(((x,y), (x,y-1)))
                if x > 0:
                    edges.append(((x,y), (x-1,y)))
        random.shuffle(edges)

        for edge in edges:
            (x1,y1), (x2,y2) = edge
            set1 = None
            set2 = None
            for s in sets:
                if (x1,y1) in s:
                    set1 = s
                if (x2,y2) in s:
                    set2 = s
            if set1 != set2:
                if x1 == x2:
                    if y1 > y2:
                        self.grid[x1][y1].border_side['North'] = False
                        self.grid[x2][y2].border_side['South'] = False
                    else:
                        self.grid[x1][y1].border_side['South'] = False
                        self.grid[x2][y2].border_side['North'] = False
                else:
                    if x1 > x2:
                        self.grid[x1][y1].border_side['West'] = False
                        self.grid[x2][y2].border_side['East'] = False
                    else:
                        self.grid[x1][y1].border_side['East'] = False
                        self.grid[x2][y2].border_side['West'] = False
                set1.extend(set2)
                sets.remove(set2)

            self.renderGrid.display_grid(self.grid)

        return self.grid