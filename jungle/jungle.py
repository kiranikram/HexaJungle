"""
jungle.py provides the Jungle base class.
Jungle deals with environment creation and interactions between agents 
and elements.
"""

from inspect import Signature
from typing import Tuple, Union, List

from abc import ABC, abstractmethod
from copy import deepcopy
import random
import math

from collections import namedtuple

import numpy as np
from skimage.draw import polygon, polygon_perimeter

from jungle.agent import Agent
from jungle.utils import (ElementsEnv, Actions, Rewards, str_dict,
                          display_dict, MIN_SIZE_ENVIR, MAX_WOOD_LOGS, BLACK,
                          WHITE)

SIZE_HEX = 40

Exit = namedtuple('Exit', ['coordinates', 'surrounding_1', 'surrounding_2'])


class Jungle(ABC):
    def __init__(self, size: int):

        self.size = size
        if self.size % 2 == 0 or size < MIN_SIZE_ENVIR:
            raise ValueError('size should be an odd number')

        # Initialize with empty values
        self.grid_env = np.ones((self.size, self.size), dtype=int)
        self.grid_env *= ElementsEnv.EMPTY.value

        # Placeholders for agents
        self.agents: List[Agent] = []

        # Set starting_positions
        pos_1 = int((self.size - 1) / 2), int((self.size - 1) / 2 - 1)
        angle_1 = 3
        self._starting_coordinates_1 = pos_1, angle_1

        pos_2 = int((self.size - 1) / 2), int((self.size - 1) / 2 + 1)
        angle_2 = 0
        self._starting_coordinates_2 = pos_2, angle_2

        # Set borders of environment
        self._set_boundaries()

        # Set elements
        self._set_elements()

        # Set Exits
        self._calculate_exit_coordinates()
        self._set_exits()

        # Save the initial grid to reset to original state
        self._initial_grid = deepcopy(self.grid_env)

    def _set_boundaries(self):

        # place outside walls
        self.grid_env[:, 0] = ElementsEnv.OBSTACLE.value
        self.grid_env[:, -1] = ElementsEnv.OBSTACLE.value
        self.grid_env[0, :] = ElementsEnv.OBSTACLE.value
        self.grid_env[-1, :] = ElementsEnv.OBSTACLE.value

        # add corners
        for row in range(2, self.size - 2, 2):
            self.grid_env[row, 1] = ElementsEnv.OBSTACLE.value

    @abstractmethod
    def _set_exits(self):
        pass

    @abstractmethod
    def _set_elements(self):
        pass

    def display(self):

        width_img = int(SIZE_HEX * math.sqrt(3) * (self.size))
        height_img = int(SIZE_HEX * (3 / 2. * self.size + 1 / 2.))

        img = np.zeros((height_img, width_img, 3))
        img[:, :, :] = [150, 250, 150]

        for row in range(self.size):

            center_x = (1 + 1.5 * row) * SIZE_HEX

            for col in range(self.size):
                elem = self.grid_env[row, col]

                center_y = math.sqrt(3) * (col)

                if row % 2 == 1:
                    center_y += math.sqrt(3) / 2.

                center_y *= SIZE_HEX

                if not (row % 2 == 0 and col == 0):
                    self._draw_hexa_element(img, (center_x, center_y), elem)

        agent_1, agent_2 = self.agents

        self._draw_agent(img, agent_1)
        self._draw_agent(img, agent_2)

        return img

    def _draw_hexa_element(self, img, center, element):

        edge_angles = [math.pi / 3 * (edge_index) for edge_index in range(6)]
        edges = [(SIZE_HEX * math.cos(angle), SIZE_HEX * math.sin(angle))
                 for angle in edge_angles]
        edges_r = [x + center[0] for x, _ in edges]
        edges_c = [y + center[1] for _, y in edges]

        rows, cols = polygon(edges_r, edges_c, img.shape)

        if element in [
                ElementsEnv.EXIT_BLACK.value, ElementsEnv.EXIT_WHITE.value,
                ElementsEnv.EXIT_EASY.value, ElementsEnv.EXIT_DIFFICULT.value
        ]:

            # Draw background for exit
            color = [255, 0, 0]
            img[rows, cols, :] = color

            # Draw inside for type of exit
            edges = [(SIZE_HEX / 2 * math.cos(angle),
                      SIZE_HEX / 2 * math.sin(angle)) for angle in edge_angles]
            edges_r_in = [x + center[0] for x, _ in edges]
            edges_c_in = [y + center[1] for _, y in edges]

            rows_in, cols_in = polygon(edges_r_in, edges_c_in, img.shape)

            img[rows_in, cols_in, :] = display_dict[element]

        else:
            img[rows, cols, :] = display_dict[element]

        rows_per, cols_per = polygon_perimeter(edges_r, edges_c, img.shape)
        img[rows_per, cols_per, :] = [0, 0, 0]

    def _draw_agent(self, img, agent):

        r, c = agent.position
        color = agent.color

        center_x = (1 + 1.5 * r) * SIZE_HEX

        center_y = math.sqrt(3) * c
        if r % 2 == 1:
            center_y += math.sqrt(3) / 2.
            center_y *= SIZE_HEX

        edge_angles = [
            math.pi / 2 - agent.angle * math.pi / 3 + 2 * math.pi / 3 *
            (edge_index) for edge_index in range(3)
        ]
        edges = [(SIZE_HEX / 2 * math.cos(angle),
                  SIZE_HEX / 2 * math.sin(angle)) for angle in edge_angles]

        edges_r = [x + center_x for x, _ in edges]
        edges_c = [y + center_y for _, y in edges]

        rows, cols = polygon(edges_r, edges_c, img.shape)

        img[rows, cols, :] = 255 * color

    def _calculate_exit_coordinates(self):

        self._exits = []

        self._exit_top_left = Exit((1, 1), (1, 2), (2, 2))
        self._exits.append(self._exit_top_left)

        self._exit_bottom_left = Exit((self.size - 2, 1), (self.size - 2, 2),
                                      (self.size - 3, 2))
        self._exits.append(self._exit_bottom_left)

        self._exit_top_right = Exit((1, self.size - 2), (1, self.size - 3),
                                    (2, self.size - 2))
        self._exits.append(self._exit_top_right)

        self._exit_bottom_right = Exit((self.size - 2, self.size - 2),
                                       (self.size - 2, self.size - 3),
                                       (self.size - 3, self.size - 2))
        self._exits.append(self._exit_bottom_right)

    def get_random_empty_location(self):

        grid = deepcopy(self.grid_env)

        # Avoid locations where agent is
        for agent in self.agents:
            if agent.position:
                grid[agent.position] = ElementsEnv.OBSTACLE.value

        # Avoid starting positions
        grid[self._starting_coordinates_1[0]] = ElementsEnv.OBSTACLE.value
        grid[self._starting_coordinates_2[0]] = ElementsEnv.OBSTACLE.value

        # Take all empty cells
        rows, cols = np.where(grid == ElementsEnv.EMPTY.value)

        # return one of them
        index = random.randint(0, len(rows) - 1)

        assert grid[rows[index], cols[index]] == ElementsEnv.EMPTY.value

        return rows[index], cols[index]

    def select_random_exit(self):
        """ Picks a random exit. """

        random.shuffle(self._exits)

        if not self._exits:
            raise ValueError('All exits have already been selected')

        return self._exits.pop(0)

    def __repr__(self):

        full_repr = ""

        for row in range(self.size):
            if row % 2 == 0:
                line = ""
            else:
                line = "{0:2}".format("")

            for col in range(self.size):

                if self.agents[0].position == (row, col):
                    line_repr = str(self.agents[0])

                elif self.agents[1].position == (row, col):
                    line_repr = str(self.agents[1])

                else:
                    element = self.grid_env[row, col]
                    line_repr = str_dict[element]

                line += "{0:3}".format(line_repr)

            full_repr += line + "\n"

        return full_repr

    def add_agents(self, agent_1, agent_2, random_position=True):

        self.agents = [agent_1, agent_2]

        self._place_agents(random_position)
        self._assign_colors()

        agent_1.reset()
        agent_2.reset()

    def _place_agents(self, random_position=True):

        if not random_position:
            self.agents[0].position, self.agents[
                0].angle = self._starting_coordinates_1
            self.agents[1].position, self.agents[
                1].angle = self._starting_coordinates_2
            return

        if random.random() > 0.5:
            self.agents[0].position, self.agents[
                0].angle = self._starting_coordinates_1
            self.agents[1].position, self.agents[
                1].angle = self._starting_coordinates_2

        else:
            self.agents[0].position, self.agents[
                0].angle = self._starting_coordinates_2
            self.agents[1].position, self.agents[
                1].angle = self._starting_coordinates_1

    def _assign_colors(self):

        if random.random() > 0.5:
            self.agents[0].color = BLACK
            self.agents[1].color = WHITE

        else:
            self.agents[0].color = WHITE
            self.agents[1].color = BLACK

    def reset(self):

        # Reset grid to initial state
        self.grid_env[:] = deepcopy(self._initial_grid)

        self._place_agents()
        self._assign_colors()

        self.agents[0].reset()
        self.agents[1].reset()

        obs = {
            self.agents[0]: self.generate_agent_obs(self.agents[0]),
            self.agents[1]: self.generate_agent_obs(self.agents[1])
        }

        return obs

    def step(self, actions):

        # First Physical move

        if not self.agents[0].done:
            rew_0 = self.move(self.agents[0], actions)
            agent_0_climbs = actions.get(self.agents[0],
                                         {}).get(Actions.CLIMB, 0)
        else:
            rew_0 = 0
            agent_0_climbs = False

        if not self.agents[1].done:
            rew_1 = self.move(self.agents[1], actions)
            agent_1_climbs = actions.get(self.agents[1],
                                         {}).get(Actions.CLIMB, 0)
        else:
            rew_1 = 0
            agent_1_climbs = False

        # If None are done, check interactions btween agents
        if self.agents[0].position == self.agents[1].position and self.agents[
                0].position:

            row, col = self.agents[0].position

            # TREE
            if self.grid_env[row, col] == ElementsEnv.TREE.value:

                # If they are on a tree they cut it
                self.grid_env[row, col] = ElementsEnv.EMPTY.value

                # one of them only gets the log
                if random.random() > 0.5:
                    self.agents[1].wood_logs += 1
                else:
                    self.agents[0].wood_logs += 1

                # But both have neg reward from the effort
                rew_0 += Rewards.REWARD_CUT_TREE.value
                rew_1 += Rewards.REWARD_CUT_TREE.value

            # RIVER
            if self.grid_env[row, col] == ElementsEnv.RIVER.value:

                # If they have enough logs they build a bridge
                if self.agents[0].wood_logs + self.agents[
                        1].wood_logs == 2 * MAX_WOOD_LOGS:
                    self.agents[0].wood_logs = 0
                    self.agents[1].wood_logs = 0
                    self.grid_env[row, col] = ElementsEnv.EMPTY.value

            # CLIMB Behavior if they are on the same cell
            if agent_0_climbs and not agent_1_climbs:
                self.agents[0].on_shoulders = True
                rew_1 += Rewards.REWARD_CARRYING.value

            elif agent_1_climbs and not agent_0_climbs:
                self.agents[1].on_shoulders = True
                rew_0 += Rewards.REWARD_CARRYING.value

            elif agent_1_climbs and agent_0_climbs:
                rew_0 += Rewards.REWARD_FELL.value
                rew_1 += Rewards.REWARD_FELL.value

        # If not on the same cell
        else:

            # If agent was on shoulders, but other agent moved:
            if self.agents[1].on_shoulders:
                self.agents[1].on_shoulders = False
                rew_1 += Rewards.REWARD_FELL.value

            if self.agents[0].on_shoulders:
                self.agents[0].on_shoulders = False
                rew_0 += Rewards.REWARD_FELL.value

        # Apply environment rules
        done_1 = self.agents[1].done
        if not done_1:
            rew, done_1 = self.apply_rules(self.agents[1])
            rew_1 += rew

        done_0 = self.agents[0].done
        if not done_0:
            rew, done_0 = self.apply_rules(self.agents[0])
            rew_0 += rew

        # All rewards and terminations are now calculated
        rewards = {self.agents[1]: rew_1, self.agents[0]: rew_0}

        # Now we calculate the observations
        obs = {}

        if not self.agents[0].done:
            obs[self.agents[0]] = self.generate_agent_obs(self.agents[0])
        else:
            obs[self.agents[0]] = None

        if not self.agents[1].done:
            obs[self.agents[1]] = self.generate_agent_obs(self.agents[1])
        else:
            obs[self.agents[1]] = None

        dones = {self.agents[0]: done_0, self.agents[1]: done_1}

        self.agents[0].done = done_0
        self.agents[1].done = done_1

        return obs, rewards, dones

    def apply_rules(self, agent):

        rew = 0

        # If on a tree, cut log
        agent_cuts = self.cutting_tree(agent)
        if agent_cuts:
            agent.wood_logs += 1
            rew += Rewards.REWARD_CUT_TREE.value

        # If on a river, drown
        agent_drowns = self.on_a_river(agent)
        if agent_drowns:
            rew += Rewards.REWARD_DROWN.value

        # If comes to boulder and not on shoulders, bumps into boulder
        bumps_boulder = self.hits_boulder(agent)
        if bumps_boulder:
            rew += Rewards.REWARD_COLLISION.value

        # If on an exit, receive reward and is done
        rew_exit, agent_exits = self.exits(agent)
        rew += rew_exit

        agent_done = agent_exits or agent_drowns

        return rew, agent_done

    def cutting_tree(self, agent):
        row, col = agent.position

        if self.cell_type(row, col) == ElementsEnv.TREE.value:
            # If they are on a tree they cut it
            self.grid_env[row, col] = ElementsEnv.EMPTY.value
            return True
        return False

    def on_a_river(self, agent):
        row, col = agent.position
        if self.cell_type(row, col) == ElementsEnv.RIVER.value:
            return True
        return False

    def hits_boulder(self, agent):
        row, col = agent.position
        if self.cell_type(row, col) == ElementsEnv.BOULDER.value:
            return True
        return False

    def exits(self, agent):
        row, col = agent.position
        current_cell = self.cell_type(row, col)

        done = True

        if current_cell == ElementsEnv.EXIT_BLACK.value and agent.color == BLACK:
            reward = Rewards.REWARD_EXIT_VERY_HIGH.value

        elif current_cell == ElementsEnv.EXIT_BLACK.value and agent.color == WHITE:
            reward = Rewards.REWARD_EXIT_LOW.value

        elif current_cell == ElementsEnv.EXIT_WHITE.value and agent.color == WHITE:
            reward = Rewards.REWARD_EXIT_VERY_HIGH.value

        elif current_cell == ElementsEnv.EXIT_WHITE.value and agent.color == BLACK:
            reward = Rewards.REWARD_EXIT_LOW.value

        elif current_cell == ElementsEnv.EXIT_EASY.value:
            reward = Rewards.REWARD_EXIT_AVERAGE.value

        elif current_cell == ElementsEnv.EXIT_DIFFICULT.value:
            reward = Rewards.REWARD_EXIT_HIGH.value

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

        agent.angle += rotation

        row, col = agent.position
        current_cell = self.cell_type(row, col)

        # If we don't move forward nothing happens
        if forward == 0:
            return 0

        # Else we see where we go
        row_new, col_new = self.get_proximal_coordinate(row, col, agent.angle)

        next_cell = self.cell_type(row_new, col_new)

        # If we were on a boulder, we can move to non-obstacles
        # We collide only if we go toward an obstacle.
        if current_cell == ElementsEnv.BOULDER.value:

            if next_cell == ElementsEnv.OBSTACLE.value:
                reward = Rewards.REWARD_COLLISION.value
                row_new, col_new = row, col

        # If we were on the ground, we move unless we face boulder or obstacle
        else:

            # Check if next cell is an obstacle, we don't move
            if next_cell == ElementsEnv.OBSTACLE.value:
                reward = Rewards.REWARD_COLLISION.value
                row_new, col_new = row, col

            # Check if next cell is a boulder
            elif next_cell == ElementsEnv.BOULDER.value:

                # If not on shoulders, we collide
                if not agent.on_shoulders:
                    reward = Rewards.REWARD_COLLISION.value
                    row_new, col_new = row, col

                # Else we move to boulders
                # and starting then we can go from boulder to boulder

        # Whatever happens, if we move forward, we are not on shoulders anymore
        agent.on_shoulders = False

        # Now that we now if we can move or not, we change position
        agent.position = row_new, col_new

        return reward

    @staticmethod
    def get_proximal_coordinate(row, col, angle):

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

        visual_obs = self._generate_full_observation(agent)

        if not (agent.on_shoulders
                or self.grid_env[agent.position] == ElementsEnv.BOULDER.value):
            visual_obs = self._filter_observations(visual_obs)

        # Add other agent relative angle if it is seen
        if agent is self.agents[0]:
            other_agent = self.agents[1]
        else:
            other_agent = self.agents[0]

        relative_angle = (other_agent.angle - agent.angle) % 6

        flat_visual_obs = []
        for line_obs in visual_obs:
            flat_visual_obs += line_obs

        if ElementsEnv.AGENT.value not in flat_visual_obs:
            relative_angle = -1

        obs_dict = {
            'visual': flat_visual_obs,
            'other_agent_angle': relative_angle,
            'color': agent.color
        }

        return obs_dict

    def _generate_full_observation(self, agent):

        grid_copy = deepcopy(self.grid_env)

        if agent == self.agents[0] and self.agents[1].position:
            row, col = self.agents[1].position
            grid_copy[row, col] = ElementsEnv.AGENT.value

        elif agent == self.agents[1] and self.agents[0].position:
            row, col = self.agents[0].position
            grid_copy[row, col] = ElementsEnv.AGENT.value

        obs = [[grid_copy[agent.position]]]

        # iterate over range
        for obs_range in range(1, agent.range_observation):

            line_obs = []

            row, col = agent.position
            angle = agent.angle

            # go to start
            for _ in range(obs_range):
                row, col, _ = self.get_next_cell(row, col, (angle - 1) % 6)

            if 0 <= row < self.size and 0 <= col < self.size:
                line_obs.append(grid_copy[row, col])
            else:
                line_obs.append(ElementsEnv.EMPTY.value)

            # move first segment
            for _ in range(obs_range):
                row, col, _ = self.get_next_cell(row, col, (angle + 1) % 6)

                if 0 <= row < self.size and 0 <= col < self.size:
                    line_obs.append(grid_copy[row, col])
                else:
                    line_obs.append(ElementsEnv.EMPTY.value)

            # move second segment
            for _ in range(obs_range):
                row, col, _ = self.get_next_cell(row, col, (angle + 2) % 6)

                if 0 <= row < self.size and 0 <= col < self.size:
                    line_obs.append(grid_copy[row, col])
                else:
                    line_obs.append(ElementsEnv.EMPTY.value)
            obs.append(line_obs)

        return obs

    @staticmethod
    def _filter_observations(obs):
        " Replace all occlusions with -1 "

        for index_line in range(1, len(obs) - 1):

            line_obs = obs[index_line]

            for i in range(len(line_obs)):

                # if there is an occlusion
                if line_obs[i] == -1 or (
                        line_obs[i] != ElementsEnv.EMPTY.value
                        and line_obs[i] != ElementsEnv.RIVER.value):

                    middle = int((len(line_obs) - 1) / 2)

                    # if it is on extremas
                    if i == middle:
                        obs[index_line + 1][i + 1] = -1

                    # if in angle, occludes 2 cells
                    elif i < middle:
                        obs[index_line + 1][i] = -1
                        obs[index_line + 1][i + 1] = -1

                    elif i > middle:
                        obs[index_line + 1][i + 1] = -1
                        obs[index_line + 1][i + 2] = -1

                    else:
                        raise ValueError

        return obs

    def cell_type(self, x, y):
        return self.grid_env[x, y]

    def add_object(self, item, coords):
        r = coords[0]
        c = coords[1]
        self.grid_env[r, c] = item.value

    def get_next_cell(self, row: int, col: int,
                      angle: int) -> Tuple[int, int, int]:

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
