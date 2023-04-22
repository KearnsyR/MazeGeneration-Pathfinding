import pygame
import sys
import pygame_gui
from maze import Maze
from path_finding import Pathfinding
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Procedurally Generated Maze and Pathfinding')
        self.clock = pygame.time.Clock()
        self.main_menu = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.end_game = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.current_maze_algorithm = "Recursive Backtracker"
        self.current_pathfinding_algorithm = "A*"
        self.grid_size = 10
        self.tile_size = 500 / self.grid_size
        self.starting_coordinate = (SCREEN_WIDTH - (self.grid_size * self.tile_size)) / 2

    def create_ui_elements(self):
        self.maze_size_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['10', '20', '30'],
            starting_option='10',
            relative_rect=pygame.Rect((10, 10), (200, 30)),
            manager=self.main_menu
        )
        
        self.maze_algorithm_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['Recursive Backtracker', 'Prim\'s Algorithm', 'Kruskal\'s Algorithm'],
            starting_option='Recursive Backtracker',
            relative_rect=pygame.Rect((10, 50), (200, 30)),
            manager=self.main_menu
        )

        self.pathfinding_algorithm_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['A*', 'Dijkstras', 'Breadth-First Search'],
            starting_option='A*',
            relative_rect=pygame.Rect((10, 90), (200, 30)),
            manager=self.main_menu
        )

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 110, SCREEN_HEIGHT - 40), (100, 30)),
            text='Start',
            manager=self.main_menu
        )

        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 110, SCREEN_HEIGHT - 90), (100, 30)),
            text='Restart',
            manager=self.end_game
        )

        self.new_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 110, SCREEN_HEIGHT - 140), (100, 30)),
            text='New',
            manager=self.end_game
        )

        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 110, SCREEN_HEIGHT - 190), (100, 30)),
            text='Quit',
            manager=self.end_game
        )

    def start(self):
        maze = Maze(self.current_maze_algorithm, self.grid_size, self.starting_coordinate, self.tile_size)
        start_pos, end_pos, grid = maze.generate_maze()
        pathfinding = Pathfinding(grid, start_pos, end_pos, self.current_pathfinding_algorithm, self.grid_size, self.starting_coordinate, self.tile_size)
        grid[start_pos[0]][start_pos[1]].type = START
        grid[end_pos[0]][end_pos[1]].type = END
        pathfinding.find_path()

    def complete(self, time_delta):
        while True:
            self.end_game.update(time_delta)
            self.end_game.draw_ui(self.screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                self.end_game.process_events(event)
                if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.restart_button:
                        self.screen.fill((0,0,0))
                        self.start()
                    elif event.ui_element == self.new_button:
                        return False
                    elif event.ui_element == self.quit_button:
                        pygame.quit()
                        sys.exit()

    def run(self):
        self.create_ui_elements()

        while True:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                self.main_menu.process_events(event)
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                        if event.ui_element == self.maze_algorithm_dropdown:
                            self.current_maze_algorithm = event.text
                        elif event.ui_element == self.pathfinding_algorithm_dropdown:
                            self.current_pathfinding_algorithm = event.text
                        elif event.ui_element == self.maze_size_dropdown:
                            self.grid_size = int(event.text)
                            self.tile_size = 500 / self.grid_size
                    elif event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.start_button:
                            self.start()
                            self.complete(time_delta)

            self.main_menu.update(time_delta)

            self.screen.fill((0,0,0))

            self.main_menu.draw_ui(self.screen)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()