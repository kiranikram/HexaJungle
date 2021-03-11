import numpy as np
import random
from enum import Enum, IntEnum

# Always ue complete imports
from jungle.utils import Definitions

# You can do it like this:
# import jungle.agent as agent
# or like this:
from jungle.agent import Agent, Actions

# sets general layout of grid in hexagonal format
class Elements(Enum):
    EXIT_ONE = 0
    EXIT_TWO = 1
    EXIT_THREE = 3
    RIVER = 5
    BOULDER = 7
    TREE = 9


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

# why do you define them here?
agent_1 = Agent(4,4,2,1)
agent_2 = Agent(3,2,0,4)


class JungleGrid:

    def __init__(self, size):
        self.size = size
        self.exits = []
        self.grid_env = np.zeros((self.size, self.size), dtype=int)
        self.exits = set_centroids(self.grid_env, self.exits)
        self.grid_env = set_exits(self.grid_env, self.exits)
        self.ip_agent_1_r, self.ip_agent_1_c = ((self.size - 1) / 2, (self.size - 1) / 2 - 1)
        self.ip_agent_2_r, self.ip_agent_2_c = ((self.size - 1) / 2, (self.size - 1) / 2 + 1)
        self.obs = {'agent_1': [0, 0], 'agent_2': [0, 0]}
        self.rew = {'agent_1': -5, 'agent_2': -5}

    def env(self):

        return self.grid_env

    def add_agents(self, agent_1, agent_2):
        if random.random() > 0.5:
            agent_1.color = Definitions.WHITE
        else:
            agent_2.color = Definitions.WHITE

            agent_1.grid_position = self.ip_agent_1_r, self.ip_agent_1_c
            agent_2.grid_position = self.ip_agent_2_r, self.ip_agent_2_c

    def step(self, actions):
        for agent in actions:
            agent.apply_actions(actions[agent])

        # get both agent's grid position
        # one may reach an exit x timesteps before the other.
        # upon reaching exit agent stops playing and waits for other agent

        done = self.both_exited()

        self.obs = self.generate_agent_obs()

        return self.obs, self.rew, done

    def both_exited(self):
        if agent_1.grid_position and agent_2.grid_position in self.exits:
            return True

    def generate_agent_obs(self):
        return self.obs


jungle = JungleGrid(11)
print(jungle.env)
