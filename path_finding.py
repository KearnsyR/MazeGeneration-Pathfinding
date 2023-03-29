import math
import pygame
from settings import *
from queue import PriorityQueue
from display_grid import DisplayGrid

def heuristic(curr_pos, end_pos):
    curr_x, curr_y = curr_pos
    end_x, end_y = end_pos
    return abs(curr_x - end_x) + abs(curr_y - end_y)

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
            if y > 0 and grid[x][y-1].border_side['South'] == False:
                grid[x][y].neighbours.append(is_traversable(grid, (x,y), (x,y-1)))
            if y < GRID_SIZE-1 and grid[x][y+1].border_side['North'] == False:
                grid[x][y].neighbours.append(is_traversable(grid, (x,y), (x,y+1)))
            if x > 0 and grid[x-1][y].border_side['East'] == False:
                grid[x][y].neighbours.append(is_traversable(grid, (x,y), (x-1,y)))
            if x < GRID_SIZE-1 and grid[x+1][y].border_side['West'] == False:
                grid[x][y].neighbours.append(is_traversable(grid, (x,y), (x+1,y)))

def path(origin, current, grid):
    while current in origin:
        current = origin[current]
        if current.type != START:
            current.type = PATH
        renderSquares = DisplayGrid()
        renderSquares.draw_squares(grid)

def astar(start_pos, end_pos, grid):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, grid[start_pos[0]][start_pos[1]]))
    origin = {}
    grid[start_pos[0]][start_pos[1]].g_score = 0
    grid[start_pos[0]][start_pos[1]].f_score = heuristic(start_pos, end_pos)
    open_set_hash = {grid[start_pos[0]][start_pos[1]]}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == grid[end_pos[0]][end_pos[1]]:
            path(origin, current, grid)
            return True

        for neighbour_coor in current.neighbours:
            temp_g_score = current.g_score + 1
            neighbour_tile = grid[neighbour_coor[0]][neighbour_coor[1]]
            if temp_g_score < neighbour_tile.g_score:
                origin[neighbour_tile] = current
                neighbour_tile.g_score = temp_g_score
                neighbour_tile.f_score = temp_g_score + heuristic(neighbour_coor, end_pos)
                if neighbour_tile not in open_set_hash: 
                    count += 1
                    open_set.put((neighbour_tile.f_score, count, neighbour_tile))
                    open_set_hash.add(neighbour_tile)
                    if neighbour_tile != grid[end_pos[0]][end_pos[1]]:
                        neighbour_tile.type = OPEN

        if current != grid[start_pos[0]][start_pos[1]]:
            current.type = CLOSED
        renderSquares = DisplayGrid()
        renderSquares.draw_squares(grid)

    return False
        
