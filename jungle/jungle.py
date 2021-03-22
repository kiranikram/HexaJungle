import numpy as np
import random
import math

from jungle.utils import ElementsEnv, Actions, Definitions


class EmptyJungle:

    def __init__(self, size):

        self.size = size

        if self.size % 2 == 0 or size < Definitions.MIN_SIZE_ENVIR.value:
            raise ValueError('size should be an odd number')

        # check with ones mulitpy by definition s
        self.grid_env = np.zeros((self.size, self.size), dtype=int)
        self.place_obstacles()

        self.agent_white = None
        self.agent_black = None

        self.agents = []
        self.done = False

        # @KI: this would be specific for each agent
        # self.logs_collected = None

        # @KI: don't need that, this is calculated by the step function

    def place_obstacles(self):

        # place outside walls
        self.grid_env[:, 0] = ElementsEnv.OBSTACLE.value
        self.grid_env[:, -1] = ElementsEnv.OBSTACLE.value
        self.grid_env[0, :] = ElementsEnv.OBSTACLE.value
        self.grid_env[-1, :] = ElementsEnv.OBSTACLE.value

        # add corners
        for row in range(2, self.size - 2, 2):
            self.grid_env[row, 1] = ElementsEnv.OBSTACLE.value

        # @  kiran: because of symmetry, not sure you need this one.
        # for row in range(2, self.size - 2, 2):
        #     self.grid_env[row, self.size - 2] = ElementsEnv.OBSTACLE.value

        # place exits
        #
        # @ kiran: do that in a subclass.
        # TODO: set function that randomly determines exits

        # place unique obstacles

        # add trees
        # TODO: function that randomly sets trees in the forest env
        # self.grid_env[3, 6] = ElementsEnv.TREE.value

        # place additional obstacles so that all corners have the same shape.
        # ^done

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

        # @ kiran: you don't have to, but if it helps.
        self.agent_black.color = Definitions.BLACK
        self.agent_white.color = Definitions.WHITE

        # @ kiran: instead, use properties
        # can change in agent
        self.agent_black.x, self.agent_black.y = self.update_cartesian(self.agent_black)
        self.agent_white.x, self.agent_white.y = self.update_cartesian(self.agent_white)

    def step(self, actions):

        # because you pass objects (agents), you can make that much more simple
        # for agent in actions:
        #     agent.apply_actions(actions[agent])
        #     print(agent)

        # Apply physical actions, White starts

        # @ kiran: we should also know if agent climbs on boulder / shoulders of other agent (elevated)
        # and positions and angle will be changed in self.apply_actions.
        # so maybe, instead:  elevated, cut_tree = self.apply_action( agent, actions) ?

        # dont need to return position etccc changed in apply action automatically
        # self.agent_white.grid_position, self.agent_white.angle, self.agent_white.wood_logs = self.apply_action(
        # self.agent_white, actions)

        # self.agent_black.grid_position, self.agent_black.angle, self.agent_black.wood_logs = self.apply_action(
        # self.agent_black, actions)

        rew = {self.agent_black: 0.0, self.agent_white: 0.0}
        done = {self.agent_black: False, self.agent_white: False}

        ag_white_rew, white_done = self.apply_action(self.agent_white, actions, rew[self.agent_white],
                                                     done[self.agent_white])
        ag_black_rew, black_done = self.apply_action(self.agent_black, actions, rew[self.agent_black],
                                                     done[self.agent_black])

        done[self.agent_white] = white_done
        done[self.agent_black] = black_done

        if white_done is True and black_done is True:
            done = True
        else:
            done = False

        self.agent_white.done = white_done

        self.agent_black.done = black_done

        rew[self.agent_white] = ag_white_rew
        rew[self.agent_black] = ag_black_rew

        # For now, we don't need observations and rewards, so we will just return dummies
        # Later, we will replace it by the correct rewards and observations
        # but before that we will write tests about it.

        # @MG I feel that this reward dict needs to be outside of step, as each call to step will
        # update a running total for each of the agents

        # make function to test for what kind of reward

        # rew = self.get_reward(rew,actions)

        # From the point of view of the policy that each 'brain' will work,
        # do you need to know when a single agent has terminated?

        # don't need to be an attribute:
        # self.obs = self.generate_agent_obs()
        obs = self.generate_agent_obs()

        self.agent_black.x, self.agent_black.y = self.update_cartesian(self.agent_black)
        self.agent_white.x, self.agent_white.y = self.update_cartesian(self.agent_white)

        # self.logs_collected = self.agent_white.log_cache + self.agent_black.log_cache

        return obs, rew, done

    # TODO: list of rules that need to be reflected
    # 1. if agent bumps into obstacle, does not move from original position
    # 2. if next cell is river, and does not have enough logs, drowns
    def apply_action(self, agent, actions, agent_rew, agent_done):

        # assuming moves forward first, then changes angle

        row, col = agent.grid_position
        angle = agent.angle
        next_cell = self.grid_env[int(row), int(col)]

        agent_actions = actions[agent]

        # agent.angle = 0

        rotation = agent_actions[Actions.ROTATE]
        agent.angle = (angle + rotation) % 6

        movement_forward = agent_actions[Actions.FORWARD]

        if movement_forward != 0:
            row_new, col_new, next_cell = self.get_proximal_coordinate(row, col, agent.angle)
        else:
            row_new, col_new = row, col
        if next_cell == ElementsEnv.OBSTACLE.value:
            agent_rew = float(Definitions.REWARD_BUMP.value)
            row_new, col_new = row, col

        # TODO overhere check if next cell is river for both of them ; if so can go on to check for logs and build bridge 
        else:
            agent_rew = self.get_reward(next_cell, agent_rew, agent)
            agent_done = self.agent_exited(next_cell)

        agent.grid_position = row_new, col_new

        if next_cell == ElementsEnv.TREE.value:
            self.grid_env[int(row_new), int(col_new)] = ElementsEnv.EMPTY.value
            agent_rew = float(Definitions.REWARD_CUT_TREE.value)
            # There is a cap on the number of logs an agent can collect
            # This should be a parameter of the jungle subclass
            if agent.wood_logs < 2:
                agent.wood_logs += 1

        return agent_rew, agent_done

        # for now, to pass the test, you only need to move forward.
        # later, with more tests, you would need to check for obstacles, other agents, etc...

    def get_proximal_coordinate(self, row, col, angle):

        row_new, col_new = row, col

        if angle == 0:
            col_new += 1
        elif angle == 1:
            row_new -= 1
            col_new += row % 2
        elif angle == 2:
            row_new -= 1
            col_new += row % 2 - 1
        elif angle == 3:
            col_new -= 1
        elif angle == 4:
            row_new += 1
            col_new += row % 2 - 1
        else:
            row_new += 1
            col_new += row % 2

        next_cell = self.grid_env[int(row_new), int(col_new)]

        return row_new, col_new, next_cell

    def agent_exited(self, next_cell):

        exits = [ElementsEnv.EXIT_EASY.value, ElementsEnv.EXIT_DIFFICULT.value, ElementsEnv.EXIT_WHITE.value,
                 ElementsEnv.EXIT_BLACK.value]

        if next_cell in exits:
            return True
        else:
            return False

    def generate_agent_obs(self):
        return {self.agent_black: None, self.agent_white: None}

    def cell_type(self, x, y):
        return self.grid_env[x, y]

    def add_object(self, item, coords):
        r = coords[0]
        c = coords[1]
        self.grid_env[r, c] = item.value

    # TODO: change this to property in agent class
    def update_cartesian(self, agent):
        x = agent.grid_position[1] + 0.5
        y = (self.size - 1 - agent.grid_position[0]) * math.sqrt(3) / 2

        return x, y

    def get_reward(self, next_cell, agent_rew, agent):
        if next_cell == ElementsEnv.EXIT_EASY.value:
            agent_rew = float(Definitions.REWARD_EXIT_AVERAGE.value)
        elif next_cell == ElementsEnv.EXIT_DIFFICULT.value:
            agent_rew = float(Definitions.REWARD_EXIT_HIGH.value)

        elif next_cell == ElementsEnv.RIVER.value:
            print(agent.color, ' at river here ')
            print(self.agent_black.grid_position,self.agent_white.grid_position)
            if self.agent_black.grid_position == self.agent_white.grid_position:
                print('both at river')
                if (self.agent_black.wood_logs + self.agent_white.wood_logs) >= 2:
                    agent_rew = float(Definitions.REWARD_BUILT_BRIDGE.value)
                else:
                    agent_rew = float(Definitions.REWARD_DROWN.value)
            else:
                agent_rew = float(Definitions.REWARD_DROWN.value)

        if agent == self.agent_white:
            if next_cell == ElementsEnv.EXIT_WHITE.value:
                agent_rew = float(Definitions.REWARD_EXIT_VERY_HIGH.value)
            elif next_cell == ElementsEnv.EXIT_BLACK.value:
                agent_rew = float(Definitions.REWARD_EXIT_LOW.value)
            #elif next_cell == ElementsEnv.RIVER.value:
                #if self.agent_black.grid_position != self.agent_white.grid_position:
                    #agent_rew = float(Definitions.REWARD_DROWN.value)

        if agent == self.agent_black:
            if next_cell == ElementsEnv.EXIT_BLACK.value:
                agent_rew = float(Definitions.REWARD_EXIT_VERY_HIGH.value)
            elif next_cell == ElementsEnv.EXIT_WHITE.value:
                agent_rew = float(Definitions.REWARD_EXIT_LOW.value)
            #elif next_cell == ElementsEnv.RIVER.value:

                #if self.agent_black.grid_position != self.agent_white.grid_position:
                    #print('agent drowns')
                    #agent_rew = float(Definitions.REWARD_DROWN.value)



        return agent_rew