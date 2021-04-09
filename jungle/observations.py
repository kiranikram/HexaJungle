import math
import pytest

from jungle.agent import Agent
from jungle.utils import Actions, Definitions, ElementsEnv


def restrict_observations(agent, obstacles):
    agent_row, agent_col = agent.grid_position
    all_ctd = []
    ctd = []
    for i in obstacles:
        obs_row = i[0]
        obs_col = i[1]

        # if directly above, drop 3 x 3 above
        if obs_col == agent_col and obs_row < agent_row:
            ctd = ctd + top_cells_to_drop(obs_row, obs_col)
            agent.top_view_obstructed = True

        elif obs_col == agent_col and obs_row > agent_row:
            ctd = ctd + bottom_cells_to_drop(obs_row, obs_col)

        elif obs_col > agent_col and obs_row == agent_row:
            ctd = ctd + right_cells_to_drop(obs_row, obs_col)

        elif obs_col < agent_col and obs_row == agent_row:
            ctd = ctd + left_cells_to_drop(obs_row, obs_col)

        elif obs_col > agent_col and obs_row < agent_row:
            ctd = ctd + top_right_cells_to_drop(obs_row, obs_col)
            agent.top_right_obstructed = True

        elif obs_col > agent_col and obs_row > agent_row:
            ctd = ctd + bottom_right_cells_to_drop(obs_row, obs_col)

        elif obs_col < agent_col and obs_row < agent_row:
            ctd = ctd + top_left_cells_to_drop(obs_row, obs_col)

        elif obs_col < agent_col and obs_row > agent_row:
            ctd = ctd + bottom_left_cells_to_drop(obs_row, obs_col)

    return ctd


def top_cells_to_drop(obs_row, obs_col):
    ctd = [(obs_row - 1, obs_col - 1), (obs_row - 1, obs_col), (obs_row - 1, obs_col + 1), (obs_row - 2, obs_col - 1),
           (obs_row - 2, obs_col), (obs_row - 2, obs_col + 1), (obs_row - 3, obs_col - 1), (obs_row - 3, obs_col),
           (obs_row - 3, obs_col + 1)]
    return ctd


def bottom_cells_to_drop(obs_row, obs_col):
    ctd = [(obs_row + 1, obs_col - 1), (obs_row + 1, obs_col), (obs_row + 1, obs_col + 1), (obs_row + 2, obs_col - 1),
           (obs_row + 2, obs_col), (obs_row + 2, obs_col + 1), (obs_row + 3, obs_col - 1), (obs_row + 3, obs_col),
           (obs_row + 3, obs_col + 1)]
    return ctd


def right_cells_to_drop(obs_row, obs_col):
    ctd = [(obs_row - 1, obs_col + 1), (obs_row, obs_col + 1), (obs_row + 1, obs_col + 1), (obs_row - 1, obs_col + 2),
           (obs_row, obs_col + 2), (obs_row + 1, obs_col + 2), (obs_row - 1, obs_col + 3), (obs_row, obs_col + 3),
           (obs_row + 1, obs_col + 3)]
    return ctd


def left_cells_to_drop(obs_row, obs_col):
    ctd = [(obs_row - 1, obs_col - 1), (obs_row, obs_col - 1), (obs_row + 1, obs_col - 1), (obs_row - 1, obs_col - 2),
           (obs_row, obs_col - 2), (obs_row + 1, obs_col - 2), (obs_row - 1, obs_col - 3), (obs_row, obs_col - 3),
           (obs_row + 1, obs_col - 3)]
    return ctd


def top_right_cells_to_drop(obs_row, obs_col):
    ctd = [(obs_row - 1, obs_col), (obs_row - 2, obs_col), (obs_row, obs_col + 1), (obs_row - 1, obs_col + 1),
           (obs_row - 2, obs_col + 1), (obs_row, obs_col + 2), (obs_row - 1, obs_col + 2), (obs_row - 2, obs_col + 2)]

    return ctd


def top_left_cells_to_drop(obs_row, obs_col):
    ctd = [(obs_row - 1, obs_col), (obs_row - 2, obs_col), (obs_row, obs_col - 1), (obs_row - 1, obs_col - 1),
           (obs_row - 2, obs_col - 1), (obs_row, obs_col - 2), (obs_row - 1, obs_col - 2), (obs_row - 2, obs_col - 2)]

    return ctd


def bottom_right_cells_to_drop(obs_row, obs_col):
    ctd = [(obs_row - 1, obs_col), (obs_row - 2, obs_col), (obs_row, obs_col - 1), (obs_row - 1, obs_col - 1),
           (obs_row - 2, obs_col - 1), (obs_row, obs_col - 2), (obs_row - 1, obs_col - 2), (obs_row - 2, obs_col - 2)]

    return ctd


def bottom_left_cells_to_drop(obs_row, obs_col):
    ctd = [(obs_row, obs_col - 1), (obs_row, obs_col - 2), (obs_row + 1, obs_col), (obs_row + 1, obs_col - 1),
           (obs_row + 1, obs_col - 2), (obs_row + 2, obs_col), (obs_row + 2, obs_col - 1), (obs_row + 2, obs_col - 2)]

    return ctd
