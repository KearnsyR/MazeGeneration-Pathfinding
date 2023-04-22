import pygame
import heapq
import time
from settings import *
from queue import PriorityQueue, Queue
from display_grid import DisplayGrid

class Pathfinding:
    def __init__(self, grid, start_pos, end_pos, pathfinding_algorithm, grid_size, starting_coordinate, tile_size):
        self.grid = grid
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.pathfinding_algorithm = pathfinding_algorithm
        self.grid_size = grid_size
        self.starting_coordinate = starting_coordinate
        self.tile_size = tile_size
        self.renderGrid = DisplayGrid(self.grid_size, self.starting_coordinate, tile_size)

        self.pathfinding_algorithms = {
            'A*': self.solve_astar,
            'Dijkstras': self.solve_dijkstra,
            'Breadth-First Search': self.solve_bfs,
        }
    
    def find_path(self):
        start_time = time.time()
        self.pathfinding_algorithms[self.pathfinding_algorithm]()
        end_time = time.time()
        print(f"The current algorithm is {self.pathfinding_algorithm}")
        print(f"Pathfinding time taken: {end_time - start_time:.3f} seconds")

    def heuristic(self, curr_pos, end_pos):
        curr_x, curr_y = curr_pos
        end_x, end_y = end_pos
        return abs(curr_x - end_x) + abs(curr_y - end_y)

    def is_traversable(self, grid, curr_pos, neighbour_pos):
        opposite_sides = {'North': 'South', 'South': 'North', 'East': 'West', 'West': 'East'}
        if curr_pos[0] > neighbour_pos[0]:
            side = 'West'
        elif curr_pos[0] < neighbour_pos[0]:
            side = 'East'
        elif curr_pos[1] > neighbour_pos[1]:
            side = 'North'
        else:
            side = 'South'
        if grid[curr_pos[0]][curr_pos[1]].border_side[side] == False and grid[neighbour_pos[0]][neighbour_pos[1]].border_side[opposite_sides[side]] == False:
            return neighbour_pos
        else:
            return None

    def get_neighbours(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if y > 0 and self.grid[x][y-1].border_side['South'] == False:
                    self.grid[x][y].neighbours.append(self.is_traversable(self.grid, (x,y), (x,y-1)))
                if y < self.grid_size-1 and self.grid[x][y+1].border_side['North'] == False:
                    self.grid[x][y].neighbours.append(self.is_traversable(self.grid, (x,y), (x,y+1)))
                if x > 0 and self.grid[x-1][y].border_side['East'] == False:
                    self.grid[x][y].neighbours.append(self.is_traversable(self.grid, (x,y), (x-1,y)))
                if x < self.grid_size-1 and self.grid[x+1][y].border_side['West'] == False:
                    self.grid[x][y].neighbours.append(self.is_traversable(self.grid, (x,y), (x+1,y)))

    def path(self, origin, current, grid):
        while current in origin.keys():
            current = origin[current]
            if current != self.grid[self.start_pos[0]][self.start_pos[1]]:
                current.type = PATH
            else:
                return
            self.renderGrid.draw_squares(grid)

    def solve_dijkstra(self):
        count = 0
        open_set = []
        heapq.heappush(open_set, (0, count, self.grid[self.start_pos[0]][self.start_pos[1]]))
        origin = {}
        self.get_neighbours()
        self.grid[self.start_pos[0]][self.start_pos[1]].g_score = 0
        open_set_hash = {self.grid[self.start_pos[0]][self.start_pos[1]]}

        while open_set:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            current = heapq.heappop(open_set)[2]
            open_set_hash.remove(current)

            if current == self.grid[self.end_pos[0]][self.end_pos[1]]:
                self.path(origin, current, self.grid)
                return True

            for neighbour_coor in current.neighbours:
                temp_g_score = current.g_score + 1
                neighbour_tile = self.grid[neighbour_coor[0]][neighbour_coor[1]]
                if temp_g_score < neighbour_tile.g_score:
                    origin[neighbour_tile] = current
                    neighbour_tile.g_score = temp_g_score
                    if neighbour_tile not in open_set_hash: 
                        count += 1
                        heapq.heappush(open_set, (neighbour_tile.g_score, count, neighbour_tile))
                        open_set_hash.add(neighbour_tile)
                        if neighbour_tile != self.grid[self.end_pos[0]][self.end_pos[1]]:
                            neighbour_tile.type = OPEN

            if current != self.grid[self.start_pos[0]][self.start_pos[1]]:
                current.type = CLOSED
            self.renderGrid.draw_squares(self.grid)

        return False
    
    def solve_bfs(self):
        open_set = Queue()
        start_tile = self.grid[self.start_pos[0]][self.start_pos[1]]
        open_set.put(start_tile)
        origin = {start_tile: None}
        self.get_neighbours()
        open_set_hash = {start_tile}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            current = open_set.get()
            open_set_hash.remove(current)

            if current == self.grid[self.end_pos[0]][self.end_pos[1]]:
                self.path(origin, current, self.grid)
                return True

            if current.type == CLOSED and current != start_tile:
                continue

            for neighbour_coor in current.neighbours:
                neighbour_tile = self.grid[neighbour_coor[0]][neighbour_coor[1]]
                if neighbour_tile == current or neighbour_tile.type == CLOSED:
                    continue
                if neighbour_tile not in open_set_hash:
                    origin[neighbour_tile] = current
                    open_set.put(neighbour_tile)
                    open_set_hash.add(neighbour_tile)
                    if neighbour_tile != self.grid[self.end_pos[0]][self.end_pos[1]] and neighbour_tile != start_tile:
                        neighbour_tile.type = OPEN
                if neighbour_tile == self.grid[self.end_pos[0]][self.end_pos[1]]:
                    neighbour_tile.type = END

            if current != start_tile:
                current.type = CLOSED

            self.renderGrid.draw_squares(self.grid)

    def solve_astar(self):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, self.grid[self.start_pos[0]][self.start_pos[1]]))
        origin = {}
        self.get_neighbours()
        self.grid[self.start_pos[0]][self.start_pos[1]].g_score = 0
        self.grid[self.start_pos[0]][self.start_pos[1]].f_score = self.heuristic(self.start_pos, self.end_pos)
        open_set_hash = {self.grid[self.start_pos[0]][self.start_pos[1]]}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            current = open_set.get()[2]
            open_set_hash.remove(current)

            if current == self.grid[self.end_pos[0]][self.end_pos[1]]:
                self.path(origin, current, self.grid)
                return True

            for neighbour_coor in current.neighbours:
                temp_g_score = current.g_score + 1
                neighbour_tile = self.grid[neighbour_coor[0]][neighbour_coor[1]]
                if temp_g_score < neighbour_tile.g_score:
                    origin[neighbour_tile] = current
                    neighbour_tile.g_score = temp_g_score
                    neighbour_tile.f_score = temp_g_score + self.heuristic(neighbour_coor, self.end_pos)
                    if neighbour_tile not in open_set_hash: 
                        count += 1
                        open_set.put((neighbour_tile.f_score, count, neighbour_tile))
                        open_set_hash.add(neighbour_tile)
                        if neighbour_tile != self.grid[self.end_pos[0]][self.end_pos[1]]:
                            neighbour_tile.type = OPEN

            if current != self.grid[self.start_pos[0]][self.start_pos[1]]:
                current.type = CLOSED
            self.renderGrid.draw_squares(self.grid)

        return False
            
