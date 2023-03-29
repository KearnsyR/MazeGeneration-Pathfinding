import math
from settings import *
from queue import PriorityQueue

def heuristic(curr_pos, end_pos):
    curr_x, curr_y = curr_pos
    end_x, end_y = end_pos
    return abs(curr_x - end_x) + abs(curr_y, end_y)

def is_traversable(grid, curr_pos, neighbour_pos):
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

def get_neighbours(grid):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            neighbours = []
            if y > 0 and grid[x][y-1].border_side['South'] == False:
                neighbours.append(is_traversable(grid, (x,y), (x,y-1)))
            if y < GRID_SIZE-1 and grid[x][y+1].border_side['North'] == False:
                neighbours.append(is_traversable(grid, (x,y), (x,y+1)))
            if x > 0 and grid[x-1][y].border_side['East'] == False:
                neighbours.append(is_traversable(grid, (x,y), (x-1,y)))
            if x < GRID_SIZE-1 and grid[x+1][y].border_side['West'] == False:
                neighbours.append(is_traversable(grid, (x,y), (x+1,y)))
            grid[x][y].neighbours = neighbours

