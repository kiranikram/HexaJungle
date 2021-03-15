import numpy as np
import random
from enum import Enum, IntEnum

# Always ue complete imports
from jungle.utils import ElementsEnv, Actions, Definitions

# You can do it like this:
# import jungle.agent as agent
# or like this:
from jungle.agent import Agent


# For now, you don't need that:
# def boundaries(local_exit, exit_type, grid):
#     r = local_exit[0]
#     c = local_exit[1]
#     if local_exit[0] == 0:
#
#         grid[r + 1, c - 1] = exit_type
#         grid[r + 2, c] = exit_type
#         grid[r + 1, c + 1] = exit_type
#
#     elif local_exit[1] == 10:
#
#         grid[r - 2, c] = exit_type
#         grid[r - 1, c - 1] = exit_type
#         grid[r + 1, c - 1] = exit_type
#         grid[r + 2, c] = exit_type
#
#     elif local_exit[1] == 0:
#
#         grid[r - 2, c] = exit_type
#         grid[r - 1, c + 1] = exit_type
#         grid[r + 1, c + 1] = exit_type
#         grid[r + 2, c] = exit_type
#
#     return grid
#
#
# def set_centroids(grid, exits):
#     for r in range(0, grid.shape[0], 5):
#         for c in range(1, grid.shape[1], 2):
#             grid[r, c] = 22
#             if r == 0:
#                 exits.append([r, c])
#
#     for r in range(3, grid.shape[0], 5):
#         for c in range(0, grid.shape[1] + 1, 2):
#             grid[r, c] = 44
#             if c == grid.shape[1]:
#                 exits.append([r, c])
#             elif c == 0:
#                 exits.append([r, c])
#
#     return exits
#
#
# def set_exits(grid, exits):
#     open_exit = random.sample(exits, 1)
#
#     exits.remove(open_exit[0])
#
#     river_exit = random.sample(exits, 1)
#
#     exits.remove(river_exit[0])
#     grid = boundaries(river_exit[0], 5, grid)
#
#     boulder_exit = random.sample(exits, 1)
#
#     exits.remove(boulder_exit[0])
#     grid = boundaries(boulder_exit[0], 7, grid)
#
#     return grid


# why do you define them here?
# agent_1 = Agent(4, 4, 2, 1)
# agent_2 = Agent(3, 2, 0, 4)


class JungleGrid:

    def __init__(self, size):

        self.size = size

        if self.size % 2 == 0:
            raise ValueError('size should be an odd number')

        # Don't need that for now
        # self.exits = []

        self.grid_env = np.zeros((self.size, self.size), dtype=int)
        self.place_obstacles()

        # self.exits = set_centroids(self.grid_env, self.exits)
        # self.grid_env = set_exits(self.grid_env, self.exits)

        # You don't need this here, you can move that directly to add_agents
        # self.ip_agent_1_r, self.ip_agent_1_c = ((self.size - 1) / 2, (self.size - 1) / 2 - 1)
        # self.ip_agent_2_r, self.ip_agent_2_c = ((self.size - 1) / 2, (self.size - 1) / 2 + 1)

        # You don't need that here, you can create the observations in the step loop.
        # so you don't need attributes
        # self.obs = {agent_1: {'field': 0, 'depth': 0}, agent_2: {'field': 0, 'depth': 0}}
        # self.rew = {agent_1: {'field': 0, 'depth': 0}, agent_2: {'field': 0, 'depth': 0}}

        # You would need attributes for agents.
        # Before being added, you can just set them to none.

        self.agent_white = None
        self.agent_black = None

    # Why do you need that ?
    # def env(self):
    #     return self.grid_env

    def place_obstacles(self):

        # place outside walls

        # That's where these definitions are convenient
        self.grid_env[:, 0] = ElementsEnv.OBSTACLE.value
        # you have to do all the others

        # place additional obstacles so that all corners have the same shape.

    def add_agents(self, agent_1, agent_2):

        # flip a coin
        if random.random() > 0.5:
            self.agent_black = agent_1
            self.agent_white = agent_2
        else:
            self.agent_black = agent_2
            self.agent_white = agent_1

        self.agent_black.color = Definitions.BLACK
        self.agent_white.color = Definitions.WHITE

        # That's where you initialize the positions
        self.agent_black.grid_position = self.get_black_starting()
        self.agent_white.grid_position = self.get_white_starting()

    def step(self, actions):

        # because you pass objects (agents), you can make that much more simple
        # for agent in actions:
        #     agent.apply_actions(actions[agent])
        #     print(agent)

        # Apply physical actions, White starts
        self.apply_action(self.agent_white, actions)
        self.apply_action(self.agent_black, actions)

        # For now, we don't need observations and rewards, so we will just return dummies
        # Later, we will replace it by the correct rewards and observations
        # but before that we will write tests about it.
        rew = {self.agent_black: 0.0, self.agent_white: 0.0}

        # From the point of view of the policy that each 'brain' will work,
        # do you need to know when a single agent has terminated?
        done = self.both_exited()

        # don't need to be an attribute:
        # self.obs = self.generate_agent_obs()
        obs = self.generate_agent_obs()

        return obs, rew, done

    def apply_action(self, agent, actions):

        agent_actions = actions[agent]

        rotation = agent_actions[Actions.ROTATE]
        agent.angle = 0

        movement_forward = agent_actions[Actions.ROTATE]
        # for now, to pass the test, you only need to move forward.
        # later, with more tests, you would need to check for obstacles, other agents, etc...

    def both_exited(self):
        # if agent_1.grid_position and agent_2.grid_position in self.exits:
        #    return True

        # For now, this is sufficient to pass the tests.
        done = {self.agent_black:False, self.agent_white :False}
        return done

    def generate_agent_obs(self):
        return {self.agent_black: None, self.agent_white: None}

    def get_black_starting(self):
        r, c = ((self.size - 1) / 2, (self.size - 1) / 2 - 1)
        return r, c

    def get_white_starting(self):
        r , c = ((self.size - 1) / 2, (self.size - 1) / 2 + 1)
        return r, c
