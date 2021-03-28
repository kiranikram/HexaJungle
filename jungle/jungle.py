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

        self.grid_env = np.ones((self.size, self.size), dtype=int)
        self.place_obstacles()
        self.agent_white = None
        self.agent_black = None
        self.agents = []
        self.done = False
        self.both_at_river = False
        self.both_at_tree = False
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
        # agent.apply_actions(actions[agent])
        #     print(agent)

        # Apply physical actions, White starts

        # @ kiran: we should also know if agent climbs on boulder / shoulders of other agent (elevated)
        # and positions and angle will be changed in self.apply_actions.
        # so maybe, instead:  elevated, cut_tree = self.apply_action( agent, actions) ?

        rew = {self.agent_black: 0.0, self.agent_white: 0.0}
        done = {self.agent_black: False, self.agent_white: False}
        obs = {self.agent_black: None, self.agent_white: None}

        ag_white_rew, white_done = self.apply_action(self.agent_white, actions, rew[self.agent_white],
                                                     done[self.agent_white])
        ag_black_rew, black_done = self.apply_action(self.agent_black, actions, rew[self.agent_black],
                                                     done[self.agent_black])

        # done[self.agent_white] = white_done
        # done[self.agent_black] = black_done

        # if white_done is True and black_done is True:
        # done = True
        # else:
        # done = False

        self.agent_white.done = white_done

        self.agent_black.done = black_done

        rew[self.agent_white] = ag_white_rew
        rew[self.agent_black] = ag_black_rew

        # @MG I feel that this reward dict needs to be outside of step, as each call to step will
        # update a running total for each of the agents

        if self.agent_white.range_observation is not None:
            obs[self.agent_white] = self.generate_agent_obs(self.agent_white)
        if self.agent_black.range_observation is not None:
            obs[self.agent_black] = self.generate_agent_obs(self.agent_black)

        self.agent_black.x, self.agent_black.y = self.update_cartesian(self.agent_black)
        self.agent_white.x, self.agent_white.y = self.update_cartesian(self.agent_white)

        return obs, rew, done

    # same cell check will have similar issues to reward same cell (the lag)

    # SAT : might need to pass in rew for other agent - same cell for tree cutting
    def apply_action(self, agent, actions, agent_rew, agent_done):

        # assuming moves forward first, then changes angle

        row, col = agent.grid_position
        angle = agent.angle
        next_cell = self.grid_env[int(row), int(col)]

        # agent_actions = actions.get(agent, {})
        agent_actions = actions[agent]

        # MG said use this 26 Mar
        #
        #
        # agent_actions = actions.get(agent, {})
        # Edited
        # agent_actions.get(Actions.ROTATE, 0)

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
            agent_rew = float(Definitions.REWARD_COLLISION.value)
            row_new, col_new = row, col

        elif next_cell == ElementsEnv.BOULDER.value:

            agent_rew = float(Definitions.REWARD_COLLISION.value)
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

        # need to check first if both agents on same tree cell


        if next_cell == ElementsEnv.TREE.value:
            print('going into tree dynamics', agent.color)
            agent_rew = self.tree_dynamics(agent,actions,agent_rew,next_cell,row_new,col_new)




        return agent_rew, agent_done

    #TODO change reward to only if they have space to get logs

    def tree_dynamics(self,agent, actions, agent_rew, next_cell,row_new,col_new):
        if self.both_at_tree:
            print('BOTH AT TREE')
            self.grid_env[int(row_new), int(col_new)] = ElementsEnv.EMPTY.value

            if self.agent_white.wood_logs == 0:
                self.agent_black.wood_logs += 1

        else:
            print('BOTH NOT!!! AT TREE')
            if agent.color == Definitions.BLACK:
                partner_on_cell = self.check_cell_occupancy(agent, actions, next_cell)
                if not partner_on_cell:
                    if agent.wood_logs < 2:
                        agent.wood_logs += 1
                        agent_rew = float(Definitions.REWARD_CUT_TREE.value)
                    self.grid_env[int(row_new), int(col_new)] = ElementsEnv.EMPTY.value

                else:
                    self.both_at_tree = True
                    print('when ag1 is black should look here')
                    if random.random() > 0.5:
                        if agent.wood_logs < 2:
                            agent_rew = float(Definitions.REWARD_CUT_TREE.value)
                            agent.wood_logs += 1
                # agent black gets log if he has less than 2
                # else ag white gets log if he has less than 2
                #self.grid_env[int(row_new), int(col_new)] = ElementsEnv.EMPTY.value

            elif agent.color == Definitions.WHITE:
                partner_on_cell = self.check_cell_occupancy(agent, actions, next_cell)
                if not partner_on_cell:
                    if agent.wood_logs < 2:
                        agent.wood_logs += 1
                        agent_rew = float(Definitions.REWARD_CUT_TREE.value)
                    self.grid_env[int(row_new), int(col_new)] = ElementsEnv.EMPTY.value

                else:
                    self.both_at_tree = True
                    if random.random() > 0.5:
                        if agent.wood_logs < 2:
                            agent_rew = float(Definitions.REWARD_CUT_TREE.value)
                            agent.wood_logs += 1
                # agent black gets log if he has less than 2
                # else ag white gets log if he has less than 2
                #self.grid_env[int(row_new), int(col_new)] = ElementsEnv.EMPTY.value




        return  agent_rew

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

        cells_to_drop = self.check_cross_obstacles(agent) + self.check_diagonal_obstacles(agent)

        # iterate over range
        for obs_range in range(1, agent.range_observation + 1):

            row, col = agent.grid_position
            angle = agent.angle

            # go to start
            for i in range(obs_range):
                row, col, _ = self.get_next_cell(row, col, (angle - 1) % 6)

            if 0 <= row < self.size and 0 <= col < self.size:
                obs.append(self.grid_env[int(row), int(col)])
                if (row, col) in cells_to_drop:
                    obs.remove(self.grid_env[int(row), int(col)])
            else:
                obs.append(0)

            # move first segment
            for i in range(obs_range):
                row, col, _ = self.get_next_cell(row, col, (angle + 1) % 6)

                if 0 <= row < self.size and 0 <= col < self.size:
                    obs.append(self.grid_env[int(row), int(col)])
                    if (row, col) in cells_to_drop:
                        obs.remove(self.grid_env[int(row), int(col)])
                else:
                    obs.append(0)

            # move second segment
            for i in range(obs_range):
                row, col, _ = self.get_next_cell(row, col, (angle + 2) % 6)

                if 0 <= row < self.size and 0 <= col < self.size:
                    obs.append(self.grid_env[int(row), int(col)])
                    if (row, col) in cells_to_drop:
                        obs.remove(self.grid_env[int(row), int(col)])
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
            print('agent is black')

            partner_row, partner_col = self.agent_white.grid_position
            partner_angle = self.agent_white.angle
            partner_actions = actions[self.agent_white]
            partner_rotation = partner_actions[Actions.ROTATE]
            partner_angle = (partner_angle + partner_rotation)
            partner_forward = partner_actions[Actions.FORWARD]
            print('partner_row, partner_col, partner_angle', partner_row, partner_col, partner_angle)

            _, _, partner_next_cell = self.get_proximal_coordinate(partner_row, partner_col, partner_angle)
            print(next_cell , partner_next_cell)
            if partner_next_cell == next_cell:
                self.on_same_cell = True
                return True
            else:
                return False

        elif agent.color == Definitions.WHITE:
            print('agent is white')

            partner_row, partner_col = self.agent_black.grid_position
            partner_angle = self.agent_black.angle
            partner_actions = actions[self.agent_black]
            partner_rotation = partner_actions[Actions.ROTATE]
            partner_angle = (partner_angle + partner_rotation)
            partner_forward = partner_actions[Actions.FORWARD]
            print('partner_row, partner_col, partner_angle', partner_row, partner_col, partner_angle)
            _, _, partner_next_cell = self.get_proximal_coordinate(partner_row, partner_col, partner_angle)
            print(next_cell, partner_next_cell)
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

    def check_cross_obstacles(self, agent):

        row, col = agent.grid_position
        left_cells_to_drop = []
        right_cells_to_drop = []
        bottom_cells_to_drop = []
        top_cells_to_drop = []

        # check directly left
        for i in range(1, agent.range_observation):
            # TODO include other obstacles besides trees
            # while col - i >= 0:
            if self.grid_env[int(row), int(col - i)] == ElementsEnv.TREE.value:
                agent.left_view_obstructed = True
                left_cells_to_drop = self.eliminate_left_view(i, row, col, agent)
                # print('left', cells_to_drop)
                break

        # check directly right
        for j in range(1, agent.range_observation):
            if col + j == self.size:
                break

            if self.grid_env[int(row), int(col + j)] == ElementsEnv.TREE.value:
                agent.right_view_obstructed = True
                right_cells_to_drop = self.eliminate_right_view(j, row, col, agent)
                # print('right', cells_to_drop)
                break

        # check directly below
        for k in range(1, agent.range_observation):
            if row + k == self.size:
                break
            if self.grid_env[int(row + k), int(col)] == ElementsEnv.TREE.value:
                agent.bottom_view_obstructed = True
                bottom_cells_to_drop = self.eliminate_bottom_view(k, row, col, agent)
                # print('below', cells_to_drop)
                break

        # check directly above
        for l in range(1, agent.range_observation):
            # while row - l >= 0:
            if self.grid_env[int(row - l), int(col)] == ElementsEnv.TREE.value:
                agent.top_view_obstructed = True
                top_cells_to_drop = self.eliminate_top_view(l, row, col, agent)
                # print('above', cells_to_drop)
                break

        cells_to_drop = left_cells_to_drop + right_cells_to_drop + bottom_cells_to_drop + top_cells_to_drop
        return cells_to_drop

    def eliminate_right_view(self, start, row, col, agent):
        cells_to_drop = []
        for i in range(start, agent.range_observation):
            coords = (row, col + i)
            cells_to_drop.append(coords)
        return cells_to_drop

    def eliminate_left_view(self, start, row, col, agent):
        cells_to_drop = []
        for i in range(start, agent.range_observation):
            coords = (row, col - i)
            cells_to_drop.append(coords)
        return cells_to_drop

    def eliminate_bottom_view(self, start, row, col, agent):
        cells_to_drop = []
        for i in range(start, agent.range_observation):
            coords = (row + i, col)
            cells_to_drop.append(coords)
        return cells_to_drop

    def eliminate_top_view(self, start, row, col, agent):
        cells_to_drop = []
        for i in range(start, agent.range_observation):
            coords = (row - i, col)
            cells_to_drop.append(coords)
        return cells_to_drop

        # TODO the same as above for diagonals

    def check_diagonal_obstacles(self, agent):

        row, col = agent.grid_position
        top_left_cells_to_drop = []
        top_right_cells_to_drop = []
        bottom_left_cells_to_drop = []
        bottom_right_cells_to_drop = []

        # check top left
        for i in range(1, agent.range_observation):
            for a in range(1, agent.range_observation):
                # TODO include other obstacles besides trees
                # while (row-i) >= 0 and (col-a) >=0:
                if self.grid_env[int(row - i), int(col - a)] == ElementsEnv.TREE.value:
                    agent.top_left_obstructed = True
                    top_left_cells_to_drop = self.eliminate_top_left_view(i, a, row, col, agent)
                    break

        # check top right
        for j in range(1, agent.range_observation):
            for b in range(1, agent.range_observation):
                # while (row - j) >= 0 and (col +b) <= self.size:
                if col + b == self.size:
                    break
                if self.grid_env[int(row - j), int(col + b)] == ElementsEnv.TREE.value:
                    agent.top_right_obstructed = True
                    top_right_cells_to_drop = self.eliminate_top_right_view(j, b, row, col, agent)
                    break

        # check bottom left
        for k in range(1, agent.range_observation):
            for c in range(1, agent.range_observation):
                # while (row +k ) <= self.size and (col - c) >= 0:
                if row + k == self.size:
                    break
                if self.grid_env[int(row + k), int(col - c)] == ElementsEnv.TREE.value:
                    agent.bottom_left_obstructed = True
                    bottom_left_cells_to_drop = self.eliminate_bottom_left_view(k, c, row, col, agent)
                    break

        # check bottom right
        for l in range(1, agent.range_observation):
            for d in range(1, agent.range_observation):
                if col + d == self.size:
                    break
                # while (row + l) <= self.size and (col +d ) <= self.size:
                if self.grid_env[int(row + l), int(col + d)] == ElementsEnv.TREE.value:
                    agent.bottom_right_obstructed = True
                    bottom_right_cells_to_drop = self.eliminate_bottom_right_view(l, d, row, col, agent)

                    break

        cells_to_drop = top_left_cells_to_drop + top_right_cells_to_drop + bottom_left_cells_to_drop + bottom_right_cells_to_drop
        return cells_to_drop

    def eliminate_top_left_view(self, start_row, start_col, row, col, agent):
        cells_to_drop = []
        for i in range(start_row, agent.range_observation):
            col = start_col
            coords = (row - i, col)
            cells_to_drop.append(coords)
        for a in range(start_col, agent.range_observation):
            row = start_row
            coords = (row, col - a)
            cells_to_drop.append(coords)
        for i in range(0, agent.range_observation):
            for a in range(0, agent.range_observation):
                coords = (start_row - i, start_col - a)
                cells_to_drop.append(coords)
        return cells_to_drop

    def eliminate_top_right_view(self, start_row, start_col, row, col, agent):
        cells_to_drop = []
        for i in range(start_row, agent.range_observation):
            col = start_col
            coords = (row - i, col)
            cells_to_drop.append(coords)
        for a in range(start_col, agent.range_observation):
            row = start_row
            coords = (row, col + a)
            cells_to_drop.append(coords)
        for i in range(0, agent.range_observation):
            for  a in range(0, agent.range_observation):
                if start_col + a == self.size:
                    break
                coords = (start_row - i, start_col + a)
                cells_to_drop.append(coords)
        return cells_to_drop

    def eliminate_bottom_left_view(self, start_row, start_col, row, col, agent):
        cells_to_drop = []
        for i in range(start_row, agent.range_observation):
            col = start_col
            coords = (row + i, col)
            cells_to_drop.append(coords)
        for a in range(start_col, agent.range_observation):
            row = start_row
            coords = (row, col - a)
            cells_to_drop.append(coords)
        for i in range(0, agent.range_observation):
            for a in range(0, agent.range_observation):
                if start_row + i == self.size:
                    break
                coords = (start_row + i, start_col - a)
                cells_to_drop.append(coords)
        return cells_to_drop

    def eliminate_bottom_right_view(self, start_row, start_col, row, col, agent):
        cells_to_drop = []
        for i in range(start_row, agent.range_observation):
            col = start_col
            coords = (row + i, col)
            cells_to_drop.append(coords)
        for a in range(start_col, agent.range_observation):
            row = start_row
            coords = (row, col + a)
            cells_to_drop.append(coords)
        for i in range(0, agent.range_observation):
            for a in range(0, agent.range_observation):
                if start_col + a == self.size:
                    break
                if start_row + i == self.size:
                    break
                coords = (start_row + i, start_col + a)
                cells_to_drop.append(coords)
        return cells_to_drop
