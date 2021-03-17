import math
import pytest
import nose

from jungle.agent import Agent
from jungle.utils import Actions, Definitions, ElementsEnv

from jungle import jungle

EmptyJungle = jungle.EmptyJungle


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
    assert agent_1.grid_position == (7, 4)
    assert agent_1.angle == 4

    assert agent_2.grid_position == (3, 6)
    assert agent_2.angle == 5

    # Check new cartesian coordinates
    assert agent_1.x == agent_1.grid_position[1] + 0.5
    assert agent_1.y == ((simple_jungle.size - 1) - agent_1.grid_position[0]) * math.sqrt(3) / 2

    assert agent_2.x == agent_2.grid_position[1] + 0.5
    assert agent_2.y == ((simple_jungle.size - 1) - agent_2.grid_position[0]) * math.sqrt(3) / 2


def test_move_to_tree():
    agent_1 = Agent(range=4)
    agent_2 = Agent(range=6)

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)

    # if agent passes tree, logs added to log_cache
    # preset log cache, and then add to it , depending on
    # agent location @ t-1, and agent actions

    # assume agents start at center

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 1},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: -1}
               }

    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (7, 4)
    assert agent_1.angle == 4
    assert agent_1.log_cache == 0

    assert agent_2.grid_position == (3, 6)
    assert agent_2.angle == 5
    assert agent_2.log_cache == 1


# not a good test
def test_move_to_river():
    # per size of the env , the agents together should have a certain number of logs
    # log rate scales logs required to the size of the env

    # test: if agent in river and not enough logs -100 on reward ; can be either agent
    agent_1 = Agent(range=4)
    agent_2 = Agent(range=4)

    simple_jungle = EmptyJungle(size=11)

    logs_needed = math.floor(11 / Definitions.LOG_RATE.value)

    simple_jungle.add_agents(agent_1, agent_2)

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: -1},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 0}
               }

    obs, rew, done = simple_jungle.step(actions)
    if (agent_1.grid_position == ElementsEnv.RIVER.value) and (simple_jungle.logs_collected < logs_needed):
        assert rew[agent_1] == -100

    if (agent_2.grid_position == ElementsEnv.RIVER.value) and (simple_jungle.logs_collected < logs_needed):
        assert rew[agent_2] == -100


def test_move_to_boulder():
    agent_1 = Agent(range=4)
    agent_2 = Agent(range=4)

    simple_jungle = EmptyJungle(size=11)
    # this checks - if agent in front of boulder, observability gets cut off


def test_collisions():
    agent_1 = Agent(range=4)
    agent_2 = Agent(range=6)

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)

    simple_jungle.add_object(ElementsEnv.OBSTACLE, (5, 3))

    # First rotation, then forward, but the order in the actions dict doesn't matter.
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: -1},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 0}
               }
    obs, rew, done = simple_jungle.step(actions)

    # TODO speak to Micahel about angles and coordinates

    assert agent_1.grid_position == (7, 4)
    assert agent_1.angle == 2

    assert rew[agent_1] == Definitions.REWARD_BUMP.value


def test_exit_types():
    agent_1 = Agent(range=4)
    agent_2 = Agent(range=6)

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)

    assert simple_jungle.cell_type(1, simple_jungle.size - 2) == ElementsEnv.EMPTY.value
    simple_jungle.add_object(ElementsEnv.RIVER_EXIT, (1, simple_jungle.size - 2))

    # check that surrounding empty cells are river
    assert simple_jungle.cell_type(2, simple_jungle.size - 3) == ElementsEnv.RIVER.value
    assert simple_jungle.cell_type(1, simple_jungle.size - 3) == ElementsEnv.RIVER.value
