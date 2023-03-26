class Settings:
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 500
        self.grid_size = 10
        self.total_border_width = 10
        self.tile_size = (self.screen_width - self.total_border_width - 10) // self.grid_size
        self.border_width = self.total_border_width // self.grid_size
        self.square_color = (255, 255, 255)
        self.border_color = (0, 0, 0)