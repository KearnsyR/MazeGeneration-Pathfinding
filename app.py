import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up the grid
grid_size = 10
total_border_width = 10
square_size = (screen_width - total_border_width - 10) // grid_size
border_width = total_border_width // grid_size
square_color = (255, 255, 255)  # white
border_color = (0, 0, 0)  # black
grid = [[{'top': True, 'right': True, 'bottom': True, 'left': True} for j in range(grid_size)] for i in range(grid_size)]

# Function to get unvisited neighbors
def get_unvisited_neighbors(i, j, grid):
    neighbors = []
    if i > 0 and all(grid[i-1][j].values()):
        neighbors.append((i-1, j))
    if i < grid_size - 1 and all(grid[i+1][j].values()):
        neighbors.append((i+1, j))
    if j > 0 and all(grid[i][j-1].values()):
        neighbors.append((i, j-1))
    if j < grid_size - 1 and all(grid[i][j+1].values()):
        neighbors.append((i, j+1))
    return neighbors

# Function to get start and end positon
def start_end_pos(side):
    x = random.randint(0, grid_size-1)
    y = random.randint(0, grid_size-1)
    if side == 'top':
        grid[0][y]['top'] = False
        return (0, y)
    elif side == 'bottom':
        grid[grid_size-1][y]['bottom'] = False
        return (grid_size-1, y)
    elif side == 'left':
        grid[x][0]['left'] = False
        return (x, 0)
    elif side == 'right':
        grid[x][grid_size-1]['right'] = False
        return (x, grid_size-1)

# Function to update squares in grid
def update_screen():
    screen.fill(square_color)
    for x in range(grid_size):
        for y in range(grid_size):
            if grid[x][y]['top']:
                pygame.draw.rect(screen, border_color, (y * square_size + 10, x * square_size + 10, square_size, border_width))
            if grid[x][y]['right']:
                pygame.draw.rect(screen, border_color, ((y + 1) * square_size - border_width + 10, x * square_size + 10, border_width, square_size))
            if grid[x][y]['bottom']:
                pygame.draw.rect(screen, border_color, (y * square_size + 10, (x + 1) * square_size - border_width + 10, square_size, border_width))
            if grid[x][y]['left']:
                pygame.draw.rect(screen, border_color, (y * square_size + 10, x * square_size + 10, border_width, square_size))
    pygame.display.flip()

# Game loop
visited_cells = set()
stack = [(random.randint(0, grid_size-1), random.randint(0, grid_size-1))]
start_side = ['top', 'bottom', 'left', 'right']
side = random.choice(start_side)
opposite_sides = {'top': 'bottom', 'bottom': 'top', 'left': 'right', 'right': 'left'}
while stack:
    i, j = stack.pop()
    visited_cells.add((i, j))
    unvisited_neighbors = [neighbor for neighbor in get_unvisited_neighbors(i, j, grid) if neighbor not in visited_cells]
    if unvisited_neighbors:
        stack.append((i, j))
        neighbor_i, neighbor_j = random.choice(unvisited_neighbors)
        if neighbor_i < i:
            grid[i][j]['top'] = False
            grid[neighbor_i][neighbor_j]['bottom'] = False
        elif neighbor_i > i:
            grid[i][j]['bottom'] = False
            grid[neighbor_i][neighbor_j]['top'] = False
        elif neighbor_j < j:
            grid[i][j]['left'] = False
            grid[neighbor_i][neighbor_j]['right'] = False
        else:
            grid[i][j]['right'] = False
            grid[neighbor_i][neighbor_j]['left'] = False

        update_screen()
        pygame.time.wait(50)
        stack.append((neighbor_i, neighbor_j))

start_pos = start_end_pos(side)
end_pos = start_end_pos(opposite_sides[side])
print("Starting location is X:" + str(start_pos[0]) + " Y:" + str(start_pos[1]) + " and the ending location is X:" + str(end_pos[0]) + " Y:" + str(end_pos[1]))
update_screen()

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

# Clean up
pygame.quit()