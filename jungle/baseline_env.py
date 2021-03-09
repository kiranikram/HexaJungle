import numpy as np


# sets general layout of grid in hexagonal format
def set_centroids(grid):
    exits = []

    for r in range(1, grid.shape[0], 5):
        for c in range(1, grid.shape[1], 2):
            grid[r, c] = 22
            if r == 0:
                exits.append([r, c])

    for r in range(3,grid.shape[0],5):
        for c in range(0,grid.shape[1]+1,2):
            grid[r,c] = 44
            if c == grid.shape[1]:
                exits.append([r, c])
            elif c == 0:
                exits.append([r, c])






class JungleGrid:

    def __init__(self, height, width):
        self.height = height
        self.width = width

        self.env = np.zeros((self.height, self.width), dtype=int)
        self.env = set_centroids(self.env)

    def env(self):
        return self.env


jungle = JungleGrid(10, 10)
print(jungle.env)
