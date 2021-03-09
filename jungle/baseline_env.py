import numpy as np
import random


# sets general layout of grid in hexagonal format

def boundaries(local_exit, exit_type, grid):
    r = local_exit[0]
    c = local_exit[1]
    if local_exit[0] == 0:

        grid[r + 1, c - 1] = exit_type
        grid[r + 2, c] = exit_type
        grid[r + 1, c + 1] = exit_type

    elif local_exit[1] == 10:

        grid[r - 2, c] = exit_type
        grid[r - 1, c - 1] = exit_type
        grid[r + 1, c - 1] = exit_type
        grid[r + 2, c] = exit_type

    elif local_exit[1] == 0:

        grid[r - 2, c] = exit_type
        grid[r - 1, c + 1] = exit_type
        grid[r + 1, c + 1] = exit_type
        grid[r + 2, c] = exit_type

    return grid


def set_centroids(grid, exits):
    for r in range(0, grid.shape[0], 5):
        for c in range(1, grid.shape[1], 2):
            grid[r, c] = 22
            if r == 0:
                exits.append([r, c])

    for r in range(3, grid.shape[0], 5):
        for c in range(0, grid.shape[1] + 1, 2):
            grid[r, c] = 44
            if c == grid.shape[1]:
                exits.append([r, c])
            elif c == 0:
                exits.append([r, c])

    return exits


def set_exits(grid, exits):
    open_exit = random.sample(exits, 1)

    exits.remove(open_exit[0])

    river_exit = random.sample(exits, 1)

    exits.remove(river_exit[0])
    grid = boundaries(river_exit[0], 5, grid)

    boulder_exit = random.sample(exits, 1)

    exits.remove(boulder_exit[0])
    grid = boundaries(boulder_exit[0], 7, grid)

    return grid


class JungleGrid:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.exits = []

        self.env = np.zeros((self.height, self.width), dtype=int)

        self.exits = set_centroids(self.env, self.exits)

        self.env = set_exits(self.env, self.exits)

    def env(self):
        return self.env


jungle = JungleGrid(11, 11)
print(jungle.env)
