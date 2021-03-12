import math
import pytest

from jungle.agent import Agent
from jungle.utils import Definitions, Actions

from jungle import baseline_env

EmptyJungle = baseline_env.JungleGrid


def test_rl_loop():
    agent_1 = Agent(initial_r=None, initial_c=None, angle=None, range=4)
    agent_2 = Agent(initial_r=None, initial_c=None, angle=None, range=6)

    simple_jungle = EmptyJungle(size=11)
    assert simple_jungle.size == 11

    simple_jungle.add_agents(agent_1, agent_2)

    # Once added, each agent randomly takes a color for the game
    assert agent_1.color is Definitions.BLACK or agent_2.color is Definitions.BLACK
    assert agent_1.color is Definitions.WHITE or agent_2.color is Definitions.WHITE

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: -1},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 0}
               }

    obs, rew, done = simple_jungle.step(actions)

    assert agent_1 in obs.keys()
    assert agent_2 in obs.keys()

    assert isinstance(rew[agent_1], float)
    assert isinstance(rew[agent_2], float)

    assert not done[agent_1] and not done[agent_2]


def check_corners(envir):
    # Verify that all corners have the same shape
    # cells are identified using np coordinates

    # Top-left corner
    assert envir.cell_type(0, 0) == Definitions.OBSTACLE
    assert envir.cell_type(0, 1) == Definitions.OBSTACLE
    assert envir.cell_type(0, 2) == Definitions.OBSTACLE
    assert envir.cell_type(1, 0) == Definitions.OBSTACLE
    assert envir.cell_type(2, 1) == Definitions.OBSTACLE
    assert envir.cell_type(1, 1) == Definitions.EXIT

    # Top-right corner
    assert envir.cell_type(0, envir.size) == Definitions.OBSTACLE
    ...
    # TODO: write for each corner


def test_environment_building():
    for size_envir in range(1, 20):

        # Check that pair size_envir raise error
        # or that too small environment raise error

        if size_envir % 2 == 0 or size_envir < Definitions.MIN_SIZE_ENVIR:

            with pytest.raises(Exception):
                simple_jungle = EmptyJungle(size=size_envir)

        else:

            simple_jungle = EmptyJungle(size=size_envir)
            check_corners(simple_jungle)


def test_initialization():
    agent_1 = Agent(range=4)
    agent_2 = Agent(range=4)

    for size_envir in [11, 13, 15]:
        simple_jungle = EmptyJungle(size=size_envir)
        simple_jungle.add_agents(agent_1, agent_2)

        # grid_position should be in np coordinates (row, col)
        assert agent_1.grid_position == ((size_envir - 1) / 2, (size_envir - 1) / 2 - 1)
        assert agent_2.grid_position == ((size_envir - 1) / 2, (size_envir - 1) / 2 + 1)

        # angle is index of trigonometric angle (0, 1, ... to 5)
        assert agent_1.angle == 3
        assert agent_2.angle == 0

        # Cartesian coordinates have unit 1.

        # on middle line, indented so +0.5
        assert agent_1.x == agent_1.grid_position[1] + 0.5
        assert agent_1.y == (size_envir - 1 - agent_1.grid_position[0]) * math.sqrt(3) / 2

        assert agent_2.x == agent_2.grid_position[1] + 0.5
        assert agent_2.y == (size_envir - 1 - agent_2.grid_position[0]) * math.sqrt(3) / 2


def test_movements():
    agent_1 = Agent(range=4)
    agent_2 = Agent(range=6)

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)

    # grid_position should be in np coordinates (row, col, angle)
    assert agent_1.grid_position == (5, 4)
    assert agent_1.angle == 3

    assert agent_2.grid_position == (5, 6)
    assert agent_2.angle == 0

    # First rotation, then forward, but the order in the actions dict doesn't matter.
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 1},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: -1}
               }

    obs, rew, done = simple_jungle.step(actions)

    # Check new positions on grid
    assert agent_1.grid_position == (6, 4)
    assert agent_1.angle == 4

    assert agent_2.grid_position == (4, 7)
    assert agent_2.angle == 5

    # Check new cartesian coordinates
    assert agent_1.x == agent_1.grid_position[1]
    assert agent_1.y == ((simple_jungle.size - 1) - agent_1.grid_position[0]) * math.sqrt(3) / 2

    assert agent_2.x == agent_2.grid_position[1]
    assert agent_2.y == ((simple_jungle.size - 1) - agent_2.grid_position[0]) * math.sqrt(3) / 2
