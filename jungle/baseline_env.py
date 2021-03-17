import numpy as np
import random
import math
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

        self.logs_collected = None
        self.rew = {self.agent_black: 0.0, self.agent_white: 0.0}

    def place_obstacles(self):

        # place outside walls

        # That's where these definitions are convenient
        # place outside walls
        self.grid_env[:, 0] = ElementsEnv.OBSTACLE.value
        self.grid_env[:, -1] = ElementsEnv.OBSTACLE.value
        self.grid_env[0, :] = ElementsEnv.OBSTACLE.value
        self.grid_env[-1, :] = ElementsEnv.OBSTACLE.value

        # add corners
        for row in range(2, self.size - 2, 2):
            self.grid_env[row, 1] = ElementsEnv.OBSTACLE.value

        for row in range(2, self.size - 2, 2):
            self.grid_env[row, self.size - 2] = ElementsEnv.OBSTACLE.value

        # add empty
        self.grid_env[1, 1] = ElementsEnv.EMPTY.value
        self.grid_env[1, 2] = ElementsEnv.EMPTY.value
        self.grid_env[2, 2] = ElementsEnv.EMPTY.value

        self.grid_env[2, self.size - 3] = ElementsEnv.EMPTY.value
        self.grid_env[1, self.size - 3] = ElementsEnv.EMPTY.value
        self.grid_env[1, self.size - 2] = ElementsEnv.EMPTY.value

        self.grid_env[self.size - 3, self.size - 3] = ElementsEnv.EMPTY.value
        self.grid_env[self.size - 2, self.size - 3] = ElementsEnv.EMPTY.value
        self.grid_env[self.size - 2, self.size - 2] = ElementsEnv.EMPTY.value

        self.grid_env[self.size - 2, 1] = ElementsEnv.EMPTY.value
        self.grid_env[self.size - 2, 2] = ElementsEnv.EMPTY.value
        self.grid_env[self.size - 3, 2] = ElementsEnv.EMPTY.value

        # place exits
        # TODO: set function that randomly determines exits

        # place unique obstacles

        # add trees
        # TODO: function that randomly sets trees in the forest env
        # self.grid_env[3, 6] = ElementsEnv.TREE.value

        # you have to do all the others

        # place additional obstacles so that all corners have the same shape.

    def add_agents(self, agent_1, agent_2):

        # flip a coin
        if random.random() > 0.5:
            self.agent_black = agent_1
            self.agent_white = agent_2

            # need better way of setting these
            self.agent_black.angle = 3
            self.agent_white.angle = 0

            self.agent_black.grid_position = ((self.size - 1) / 2, (self.size - 1) / 2 - 1)
            self.agent_white.grid_position = ((self.size - 1) / 2, (self.size - 1) / 2 + 1)





        else:
            self.agent_black = agent_2
            self.agent_white = agent_1

            self.agent_black.angle = 0
            self.agent_white.angle = 3

            self.agent_black.grid_position = ((self.size - 1) / 2, (self.size - 1) / 2 + 1)
            self.agent_white.grid_position = ((self.size - 1) / 2, (self.size - 1) / 2 - 1)

        self.agent_black.color = Definitions.BLACK
        self.agent_white.color = Definitions.WHITE

        self.agent_black.x, self.agent_black.y = self.update_cartesian(self.agent_black)
        self.agent_white.x, self.agent_white.y = self.update_cartesian(self.agent_white)

        # That's where you initialize the positions
        # self.agent_black.grid_position =

        # self.agent_white.grid_position =

    def step(self, actions):

        # because you pass objects (agents), you can make that much more simple
        # for agent in actions:
        #     agent.apply_actions(actions[agent])
        #     print(agent)

        # Apply physical actions, White starts

        self.agent_white.grid_position, self.agent_white.angle, self.agent_white.log_cache = self.apply_action(
            self.agent_white, actions)

        self.agent_black.grid_position, self.agent_black.angle, self.agent_black.log_cache = self.apply_action(
            self.agent_black, actions)

        # For now, we don't need observations and rewards, so we will just return dummies
        # Later, we will replace it by the correct rewards and observations
        # but before that we will write tests about it.

        rew = {self.agent_black: 0.0, self.agent_white: 0.0}
        rew[self.agent_white] = float(Definitions.REWARD_BUMP.value)
        rew[self.agent_black] = float(Definitions.REWARD_BUMP.value)

        # From the point of view of the policy that each 'brain' will work,
        # do you need to know when a single agent has terminated?
        done = self.both_exited()

        # don't need to be an attribute:
        # self.obs = self.generate_agent_obs()
        obs = self.generate_agent_obs()

        self.agent_black.x, self.agent_black.y = self.update_cartesian(self.agent_black)
        self.agent_white.x, self.agent_white.y = self.update_cartesian(self.agent_white)

        self.logs_collected = self.agent_white.log_cache + self.agent_black.log_cache

        return obs, rew, done

    def apply_action(self, agent, actions):

        # assuming moves forward first, then changes angle

        row, col = agent.grid_position
        angle = agent.angle

        agent_actions = actions[agent]

        # agent.angle = 0

        movement_forward = agent_actions[Actions.ROTATE]
        if movement_forward != 0:
            r, c, next_cell = self.get_proximal_coordinate(row, col, agent.angle)

        else:
            r , c = row , col
            next_cell = self.grid_env[int(row),int(col)]

        agent.grid_position = r, c

        rotation = agent_actions[Actions.ROTATE]
        agent.angle = (angle + rotation) % 6

        if next_cell == ElementsEnv.TREE.value:
            agent.log_cache += 1

        # for now, to pass the test, you only need to move forward.
        # later, with more tests, you would need to check for obstacles, other agents, etc...



        return agent.grid_position, agent.angle, agent.log_cache

    def get_proximal_coordinate(self, row, col, angle):

        row_new, col_new = int(row), int(col)

        if angle == 0:
            row_new -= 2
        elif angle == 1:
            row_new -= 1
            col_new += 1
        elif angle == 2:
            row_new += 1
            col_new += 1
        elif angle == 3:
            row_new += 2
        elif angle == 4:
            row_new += 1
            col_new += - 1
        else:
            row_new -= 1
            col_new -= 1


        next_cell = self.grid_env[row_new, col_new]

        return row_new, col_new, next_cell

    def both_exited(self):
        # if agent_1.grid_position and agent_2.grid_position in self.exits:
        #    return True

        # For now, this is sufficient to pass the tests.
        done = {self.agent_black: False, self.agent_white: False}
        return done

    def generate_agent_obs(self):
        return {self.agent_black: None, self.agent_white: None}

    # ignore fgor now
    def get_black_starting(self, agent):
        r, c = 0, 0
        print('agent', agent)
        # print('black one')
        # r, c = (self.size - 1) / 2, (self.size - 1) / 2 - 1
        # elif 'agent' == 'agent_2':
        # print('black two ')
        # r, c = (self.size - 1) / 2, (self.size - 1) / 2 + 1

        # return r, c

    # ignore for now
    def get_white_starting(self, agent):
        r, c = 0, 0
        if 'agent' == 'agent_1':
            print('white one')
            r, c = (self.size - 1) / 2, (self.size - 1) / 2 - 1
        elif 'agent' == 'agent_2':
            print('white two ')
            r, c = (self.size - 1) / 2, (self.size - 1) / 2 + 1

        return r, c

    def cell_type(self, x, y):
        return self.grid_env[x, y]

    def add_object(self, item, coords):
        r = coords[0]
        c = coords[1]
        self.grid_env[r, c] = item.value

    def update_cartesian(self, agent):
        x = agent.grid_position[1] + 0.5
        y = (self.size - 1 - agent.grid_position[0]) * math.sqrt(3) / 2

        return x, y
