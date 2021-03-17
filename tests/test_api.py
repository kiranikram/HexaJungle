import math
import pytest
import nose

from jungle.agent import Agent
from jungle.utils import Actions, Definitions, ElementsEnv

from jungle import baseline_env

EmptyJungle = baseline_env.JungleGrid


def test_rl_loop():
    # Todo: remove initial_r, initial_c, angle. These are defined by the jungle envr, so it is redundant.
    agent_1 = Agent(range=4)
    agent_2 = Agent(range=6)

    simple_jungle = EmptyJungle(size=11)
    assert simple_jungle.size == 11

    simple_jungle.add_agents(agent_1, agent_2)

    # Once added, each agent randomly takes a color for the game
    assert (agent_1.color is Definitions.BLACK and agent_2.color is Definitions.WHITE) \
           or (agent_1.color is Definitions.WHITE and agent_2.color is Definitions.BLACK)

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: -1},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 0}
               }

    obs, rew, done = simple_jungle.step(actions)

    assert agent_1 in obs.keys()
    assert agent_2 in obs.keys()

    assert isinstance(rew[agent_1], float)
    assert isinstance(rew[agent_2], float)

    assert not done[agent_1] and not done[agent_2]


def test_check_corners():
    # Verify that all corners have the same shape
    # cells are identified using np coordinates\
    simple_jungle = EmptyJungle(size=11)
    envir = simple_jungle

    # Todo: you don't have exits in empty jungles/
    # you will place exits and their surroundings by subclassing Empty Jungle.

    # Top-left corner
    # Should look like that:
    #   x x x
    #    x . .
    #   x x .

    assert envir.cell_type(0, 0) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(0, 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(0, 2) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(1, 0) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(2, 0) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(2, 1) == ElementsEnv.OBSTACLE.value

    assert envir.cell_type(1, 1) == ElementsEnv.EMPTY.value
    assert envir.cell_type(1, 2) == ElementsEnv.EMPTY.value
    assert envir.cell_type(2, 2) == ElementsEnv.EMPTY.value

    # todo: other corners with similar values

    # @MG I've kept these in the same shape as above

    # Top-right corner
    assert envir.cell_type(0, envir.size - 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(0, envir.size - 2) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(0, envir.size - 3) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(1, envir.size - 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(2, envir.size - 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(2, envir.size - 2) == ElementsEnv.OBSTACLE.value

    assert envir.cell_type(2, envir.size - 3) == ElementsEnv.EMPTY.value
    assert envir.cell_type(1, envir.size - 3) == ElementsEnv.EMPTY.value
    assert envir.cell_type(1, envir.size - 2) == ElementsEnv.EMPTY.value

    # # Bottom-right corner
    # # no exits
    assert envir.cell_type(envir.size - 1, envir.size - 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 1, envir.size - 2) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 2, envir.size - 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 3, envir.size - 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 1, envir.size - 3) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 3, envir.size - 2) == ElementsEnv.OBSTACLE.value

    assert envir.cell_type(envir.size - 3, envir.size - 3) == ElementsEnv.EMPTY.value
    assert envir.cell_type(envir.size - 2, envir.size - 3) == ElementsEnv.EMPTY.value
    assert envir.cell_type(envir.size - 2, envir.size - 2) == ElementsEnv.EMPTY.value
    #
    # # Bottom-left corner
    #
    assert envir.cell_type(envir.size - 3, 0) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 2, 0) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 1, 0) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 1, 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 1, 2) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 3, 1) == ElementsEnv.OBSTACLE.value

    assert envir.cell_type(envir.size - 2, 1) == ElementsEnv.EMPTY.value
    assert envir.cell_type(envir.size - 2, 2) == ElementsEnv.EMPTY.value
    assert envir.cell_type(envir.size - 3, 2) == ElementsEnv.EMPTY.value


def test_environment_building():
    for size_envir in range(1, 20):

        # Check that pair size_envir raise error
        # or that too small environment raise error

        # TODO: here check if you should use Definitions.MIN_SIZE_ENVIR.value
        if size_envir % 2 == 0 or size_envir < Definitions.MIN_SIZE_ENVIR:

            with pytest.raises(Exception):
                simple_jungle = EmptyJungle(size=size_envir)

        else:

            simple_jungle = EmptyJungle(size=size_envir)

            # TODO: here, you should rename test_check_corners to check_corners so that you cn test every envir.
            test_check_corners(simple_jungle)


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


def test_collisions():
    agent_1 = Agent(range=4)
    agent_2 = Agent(range=6)

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)

    simple_jungle.add_object(ElementsEnv.OBSTACLE, (5, 3))

    # First rotation, then forward, but the order in the actions dict doesn't matter.
    actions = {agent_1: {Actions.FORWARD: 1}}
    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (5, 4)
    assert agent_1.angle == 3

    assert rew[agent_1] == Definitions.REWARD_BUMP.value
