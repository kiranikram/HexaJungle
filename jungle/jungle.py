import numpy as np
import random
import math

from collections import namedtuple

from jungle.utils import ElementsEnv, Actions, Definitions
from jungle.observations import restrict_observations

Exit = namedtuple('Exit', ['coordinates', 'surrounding_1', 'surrounding_2'])


class EmptyJungle:

    def __init__(self, size):

        # self.size = config['size']
        self.size = size

        if self.size % 2 == 0 or size < Definitions.MIN_SIZE_ENVIR.value:
            raise ValueError('size should be an odd number')

        # Initialize with empty values
        self.grid_env = np.ones((self.size, self.size), dtype=int) * ElementsEnv.EMPTY.value
        self.place_obstacles()

        self.agent_white = None
        self.agent_black = None

        self.exit_top_left = None
        self.exit_bottom_left = None
        self.exit_top_right = None
        self.exit_bottom_right = None
        self.calculate_exit_coordinates()

        self.list_selected_exits = [
            self.exit_top_left,
            self.exit_bottom_right,
            self.exit_top_right,
            self.exit_bottom_left,
        ]

        self.tree_coordinates = None
        self.determine_tree_locations()
        self.add_trees()

    @property
    def agents(self):
        return [self.agent_white, self.agent_white]

    def place_obstacles(self):

        # place outside walls
        self.grid_env[:, 0] = ElementsEnv.OBSTACLE.value
        self.grid_env[:, -1] = ElementsEnv.OBSTACLE.value
        self.grid_env[0, :] = ElementsEnv.OBSTACLE.value
        self.grid_env[-1, :] = ElementsEnv.OBSTACLE.value

        # add corners
        for row in range(2, self.size - 2, 2):
            self.grid_env[row, 1] = ElementsEnv.OBSTACLE.value

    def calculate_exit_coordinates(self):

        self.exit_top_left = Exit((1, 1), (1, 2), (2, 2))
        self.exit_bottom_left = Exit((self.size - 2, 1),
                                     (self.size - 2, 2),
                                     (self.size - 3, 2))
        self.exit_top_right = Exit((1, self.size - 2),
                                   (1, self.size - 3),
                                   (2, self.size - 2))
        self.exit_bottom_right = Exit((self.size - 2, self.size - 2),
                                      (self.size - 2, self.size - 3),
                                      (self.size - 3, self.size - 2))

    def determine_tree_locations(self):

        # trees must not be on any exit coordinates
        # trees must not be where agents are
        trees = []
        for row in range(2, self.size - 2):
            for col in range(2, self.size - 2):
                trees.append((row, col))
        agent_1_location = int((self.size - 1) / 2), int((self.size - 1) / 2 - 1)

        trees.remove(agent_1_location)
        agent_2_location = int((self.size - 1) / 2), int((self.size - 1) / 2 + 1)

        trees.remove(agent_2_location)

        no_of_trees = math.floor(self.size / 2)
        no_of_trees = no_of_trees + 1
        self.tree_coordinates = random.sample(trees, no_of_trees)

    def add_trees(self):

        for location in self.tree_coordinates:
            self.add_object(ElementsEnv.TREE, location)

    def select_random_exit(self):

        """ Picks a random exit. """

        random.shuffle(self.list_selected_exits)

        if not self.list_selected_exits:
            raise ValueError('All exits have already been selected')

        return self.list_selected_exits.pop(0)

    def __repr__(self):

        full_repr = ""

        for r in range(self.size):
            if r % 2 == 0:
                line = ""
            else:
                line = "{0:1}".format("")

            for c in range(self.size):
                repr = str(self.grid_env[r, c])

                line += "{0:2}".format(repr)

            full_repr += line + "\n"

        return full_repr

    def add_agents(self, agent_1, agent_2):

        # Agent 1 always start on the left.
        agent_1.grid_position = int((self.size - 1) / 2), int((self.size - 1) / 2 - 1)
        agent_1.angle = 3

        agent_2.grid_position = int((self.size - 1) / 2), int((self.size - 1) / 2 + 1)
        agent_2.angle = 0

        # flip a coin to decide who is black or white
        if random.random() > 0.5:
            self.agent_black = agent_1
            self.agent_white = agent_2

        else:
            self.agent_black = agent_2
            self.agent_white = agent_1

        self.agent_black.color = Definitions.BLACK
        self.agent_white.color = Definitions.WHITE

        self.agent_black.done = False
        self.agent_white.done = False

        self.agent_white.starting_position = self.agent_white.grid_position
        self.agent_white.starting_angle = self.agent_white.angle

        self.agent_black.starting_position = self.agent_black.grid_position
        self.agent_black.starting_angle = self.agent_black.angle

    def reset(self):

        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def reinitialize_grid(self):
        self.grid_env[:] = np.ones((self.size, self.size), dtype=int) * ElementsEnv.EMPTY.value

        self.place_obstacles()
        # self.add_trees()

    def swap_agent_positions(self):
        self.agent_white.grid_position = self.agent_black.starting_position
        self.agent_white.angle = self.agent_black.starting_angle

        self.agent_black.grid_position = self.agent_white.starting_position
        self.agent_black.angle = self.agent_white.starting_angle

    def step(self, actions):
        print(actions)

        # First Physical move
        if not self.agent_white.done:
            rew_white = self.move(self.agent_white, actions)
            white_climbs = actions.get(self.agent_white, {}).get(Actions.CLIMB, 0)
        else:
            rew_white = 0
            white_climbs = False

        if not self.agent_black.done:
            rew_black = self.move(self.agent_black, actions)
            black_climbs = actions.get(self.agent_black, {}).get(Actions.CLIMB, 0)
        else:
            rew_black = 0
            black_climbs = False

        # Then Test for different cases

        # If both on same position:
        # This will be false if one agent is done

        if self.agent_white.grid_position == self.agent_black.grid_position:

            r, c = self.agent_white.grid_position

            # TREE
            if self.grid_env[r, c] == ElementsEnv.TREE.value:
                # If they are on a tree they cut it
                self.grid_env[r, c] = ElementsEnv.EMPTY.value

                # one of them only gets the log
                if random.random() > 0.5:
                    self.agent_black.wood_logs += 1
                else:
                    self.agent_white.wood_logs += 1

                # But both have neg reward from the effort
                rew_white += Definitions.REWARD_CUT_TREE.value
                rew_black += Definitions.REWARD_CUT_TREE.value

            # RIVER
            if self.grid_env[r, c] == ElementsEnv.RIVER.value:

                # If they have enough logs they build a bridge
                if self.agent_white.wood_logs + self.agent_black.wood_logs == 4:
                    self.agent_white.wood_logs = 0
                    self.agent_black.wood_logs = 0
                    self.grid_env[r, c] = ElementsEnv.EMPTY.value
                    rew_black += Definitions.REWARD_BUILT_BRIDGE.value
                    rew_white += Definitions.REWARD_BUILT_BRIDGE.value

                # else they will drown, but we will see that later.
                else:
                    self.agent_white.done = True
                    # @MG white was repeated, so changed to black
                    self.agent_black.done = True
                    rew_white += Definitions.REWARD_DROWN.value
                    rew_black += Definitions.REWARD_DROWN.value
                    print('agents drowned')

            # BOULDER

            if self.grid_env[r, c] == ElementsEnv.BOULDER.value:
                # if one agent is on shoulders, they can cross
                if self.agent_white.on_shoulders or self.agent_black.on_shoulders:
                    rew_white += Definitions.REWARD_CROSS_BOULDER.value
                    rew_black += Definitions.REWARD_CROSS_BOULDER.value

            # CLIMB Behavior if they are on the same cell

            if white_climbs and not black_climbs:
                self.agent_white.on_shoulders = True
                rew_black += Definitions.REWARD_CARRYING.value
                print('ag white carrying')

            elif black_climbs and not white_climbs:
                self.agent_black.on_shoulders = True
                rew_white += Definitions.REWARD_CARRYING.value
                print('ag black carrying')

            elif black_climbs and white_climbs:
                rew_white += Definitions.REWARD_FELL.value
                rew_black += Definitions.REWARD_FELL.value
                print('agents fell')

        # If not on the same cell
        else:

            # If agent was on shoulders, but other agent moved:
            if self.agent_black.on_shoulders:
                self.agent_black.on_shoulders = False
                rew_black += Definitions.REWARD_FELL.value
                print('black fell')

            if self.agent_white.on_shoulders:
                self.agent_white.on_shoulders = False
                rew_white += Definitions.REWARD_FELL.value
                print('white fell')

            # If try to climb, fails
            if black_climbs:
                rew_black += Definitions.REWARD_FELL.value
                print('black fell')

            if white_climbs:
                rew_white += Definitions.REWARD_FELL.value
                print('white fell')

        # Apply environment rules

        if not self.agent_black.done:
            rew, self.agent_black.done = self.apply_rules(self.agent_black)
            rew_black += rew

        if not self.agent_white.done:
            rew, self.agent_white.done = self.apply_rules(self.agent_white)
            rew_white += rew

        # All rewards and terminations are now calculated
        rewards = {'black': rew_black, 'white': rew_white}

        if self.agent_white.done:
            print('ag white done')

        if self.agent_black.done:
            print('ag black done')

        if self.agent_white.done and self.agent_black.done:
            done = dict({"__all__": True})
        elif self.agent_white.done and not self.agent_black.done:
            done = dict({"white": True, "__all__": False})
        elif self.agent_black.done and not self.agent_white.done:
            done = dict({"black": True, "__all__": False})
        else:
            done = dict({"__all__": False})

        # Now we calculate the observations
        obs = {}
        # obs[self.agent_white] = []#self.generate_agent_obs(self.agent_white)
        # obs[self.agent_black] = []#self.generate_agent_obs(self.agent_black)
        # if not self.agent_white.done:
        # obs[self.agent_white] = self.generate_agent_obs(self.agent_white)
        # if not self.agent_black.done:
        # obs[self.agent_black] = self.generate_agent_obs(self.agent_black)

        if not self.agent_white.done:
            obs['white'] = self.generate_agent_obs(self.agent_white)
            self.agent_white.last_obs = self.generate_agent_obs(self.agent_white)
        else:
            obs['white'] = self.agent_white.last_obs

        if not self.agent_black.done:
            obs['black'] = self.generate_agent_obs(self.agent_black)
            self.agent_black.last_obs = self.generate_agent_obs(self.agent_white)
        else:
            obs['black'] = self.agent_black.last_obs

        print('*************')
        print('at this step agent white :')
        print(self.agent_white.grid_position, 'and reward:', rew_white)
        print('at this step agent black :')
        print(self.agent_black.grid_position, 'and reward:', rew_black)
        return obs, rewards, done

    def apply_rules(self, agent):

        rew = 0

        # If on a tree, cut log
        agent_cuts = self.cutting_tree(agent)
        if agent_cuts:
            agent.wood_logs += 1
            rew += Definitions.REWARD_CUT_TREE.value

        # If on a river, drown
        agent_drowns = self.on_a_river(agent)
        if agent_drowns:
            rew += Definitions.REWARD_DROWN.value
            print('agent drowns')

        # If comes to boulder and not on shoulders, bumps into boulder
        bumps_boulder = self.hits_boulder(agent)
        if bumps_boulder:
            rew += Definitions.REWARD_COLLISION.value

        # If on an exit, receive reward and is done
        r, agent_exits = self.exits(agent)
        rew += r

        agent_done = agent_exits or agent_drowns or bumps_boulder

        return rew, agent_done

    def cutting_tree(self, agent):
        r, c = agent.grid_position

        if self.cell_type(r, c) == ElementsEnv.TREE.value:
            # If they are on a tree they cut it
            self.grid_env[r, c] = ElementsEnv.EMPTY.value
            return True
        return False

    def on_a_river(self, agent):
        r, c = agent.grid_position
        if self.cell_type(r, c) == ElementsEnv.RIVER.value:
            return True
        return False

    def hits_boulder(self, agent):
        r, c = agent.grid_position
        if self.cell_type(r, c) == ElementsEnv.BOULDER.value:
            return True
        return False

    def exits(self, agent):

        r, c = agent.grid_position
        current_cell = self.cell_type(r, c)

        done = True

        if current_cell == ElementsEnv.EXIT_BLACK.value and agent.color == Definitions.BLACK:
            reward = Definitions.REWARD_EXIT_VERY_HIGH.value

        elif current_cell == ElementsEnv.EXIT_BLACK.value and agent.color == Definitions.WHITE:
            reward = Definitions.REWARD_EXIT_LOW.value

        elif current_cell == ElementsEnv.EXIT_WHITE.value and agent.color == Definitions.WHITE:
            reward = Definitions.REWARD_EXIT_VERY_HIGH.value

        elif current_cell == ElementsEnv.EXIT_WHITE.value and agent.color == Definitions.BLACK:
            reward = Definitions.REWARD_EXIT_LOW.value

        elif current_cell == ElementsEnv.EXIT_EASY.value:
            reward = Definitions.REWARD_EXIT_AVERAGE.value
            print('%%%%%%%%%%%%%%%%%%')

            print('easy exit reward')
            print('%%%%%%%%%%%%%%%%%%')


        elif current_cell == ElementsEnv.EXIT_DIFFICULT.value:
            reward = Definitions.REWARD_EXIT_HIGH.value
            print('££££££££££££££££££££')
            print('££££££££££££££££££££')
            print('DIFFICULT exit reward')
            print('££££££££££££££££££££')
            print('££££££££££££££££££££')

        # if we are not on an exit
        else:
            reward = 0
            done = False

        return reward, done

    def move(self, agent, actions):

        reward = 0

        action_dict = actions.get(agent, {})
        rotation = action_dict.get(Actions.ROTATE, 0)
        forward = action_dict.get(Actions.FORWARD, 0)

        # First, change angle
        # the modulo is taken care of in the agent property
        agent.angle += rotation

        # Then move forward

        # In order to move forward, we first check the destinations cell

        row, col = agent.grid_position
        current_cell = self.cell_type(row, col)

        # If we don't move forward nothing happens
        if forward == 0:
            return 0

        # Else we see where we go
        row_new, col_new = self.get_proximal_coordinate(row, col, agent.angle)

        next_cell = self.cell_type(row_new, col_new)

        # If we were on a boulder, we can move to boulders or empty cells or trees or exits.
        # We collide only if we go toward an obstacle.
        if current_cell == ElementsEnv.BOULDER.value:

            if next_cell == ElementsEnv.OBSTACLE.value:
                reward = Definitions.REWARD_COLLISION.value
                row_new, col_new = row, col

        # If we were on the ground, we move unless we face a boulder or obstacle
        else:

            # Check if next cell is an obstacle, we don't move
            if next_cell == ElementsEnv.OBSTACLE.value:
                reward = Definitions.REWARD_COLLISION.value
                row_new, col_new = row, col

            # Check if next cell is a boulder
            elif next_cell == ElementsEnv.BOULDER.value:

                # If not on shoulders, we collide
                if not agent.on_shoulders:
                    reward = Definitions.REWARD_COLLISION.value
                    row_new, col_new = row, col

                # Else we move to boulders, and starting then we can go from boulder to boulder

        # Whatever happens, if we move forward, we are not on shoulders anymore
        agent.on_shoulders = False

        # Now that we now if we can move or not, we change position
        agent.grid_position = row_new, col_new

        return reward

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

        return row_new, col_new

    def generate_agent_obs(self, agent):

        obs = []
        obs_coordinates = []
        obstacles = []

        # cells_to_drop = self.check_cross_obstacles(agent) + self.check_diagonal_obstacles(agent)

        # iterate over range
        if agent.range_observation is None:
            agent.range_observation = 4
        for obs_range in range(1, agent.range_observation + 1):

            row, col = agent.grid_position

            angle = agent.angle

            if row not in range(1, self.size - 2) or col not in range(1, self.size - 2):
                obs.append(0)
            else:

                # go to start
                for i in range(obs_range):
                    row, col, _ = self.get_next_cell(row, col, (angle - 1) % 6)

                if 0 <= row < self.size and 0 <= col < self.size:
                    obs.append(self.grid_env[int(row), int(col)])
                    obs_coordinates.append((row, col))

                # if not agent.on_shoulders:
                # if (row, col) in cells_to_drop:
                # obs.remove(self.grid_env[int(row), int(col)])
                else:
                    obs.append(0)

                # move first segment
                for i in range(obs_range):

                    row, col, _ = self.get_next_cell(row, col, (angle + 1) % 6)

                    if 0 <= row < self.size and 0 <= col < self.size:
                        obs.append(self.grid_env[int(row), int(col)])
                        obs_coordinates.append((row, col))

                    # if not agent.on_shoulders:
                    # if (row, col) in cells_to_drop:
                    # obs.remove(self.grid_env[int(row), int(col)])

                    else:
                        obs.append(0)

                # move second segment
                for i in range(obs_range):

                    row, col, _ = self.get_next_cell(row, col, (angle + 2) % 6)

                    if 0 <= row < self.size and 0 <= col < self.size:
                        obs.append(self.grid_env[int(row), int(col)])
                        obs_coordinates.append((row, col))

                    # if not agent.on_shoulders:
                    # if (row, col) in cells_to_drop:
                    # obs.remove(self.grid_env[int(row), int(col)])

                    else:
                        obs.append(0)

        for i in obs_coordinates:

            current_cell = self.cell_type(i[0], i[1])
            if current_cell == ElementsEnv.TREE.value or current_cell == ElementsEnv.RIVER.value \
                    or current_cell == ElementsEnv.BOULDER.value:
                obstacles.append((i[0], i[1]))

        cells_to_drop = restrict_observations(agent, obstacles)

        if not agent.on_shoulders:
            for i in obs_coordinates:
                if i in cells_to_drop:
                    r_row = i[0]
                    r_col = i[1]

                    obs.remove(self.grid_env[int(r_row), int(r_col)])

        if len(obs) < 15:
            obs += [0] * (15 - len(obs))

        if agent == self.agent_white:
            obs.append(ElementsEnv.AGENT_WHITE.value)
        else:
            obs.append(ElementsEnv.AGENT_BLACK.value)

        obs = np.asarray(obs)

        env_elements = len(ElementsEnv) + 1

        one_hot_obs = np.eye(env_elements)[obs]
        one_hot_obs = list(one_hot_obs.flat)

        return one_hot_obs

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

        elif agent.color == Definitions.WHITE:

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

    def check_cross_obstacles(self, agent):

        row, col = agent.grid_position
        cells_to_drop = []

        # check directly left
        for i in range(1, agent.range_observation):
            # TODO include other obstacles besides trees
            if self.grid_env[int(row), int(col - i)] == ElementsEnv.TREE.value:
                agent.left_view_obstructed = True
                cells_to_drop.append(self.eliminate_left_view(i, row, col, agent))
                break

        # check directly right
        for j in range(1, agent.range_observation):
            if col + j == self.size:
                break
            if self.grid_env[int(row), int(col + j)] == ElementsEnv.TREE.value:
                agent.right_view_obstructed = True
                cells_to_drop.append(self.eliminate_right_view(j, row, col, agent))
                break

        # check directly below
        for k in range(1, agent.range_observation):
            if row + k == self.size:
                break
            if self.grid_env[int(row + k), int(col)] == ElementsEnv.TREE.value:
                agent.bottom_view_obstructed = True
                cells_to_drop.append(self.eliminate_bottom_view(k, row, col, agent))
                break

        # check directly above
        for l in range(1, agent.range_observation):
            if self.grid_env[int(row - l), int(col)] == ElementsEnv.TREE.value:
                agent.top_view_obstructed = True
                cells_to_drop.append(self.eliminate_top_view(l, row, col, agent))
                break

        return cells_to_drop

    def eliminate_right_view(self, start, row, col, agent):
        cells_to_drop = []
        for i in range(start, agent.range_observation):
            cells_to_drop.append((row, col + i))
        return cells_to_drop

    def eliminate_left_view(self, start, row, col, agent):
        cells_to_drop = []
        for i in range(start, agent.range_observation):
            cells_to_drop.append((row, col - i))
        return cells_to_drop

    def eliminate_bottom_view(self, start, row, col, agent):
        cells_to_drop = []
        for i in range(start, agent.range_observation):
            cells_to_drop.append((row + i, col))
        return cells_to_drop

    def eliminate_top_view(self, start, row, col, agent):
        cells_to_drop = []
        for i in range(start, agent.range_observation):
            cells_to_drop.append((row - i, col))
        return cells_to_drop

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

                if self.grid_env[int(row - i), int(col - a)] == ElementsEnv.TREE.value:
                    agent.top_left_obstructed = True
                    top_left_cells_to_drop = self.eliminate_top_left_view(i, a, row, col, agent)

                    break

        # check top right
        for j in range(1, agent.range_observation):
            for b in range(1, agent.range_observation):

                if col + b == self.size:
                    break
                if self.grid_env[int(row - j), int(col + b)] == ElementsEnv.TREE.value:
                    agent.top_right_obstructed = True
                    top_right_cells_to_drop = self.eliminate_top_right_view(j, b, row, col, agent)

                    break

        # check bottom left
        for k in range(1, agent.range_observation):
            for c in range(1, agent.range_observation):

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

                if self.grid_env[int(row + l), int(col + d)] == ElementsEnv.TREE.value:
                    agent.bottom_right_obstructed = True
                    bottom_right_cells_to_drop = self.eliminate_bottom_right_view(l, d, row, col, agent)

                    break

        cells_to_drop = top_left_cells_to_drop + top_right_cells_to_drop + bottom_left_cells_to_drop + bottom_right_cells_to_drop

        return cells_to_drop

    def eliminate_top_left_view(self, start_rows, start_cols, row, col, agent):
        cells_to_drop = []
        row = row + start_rows
        col = col - start_cols
        for i in range(1, agent.range_observation):
            coords = (row - i, col)
            cells_to_drop.append(coords)
        for a in range(1, agent.range_observation):
            coords = (row, col - a)
            cells_to_drop.append(coords)
        for i in range(0, agent.range_observation):
            for a in range(0, agent.range_observation):
                coords = (row - i, col - a)
                cells_to_drop.append(coords)
        return cells_to_drop

    def eliminate_top_right_view(self, start_rows, start_cols, row, col, agent):
        cells_to_drop = []
        row = row + start_rows
        col = col - start_cols
        for i in range(1, agent.range_observation):
            coords = (row - i, col)
            cells_to_drop.append(coords)
        for a in range(1, agent.range_observation):
            coords = (row, col + a)
            cells_to_drop.append(coords)
        for i in range(1, agent.range_observation):
            for a in range(1, agent.range_observation):
                if col + a == self.size:
                    break
                coords = (row - i, col + a)
                cells_to_drop.append(coords)

        return cells_to_drop

    def eliminate_bottom_left_view(self, start_rows, start_cols, row, col, agent):
        cells_to_drop = []
        row = row + start_rows
        col = col - start_cols
        for i in range(1, agent.range_observation):
            coords = (row + i, col)
            cells_to_drop.append(coords)
        for a in range(1, agent.range_observation):
            coords = (row, col - a)
            cells_to_drop.append(coords)
        for i in range(1, agent.range_observation):
            for a in range(1, agent.range_observation):
                if row + i == self.size:
                    break
                coords = (row + i, col - a)
                cells_to_drop.append(coords)

        return cells_to_drop

    def eliminate_bottom_right_view(self, start_rows, start_cols, row, col, agent):
        cells_to_drop = []
        row = row + start_rows
        col = col - start_cols
        for i in range(1, agent.range_observation):
            coords = (row + i, col)
            cells_to_drop.append(coords)
        for a in range(1, agent.range_observation):
            coords = (row, col + a)
            cells_to_drop.append(coords)
        for i in range(1, agent.range_observation):
            for a in range(1, agent.range_observation):
                if col + a == self.size:
                    break
                if row + i == self.size:
                    break
                coords = (row + i, col + a)
                cells_to_drop.append(coords)
        return cells_to_drop
