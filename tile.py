class Tile:
    def __init__(self, x, y):
        self.border_side = {
            'North': True,
            'East': True,
            'South': True,
            'West': True
        }
        self.x = x
        self.y = y
        self.neighbours = []