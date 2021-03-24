import numpy as np
import random
import math

from jungle.utils import ElementsEnv, Actions, Definitions


# DO MENTION AGENTs CAN BE ON SAME CELL

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
        self.both_at_river = False
        self.on_same_cell = False

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
        obs = {self.agent_black: [], self.agent_white: []}

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

        # @MG I feel that this reward dict needs to be outside of step, as each call to step will
        # update a running total for each of the agents

        obs[self.agent_white] = self.generate_agent_obs(self.agent_white)
        obs[self.agent_black] = self.generate_agent_obs(self.agent_black)

        self.agent_black.x, self.agent_black.y = self.update_cartesian(self.agent_black)
        self.agent_white.x, self.agent_white.y = self.update_cartesian(self.agent_white)

        return obs, rew, done

    # TODO: write function that determines if in fact agent can climb on other agent; for this they have to be on the
    #  same cell ; this will tie into action selection {legal actions}
    # same cell check will have similar issues to reward same cell (the lag)
    def apply_action(self, agent, actions, agent_rew, agent_done):

        # assuming moves forward first, then changes angle

        row, col = agent.grid_position
        angle = agent.angle
        next_cell = self.grid_env[int(row), int(col)]

        agent_actions = actions[agent]

        rotation = agent_actions[Actions.ROTATE]
        movement_forward = agent_actions[Actions.FORWARD]
        agent_climbs = agent_actions[Actions.CLIMB]
        agent.angle = (angle + rotation) % 6

        # TODO agent rew can consist of multiple items : eg neg rew for carrying but also neg reward for bumping

        if movement_forward != 0:
            row_new, col_new, next_cell = self.get_proximal_coordinate(row, col, agent.angle)
        else:
            row_new, col_new = row, col

        if agent_climbs != 0:

            agent_rew = self.climb_dynamics(agent, actions, agent_rew, next_cell)

        elif agent_climbs == 0:
            agent_rew = self.check_partner_reactions(agent, actions, agent_rew, movement_forward)
        if next_cell == ElementsEnv.OBSTACLE.value:
            agent_rew = float(Definitions.REWARD_BUMP.value)
            row_new, col_new = row, col

        elif next_cell == ElementsEnv.BOULDER.value:
            print('we here ')
            agent_rew = float(Definitions.REWARD_BUMP.value)
            if not agent.on_shoulders:
                row_new, col_new = row, col
            agent.range_observation = agent.range_observation - Definitions.RANGE_INCREASE.value
            # TODO come back to this as need a way


        elif next_cell == ElementsEnv.RIVER.value:

            row_new, col_new, agent_rew = self.check_agents_at_river(agent, next_cell, actions, agent_rew, row_new,
                                                                     col_new, row, col)
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

    def generate_agent_obs(self, agent):

        obs = []

        # iterate over range
        for obs_range in range(1, agent.range_observation + 1):

            row, col = agent.grid_position
            angle = agent.angle

            # go to start
            for i in range(obs_range):
                row, col, _ = self.get_next_cell(row, col, (angle - 1) % 6)

            if 0 <= row < self.size and 0 <= col < self.size:
                obs.append(self.grid_env[int(row), int(col)])
            else:
                obs.append(0)

            # move first segment
            for i in range(obs_range):
                row, col, _ = self.get_next_cell(row, col, (angle + 1) % 6)

                if 0 <= row < self.size and 0 <= col < self.size:
                    obs.append(self.grid_env[int(row), int(col)])
                else:
                    obs.append(0)

            # move second segment
            for i in range(obs_range):
                row, col, _ = self.get_next_cell(row, col, (angle + 2) % 6)

                if 0 <= row < self.size and 0 <= col < self.size:
                    obs.append(self.grid_env[int(row), int(col)])
                else:
                    obs.append(0)

        return np.asarray(obs)

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

        if agent == self.agent_white:
            if next_cell == ElementsEnv.EXIT_WHITE.value:
                agent_rew = float(Definitions.REWARD_EXIT_VERY_HIGH.value)
            elif next_cell == ElementsEnv.EXIT_BLACK.value:
                agent_rew = float(Definitions.REWARD_EXIT_LOW.value)

        if agent == self.agent_black:
            if next_cell == ElementsEnv.EXIT_BLACK.value:
                agent_rew = float(Definitions.REWARD_EXIT_VERY_HIGH.value)
            elif next_cell == ElementsEnv.EXIT_WHITE.value:
                agent_rew = float(Definitions.REWARD_EXIT_LOW.value)

        return agent_rew

    def check_agents_at_river(self, agent, next_cell, actions, agent_rew, row_new, col_new, row, col):

        if self.both_at_river:
            agent_rew = float(Definitions.REWARD_BUILT_BRIDGE.value)
            self.grid_env[int(row_new), int(col_new)] = ElementsEnv.BRIDGE.value
            row_new, col_new = row, col
        else:
            if agent.color == Definitions.BLACK:

                partner_row, partner_col = self.agent_white.grid_position
                partner_angle = self.agent_white.angle
                partner_actions = actions[self.agent_white]
                partner_rotation = partner_actions[Actions.ROTATE]
                partner_angle = (partner_angle + partner_rotation)
                partner_forward = partner_actions[Actions.FORWARD]
                if partner_forward != 0:
                    _, _, partner_next_cell = self.get_proximal_coordinate(partner_row, partner_col, partner_angle)

                    if partner_next_cell == next_cell:

                        if self.agent_white.wood_logs + self.agent_black.wood_logs >= 2:
                            agent_rew = float(Definitions.REWARD_BUILT_BRIDGE.value)
                            self.both_at_river = True
                            row_new, col_new = row, col
                        else:
                            agent_rew = float(Definitions.REWARD_DROWN.value)
                    else:
                        agent_rew = float(Definitions.REWARD_DROWN.value)
                else:
                    agent_rew = float(Definitions.REWARD_DROWN.value)
            elif agent.color == Definitions.WHITE:

                partner_row, partner_col = self.agent_black.grid_position
                partner_angle = self.agent_black.angle
                partner_actions = actions[self.agent_black]
                partner_rotation = partner_actions[Actions.ROTATE]
                partner_angle = (partner_angle + partner_rotation)
                partner_forward = partner_actions[Actions.FORWARD]
                if partner_forward != 0:
                    _, _, partner_next_cell = self.get_proximal_coordinate(partner_row, partner_col, partner_angle)
                    if partner_next_cell == next_cell:
                        if self.agent_white.wood_logs + self.agent_black.wood_logs >= 2:
                            agent_rew = float(Definitions.REWARD_BUILT_BRIDGE.value)
                            self.both_at_river = True
                            row_new, col_new = row, col
                        else:
                            agent_rew = float(Definitions.REWARD_DROWN.value)
                    else:
                        agent_rew = float(Definitions.REWARD_DROWN.value)
                else:
                    agent_rew = float(Definitions.REWARD_DROWN.value)

        return row_new, col_new, agent_rew

    # from the perspective of the agent that climbs - also need to account for the agent bearing the burden
    def climb_dynamics(self, agent, actions, agent_rew, next_cell):
        print('we are climbing')

        if agent.color == Definitions.BLACK:
            partner_on_cell = self.check_cell_occupancy(agent, actions, next_cell)
            if not partner_on_cell:
                agent_rew = float(Definitions.REWARD_INVIABLE_CLIMB.value)
            partner_actions = actions[self.agent_white]
            partner_forward = partner_actions[Actions.FORWARD]
            partner_climbed = partner_actions[Actions.CLIMB]
            if partner_climbed == 1:
                agent_rew = float(Definitions.REWARD_BOTH_CLIMBED.value)
            elif partner_forward == 0:
                agent.range_observation = agent.range_observation + Definitions.RANGE_INCREASE.value
                agent.on_shoulders = True

        elif agent.color == Definitions.WHITE:
            partner_on_cell = self.check_cell_occupancy(agent, actions, next_cell)
            if not partner_on_cell:
                agent_rew = float(Definitions.REWARD_INVIABLE_CLIMB.value)
            partner_actions = actions[self.agent_black]
            partner_forward = partner_actions[Actions.FORWARD]
            partner_climbed = partner_actions[Actions.CLIMB]
            if partner_climbed == 1:
                agent_rew = float(Definitions.REWARD_BOTH_CLIMBED.value)
            elif partner_forward == 0:
                agent.range_observation = agent.range_observation + Definitions.RANGE_INCREASE.value
                agent.on_shoulders = True

        return agent_rew

    def check_partner_reactions(self, agent, actions, agent_rew, forward):
        if agent.color == Definitions.BLACK:
            partner_actions = actions[self.agent_white]
            partner_climbed = partner_actions[Actions.CLIMB]
            partner_forward = partner_actions[Actions.FORWARD]
            if partner_climbed == 1:
                agent_rew = float(Definitions.REWARD_CARRYING.value)
            elif agent.on_shoulders and partner_forward == 1 and forward == 0:

                agent_rew = float(Definitions.REWARD_FELL.value)
                agent.on_shoulders = False
                agent.range_observation = agent.range_observation - Definitions.RANGE_INCREASE.value
            elif agent.on_shoulders and partner_forward == 1 and forward == 1:
                agent.on_shoulders = True

        elif agent.color == Definitions.WHITE:
            partner_actions = actions[self.agent_black]
            partner_climbed = partner_actions[Actions.CLIMB]
            partner_forward = partner_actions[Actions.FORWARD]
            if partner_climbed == 1:
                agent_rew = float(Definitions.REWARD_CARRYING.value)
            elif agent.on_shoulders and partner_forward == 1 and forward == 0:

                agent_rew = float(Definitions.REWARD_FELL.value)
                agent.on_shoulders = False
                agent.range_observation = agent.range_observation - Definitions.RANGE_INCREASE.value
            elif agent.on_shoulders and partner_forward == 1 and forward == 1:
                agent.on_shoulders = True

        return agent_rew

    def check_cell_occupancy(self, agent, actions, next_cell):

        if agent.color == Definitions.BLACK:

            partner_row, partner_col = self.agent_white.grid_position
            partner_angle = self.agent_white.angle
            partner_actions = actions[self.agent_white]
            partner_rotation = partner_actions[Actions.ROTATE]
            partner_angle = (partner_angle + partner_rotation)
            partner_forward = partner_actions[Actions.FORWARD]

            _, _, partner_next_cell = self.get_proximal_coordinate(partner_row, partner_col, partner_angle)

            if partner_next_cell == next_cell:
                self.on_same_cell = True
                return True
            else:
                return False

        if agent.color == Definitions.WHITE:

            partner_row, partner_col = self.agent_black.grid_position
            partner_angle = self.agent_black.angle
            partner_actions = actions[self.agent_black]
            partner_rotation = partner_actions[Actions.ROTATE]
            partner_angle = (partner_angle + partner_rotation)
            partner_forward = partner_actions[Actions.FORWARD]

            _, _, partner_next_cell = self.get_proximal_coordinate(partner_row, partner_col, partner_angle)

            if partner_next_cell == next_cell:
                self.on_same_cell = True
                return True
            else:
                return False

    def get_next_cell(self, row, col, angle):

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

        if 0 <= row_new < self.size and 0 <= col_new < self.size:
            next_cell = self.grid_env[int(row_new), int(col_new)]
        else:
            next_cell = 0

        return row_new, col_new, next_cell
