import numpy as np
import random


# sets general layout of grid in hexagonal format


class JungleGrid:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.exits = []

        self.env = np.zeros((self.height, self.width), dtype=int)

    def set_centroids(self):
        grid = self.env

        for r in range(1, grid.shape[0], 5):
            for c in range(1, grid.shape[1], 2):
                # grid[r, c] = 22
                if r == 0:
                    self.exits.append([r, c])

        for r in range(3, grid.shape[0], 5):
            for c in range(0, grid.shape[1] + 1, 2):
                # grid[r,c] = 44
                if c == grid.shape[1]:
                    self.exits.append([r, c])
                elif c == 0:
                    self.exits.append([r, c])

    def set_exits(self, grid):

        def boundaries(local_exit, exit_type, grid):
            r = exit[0]
            c = exit[1]
            if exit[0] == 0:

                grid[r + 1, c - 1] = exit_type
                grid[r + 2, c] = exit_type
                grid[r + 1, c + 1] = exit_type

            elif exit[1] == 10:

                grid[r - 2, c] = exit_type
                grid[r - 1, c - 1] = exit_type
                grid[r + 1, c - 1] = exit_type
                grid[r + 2, c] = exit_type

            elif exit[1] == 0:

                grid[r - 2, c] = exit_type
                grid[r - 1, c + 1] = exit_type
                grid[r + 1, c + 1] = exit_type
                grid[r + 2, c] = exit_type

            return grid

        open_exit = random.sample(self.exits, 1)

        self.exits.remove(open_exit[0])

        river_exit = random.sample(self.exits, 1)

        self.exits.remove(river_exit[0])
        grid = boundaries(river_exit[0], 5, grid)

        boulder_exit = random.sample(self.exits, 1)

        self.exits.remove(boulder_exit[0])
        grid = boundaries(boulder_exit[0], 7, grid)

        return grid


jungle = JungleGrid(10, 10)
print(jungle.env)
