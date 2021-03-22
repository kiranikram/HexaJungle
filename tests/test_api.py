import math
import pytest
import nose

from jungle.agent import Agent
from jungle.utils import Actions, Definitions, ElementsEnv

from jungle.jungle import EmptyJungle


# @KI import directly EmptyJungle
# EmptyJungle = jungle.EmptyJungle


def test_rl_loop():
    # Todo: remove initial_r, initial_c, angle. These are defined by the jungle envr, so it is redundant.
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=6)

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


def check_corners(envir):
    # Verify that all corners have the same shape
    # cells are identified using np coordinates\

    # @KI here envir is a parameter, so that we can check that it works for several envir size.
    # simple_jungle = EmptyJungle(size=11)
    # envir = simple_jungle

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
        if size_envir % 2 == 0 or size_envir < Definitions.MIN_SIZE_ENVIR.value:

            with pytest.raises(Exception):
                EmptyJungle(size=size_envir)

        else:

            simple_jungle = EmptyJungle(size=size_envir)

            # TODO: here, you should rename test_check_corners to check_corners so that you cn test every envir.
            check_corners(simple_jungle)


def test_initialization():
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

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
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=6)

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

    assert agent_2.grid_position == (6, 7)
    assert agent_2.angle == 5

    # Check new cartesian coordinates
    # assert agent_1.x == agent_1.grid_position[1]
    # assert agent_1.y == ((simple_jungle.size - 1) - agent_1.grid_position[0]) * math.sqrt(3) / 2
    #
    # assert agent_2.x == agent_2.grid_position[1]
    # assert agent_2.y == ((simple_jungle.size - 1) - agent_2.grid_position[0]) * math.sqrt(3) / 2


def test_collisions_with_obstacles():
    # Agent 1 moves and collides with obstacles.
    # Looks something like:
    #  . X .
    #   . . .
    #  . X A .

    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=6)

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)

    simple_jungle.add_object(ElementsEnv.OBSTACLE, (5, 3))
    simple_jungle.add_object(ElementsEnv.OBSTACLE, (3, 3))

    # just forward, towards the object.
    # TODO: put in agent 2 actions for these tests; currently they are at zero
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0}
               }

    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (5, 4)
    assert agent_1.angle == 3

    assert rew[agent_1] == Definitions.REWARD_BUMP.value

    # now rotate, then forward towards another object.

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: -1},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0}
               }

    obs, rew, done = simple_jungle.step(actions)

    assert rew[agent_1] == 0.0
    assert agent_1.angle == 2

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0}
               }

    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (4, 4)

    # @MG according to the order of events this was in the wrong place so Imoved it up
    # assert rew[agent_1] == 0.0

    # now should bump
    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (4, 4)
    assert rew[agent_1] == Definitions.REWARD_BUMP.value

    assert agent_1.angle == 2

    assert rew[agent_1] == Definitions.REWARD_BUMP.value

    # Todo: add similar tests for agent 2!


def test_collision_with_tree():
    # Agent 1 moves and collides with obstacles.
    # Looks something like:
    #  . . . . . .
    #   . T T T . .
    #  . . . . A .

    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=6)

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)

    simple_jungle.add_object(ElementsEnv.TREE, (4, 4))
    simple_jungle.add_object(ElementsEnv.TREE, (4, 3))
    simple_jungle.add_object(ElementsEnv.TREE, (4, 2))

    # move to first tree
    # TODO: put in agent 2 actions for these tests; currently they are at zero
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: -1},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0}}
    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (4, 4)
    assert agent_1.angle == 2
    assert rew[agent_1] == Definitions.REWARD_CUT_TREE.value
    assert agent_1.wood_logs == 1

    # move to second tree
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 1},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0}}
    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (4, 3)
    assert agent_1.angle == 3
    assert rew[agent_1] == Definitions.REWARD_CUT_TREE.value
    assert agent_1.wood_logs == 2

    # move to third tree
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0}}
    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (4, 2)
    assert agent_1.angle == 3
    assert rew[agent_1] == Definitions.REWARD_CUT_TREE.value

    assert agent_1.wood_logs == 2

    # we are limiting the number of tree logs to 2.
    # then, later, agents would need 4 logs total to replace water by empty (building a bridge)


def test_exits():
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=6)

    assert agent_1.done is False
    assert agent_2.done is False

    # we put exit towards an agent and move through it
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0}}

    # exits provide 4 different rewards: LOW, AVERAGE, HIGH, VERY_HIGH
    # There are 4 different kinds of exits:
    # - EXIT_EASY: provide average reward
    # - EXIT_DIFFICULT: provide high reward
    # - EXIT_WHITE: provide very high reward to white, low reward to black
    # - EXIT_BLACK: provide very high reward to black, low reward to white

    # agent 1 takes easy exit.

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)
    simple_jungle.add_object(ElementsEnv.EXIT_EASY, (5, 3))

    _, rew, done = simple_jungle.step(actions)

    assert rew[agent_1] == Definitions.REWARD_EXIT_AVERAGE.value

    # agent 1 takes hard exit.

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)
    simple_jungle.add_object(ElementsEnv.EXIT_DIFFICULT, (5, 3))

    # when entering a new environment, agents done is reset.
    # TODO : take done out of agent and instantiate in jungle

    assert agent_1.done is False
    assert agent_2.done is False

    _, rew, done = simple_jungle.step(actions)
    assert rew[agent_1] == Definitions.REWARD_EXIT_HIGH.value

    # If an agent takes the exit of its color, it receives a very high reward
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 0}}

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    if agent_1.color is Definitions.WHITE:
        simple_jungle.add_object(ElementsEnv.EXIT_WHITE, (5, 3))
        simple_jungle.add_object(ElementsEnv.EXIT_BLACK, (5, 7))
    else:
        simple_jungle.add_object(ElementsEnv.EXIT_BLACK, (5, 3))
        simple_jungle.add_object(ElementsEnv.EXIT_WHITE, (5, 7))

    _, rew, done = simple_jungle.step(actions)
    assert rew[agent_1] == Definitions.REWARD_EXIT_VERY_HIGH.value
    assert rew[agent_1] == Definitions.REWARD_EXIT_VERY_HIGH.value

    assert done[agent_1] is True
    assert done[agent_2] is True

    # If an agent takes the exit of the opposite color, it receives a low reward

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    if agent_1.color is Definitions.BLACK:
        simple_jungle.add_object(ElementsEnv.EXIT_WHITE, (5, 3))
        simple_jungle.add_object(ElementsEnv.EXIT_BLACK, (5, 7))
    else:
        simple_jungle.add_object(ElementsEnv.EXIT_BLACK, (5, 3))
        simple_jungle.add_object(ElementsEnv.EXIT_WHITE, (5, 7))

    _, rew, done = simple_jungle.step(actions)
    assert rew[agent_1] == Definitions.REWARD_EXIT_LOW.value
    assert rew[agent_1] == Definitions.REWARD_EXIT_LOW.value


def test_gameplay_exit():
    # Game continues when one agent exits.
    # Game terminates when both agents exit.

    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=6)

    # agent 1 takes easy exit.

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)
    simple_jungle.add_object(ElementsEnv.EXIT_EASY, (5, 3))

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0}}

    _, rew, done = simple_jungle.step(actions)

    assert done is False
    assert agent_1.done is True
    assert not agent_2.done

    # agent 2 rotates then goes towards exit.
    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 1}}

    simple_jungle.step(actions)
    simple_jungle.step(actions)
    simple_jungle.step(actions)

    assert agent_1.done
    assert not agent_2.done

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 0}}

    # @MG needed to add exit as per agent2's starting position and your suggested^ actions
    simple_jungle.add_object(ElementsEnv.EXIT_EASY, (5, 4))

    simple_jungle.step(actions)
    _, rew, done = simple_jungle.step(actions)

    assert agent_1.done
    assert agent_2.done
    assert done


def test_cut_tree():
    # agent takes 3 actions and comes to a tree. once cut , the cell becomes empty
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=6)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    simple_jungle.add_object(ElementsEnv.TREE, (5, 7))
    simple_jungle.add_object(ElementsEnv.TREE, (3, 5))

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 0}}

    _, rew, done = simple_jungle.step(actions)

    assert agent_2.wood_logs == 1
    assert simple_jungle.cell_type(5, 7) == ElementsEnv.EMPTY.value

    # assert increase in logs for agent 2 and tree converts to empty + agent has logs

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: -1},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0}}

    _, rew, done = simple_jungle.step(actions)
    _, rew, done = simple_jungle.step(actions)
    _, rew, done = simple_jungle.step(actions)

    assert agent_1.wood_logs == 1
    assert simple_jungle.cell_type(3, 5) == ElementsEnv.EMPTY.value


def test_approach_river_together():
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=6)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    simple_jungle.add_object(ElementsEnv.RIVER, (4, 5))

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 1}}

    _, rew, done = simple_jungle.step(actions)
    _, rew, done = simple_jungle.step(actions)
    _, rew, done = simple_jungle.step(actions)
    _, rew, done = simple_jungle.step(actions)

    print(agent_2.color)
    print(agent_2.grid_position)

    # both agents need to be at River, otherwise lone agent at river dies
    assert rew[agent_2] == Definitions.REWARD_DROWN.value


def test_build_bridge():

    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=6)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    simple_jungle.add_object(ElementsEnv.RIVER, (4, 4))
    simple_jungle.add_object(ElementsEnv.TREE, (4, 6))
    simple_jungle.add_object(ElementsEnv.TREE, (4, 5))

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: -1},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 1}}

    _, rew, done = simple_jungle.step(actions)

    print(agent_1.color, agent_1.grid_position, agent_1.angle, agent_1.wood_logs)
    print(agent_2.color,agent_2.grid_position, agent_2.angle, agent_2.wood_logs)
    print(" ")

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 1}}

    _, rew, done = simple_jungle.step(actions)

    print(agent_1.grid_position, agent_1.angle, agent_1.wood_logs)
    print(agent_2.grid_position, agent_2.angle, agent_2.wood_logs)
    print(" ")

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 0}}

    _, rew, done = simple_jungle.step(actions)

    print(agent_1.grid_position, agent_1.angle, agent_1.wood_logs)
    print(agent_2.grid_position, agent_2.angle, agent_2.wood_logs)
    print(" ")

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 1}}

    _, rew, done = simple_jungle.step(actions)

    print(agent_1.grid_position, agent_1.angle, agent_1.wood_logs)
    print(agent_2.grid_position, agent_2.angle, agent_2.wood_logs)
    print(" ")

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 0}}

    _, rew, done = simple_jungle.step(actions)

    print(agent_1.grid_position, agent_1.angle, agent_1.wood_logs)
    print(agent_2.grid_position, agent_2.angle, agent_2.wood_logs)
    print(" ")

    # assert there are enough logs
    assert (agent_1.wood_logs + agent_2.wood_logs) >= 2

    # assert they both get reward for building bridge (both need to be at river)
    assert rew[agent_1] == Definitions.REWARD_BUILT_BRIDGE.value
    assert rew[agent_2] == Definitions.REWARD_BUILT_BRIDGE.value

    # assert river cell becomes bridge cell
    assert simple_jungle.cell_type(4, 4) == ElementsEnv.BRIDGE.value

    # assert they stay at original position
    #assert agent_1.grid_position == (5, 4)
    #assert agent_1.grid_position == (4, 5)
