import math
import pytest
import nose

from jungle.agent import Agent
from jungle.utils import Actions, Definitions, ElementsEnv

from jungle.jungle import EmptyJungle


def test_rl_loop():
    """
    Tests the general RL api.
    """

    agent_1 = Agent()
    agent_2 = Agent()

    simple_jungle = EmptyJungle(size=11)
    assert simple_jungle.size == 11

    simple_jungle.add_agents(agent_1, agent_2)

    # Once added, each agent randomly takes a color for the game
    assert (agent_1.color is Definitions.BLACK and agent_2.color is Definitions.WHITE) \
           or (agent_1.color is Definitions.WHITE and agent_2.color is Definitions.BLACK)

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: -1},
               agent_2: {Actions.FORWARD: 1}
               }

    obs, rew, done = simple_jungle.step(actions)

    # Because observations are not set, it should return none:
    assert isinstance(obs[agent_1], (list, tuple))
    assert isinstance(obs[agent_2], (list, tuple))

    assert isinstance(rew[agent_1], (float, int))
    assert isinstance(rew[agent_2], (float, int))

    assert not done

    # should work with some actions not set (default to 0

    # agent_1 moves fwd ; agent_2 rotates -1
    actions = {agent_1: {Actions.FORWARD: 1},
               agent_2: {Actions.ROTATE: -1}
               }
    simple_jungle.step(actions)

    # should work without agent in the dict. (default to 0)

    pos_before = agent_1.grid_position

    # agent_2 rotates -1
    actions = {agent_2: {Actions.ROTATE: -1}
               }
    simple_jungle.step(actions)

    # make sure that position doesn't change when action is empty
    assert pos_before == agent_1.grid_position


def test_agents_on_same_cell():
    agent_1 = Agent()
    agent_2 = Agent()

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)
    print(agent_1.grid_position, agent_2.grid_position)

    # Move agent 2 on cell of agent 1

    # First rotate
    # agent_2 rotates
    actions = {agent_2: {Actions.ROTATE: 1}
               }
    simple_jungle.step(actions)
    simple_jungle.step(actions)
    simple_jungle.step(actions)

    # then move forward twice
    # agent_2 moves fwd
    actions = {agent_2: {Actions.FORWARD: 1}
               }
    simple_jungle.step(actions)
    obs, rew, done = simple_jungle.step(actions)

    # should be on the same cell, no collision
    assert agent_1.grid_position == agent_2.grid_position
    assert rew[agent_1] == rew[agent_2] == 0


def test_visualize_env():
    agent_1 = Agent()
    agent_2 = Agent()

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)

    check_corners(simple_jungle)


def check_corners(envir):
    # Verify that all corners have the same shape
    # cells are identified using np coordinates\

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

    # Top-right corner
    #   x x x
    #    . . x
    #   . . x

    assert envir.cell_type(0, envir.size - 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(0, envir.size - 2) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(0, envir.size - 3) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(1, envir.size - 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(2, envir.size - 1) == ElementsEnv.OBSTACLE.value

    assert envir.cell_type(2, envir.size - 2) == ElementsEnv.EMPTY.value
    assert envir.cell_type(2, envir.size - 3) == ElementsEnv.EMPTY.value
    assert envir.cell_type(1, envir.size - 3) == ElementsEnv.EMPTY.value
    assert envir.cell_type(1, envir.size - 2) == ElementsEnv.EMPTY.value

    # Bottom-right corner
    #   . . x
    #    . . x
    #   x x x

    assert envir.cell_type(envir.size - 1, envir.size - 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 1, envir.size - 2) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 2, envir.size - 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 3, envir.size - 1) == ElementsEnv.OBSTACLE.value
    assert envir.cell_type(envir.size - 1, envir.size - 3) == ElementsEnv.OBSTACLE.value

    assert envir.cell_type(envir.size - 3, envir.size - 2) == ElementsEnv.EMPTY.value
    assert envir.cell_type(envir.size - 3, envir.size - 3) == ElementsEnv.EMPTY.value
    assert envir.cell_type(envir.size - 2, envir.size - 3) == ElementsEnv.EMPTY.value
    assert envir.cell_type(envir.size - 2, envir.size - 2) == ElementsEnv.EMPTY.value

    # Bottom-left corner
    #   x x . .
    #    x . .
    #   x x x
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

        if size_envir % 2 == 0 or size_envir < Definitions.MIN_SIZE_ENVIR.value:

            with pytest.raises(Exception):
                EmptyJungle(size=size_envir)

        else:

            simple_jungle = EmptyJungle(size=size_envir)
            check_corners(simple_jungle)


def test_initialization():
    agent_1 = Agent()
    agent_2 = Agent()

    for size_envir in [11, 13, 15]:
        simple_jungle = EmptyJungle(size=size_envir)
        simple_jungle.add_agents(agent_1, agent_2)

        # grid_position should be in np coordinates (row, col)
        assert agent_1.grid_position == ((size_envir - 1) / 2, (size_envir - 1) / 2 - 1)
        assert agent_2.grid_position == ((size_envir - 1) / 2, (size_envir - 1) / 2 + 1)

        # angle is index of trigonometric angle (0, 1, ... to 5)
        assert agent_1.angle == 3
        assert agent_2.angle == 0


def test_movements():
    agent_1 = Agent()
    agent_2 = Agent()

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    assert agent_1.grid_position == (5, 4)
    assert agent_1.angle == 3

    assert agent_2.grid_position == (5, 6)
    assert agent_2.angle == 0

    # First rotation, then forward, but the order in the actions dict doesn't matter.
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 1},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: -1}
               }
    simple_jungle.step(actions)

    # Check new positions on grid
    assert agent_1.grid_position == (6, 4)
    assert agent_1.angle == 4

    assert agent_2.grid_position == (6, 7)
    assert agent_2.angle == 5

    # Perform the same action 5 more times and it should go back to original position
    # Basically, it is doing a circle

    for i in range(5):
        simple_jungle.step(actions)

    assert agent_1.grid_position == (5, 4)
    assert agent_1.angle == 3

    assert agent_2.grid_position == (5, 6)
    assert agent_2.angle == 0


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

    # agent_1 moves forward, towards the object.
    actions = {agent_1: {Actions.FORWARD: 1}}

    obs, rew, done = simple_jungle.step(actions)

    # agent keeps position and angle
    assert agent_1.grid_position == (5, 4)
    assert agent_1.angle == 3

    # agent receives reward for collision
    assert rew[agent_1] == Definitions.REWARD_COLLISION.value

    # agent_1 now rotates, then moves forward towards another object.
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: -1, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}
               }

    obs, rew, done = simple_jungle.step(actions)

    # first movement occurs without collision
    assert agent_1.grid_position == (4, 4)
    assert rew[agent_1] == 0.0
    assert agent_1.angle == 2

    # agent_1 moves forward, now it should bump
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}
               }

    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (4, 4)
    assert rew[agent_1] == Definitions.REWARD_COLLISION.value
    assert agent_1.angle == 2


def test_collision_with_tree():
    # Agent 1 moves and collides with tree.
    # Looks something like:
    #  . . . . . .
    #   . T T T . .
    #  . . . . A .

    agent_1 = Agent()
    agent_2 = Agent()

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)

    simple_jungle.add_object(ElementsEnv.TREE, (4, 4))
    simple_jungle.add_object(ElementsEnv.TREE, (4, 3))
    simple_jungle.add_object(ElementsEnv.TREE, (4, 2))

    # move to first tree
    # agent_1 forward +1 and rotates -1
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: -1, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}
               }

    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (4, 4)
    assert agent_1.angle == 2
    assert rew[agent_1] == Definitions.REWARD_CUT_TREE.value
    assert agent_1.wood_logs == 1

    # move to second tree
    # agent_1 forward +1 and rotates 1
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 1, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}
               }

    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (4, 3)
    assert agent_1.angle == 3
    assert rew[agent_1] == Definitions.REWARD_CUT_TREE.value
    assert agent_1.wood_logs == 2

    # move to third tree
    # agent_1 forward +1
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}
               }

    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (4, 2)
    assert agent_1.angle == 3
    assert rew[agent_1] == Definitions.REWARD_CUT_TREE.value
    assert agent_1.wood_logs == 2

    # we are limiting the number of tree logs to 2.
    # then, later, agents would need 4 logs total to replace water by empty (building a bridge)


def run_tree_experiment():
    # Agent 1 and 2 move at the same time and collide with a tree.
    # Sometimes 1 get the log, sometimes 2 get the log
    #  . . . . . .
    #   . 1 T 2 .
    #  . . . . . .

    agent_1 = Agent()
    agent_2 = Agent()

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    simple_jungle.add_object(ElementsEnv.TREE, (5, 5))

    # face the tree
    # agent_1 and agent_2 rotate -1
    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: -1, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: -1, Actions.CLIMB: 0}
               }

    simple_jungle.step(actions)
    simple_jungle.step(actions)

    simple_jungle.step(actions)

    # move towards the tree
    # agent_1 fwd 1 , agent_2 fwd -1
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: -1, Actions.ROTATE: 0, Actions.CLIMB: 0}
               }

    simple_jungle.step(actions)

    # one of them gets the log
    assert ((agent_1.wood_logs == 1 and agent_2.wood_logs == 0)
            or (agent_1.wood_logs == 0 and agent_2.wood_logs == 1))

    return agent_1.wood_logs, agent_2.wood_logs


def test_two_agents_cutting_a_tree():
    agent_1_gets_log = 0
    agent_2_gets_log = 0

    # check that the log doesn't go all the time to the same agent

    for i in range(100):
        log_1, log_2 = run_tree_experiment()

        agent_1_gets_log += log_1
        agent_2_gets_log += log_2

    assert agent_2_gets_log != 0 and agent_1_gets_log != 0


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

    assert agent_1.done
    assert agent_2.done
    assert done

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

    # both agents need to be at River, otherwise lone agent at river dies
    assert rew[agent_2] == Definitions.REWARD_DROWN.value

    # From MG test that agent 2 is dead -- eg maybe no value for agent 2 on grid


def test_build_bridge():

    agent_1 = Agent()
    agent_2 = Agent()

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    # Place a river between them, and trees in front of them
    simple_jungle.add_object(ElementsEnv.RIVER, (5, 5))
    simple_jungle.add_object(ElementsEnv.TREE, (5, 3))
    simple_jungle.add_object(ElementsEnv.TREE, (5, 2))
    simple_jungle.add_object(ElementsEnv.TREE, (5, 7))
    simple_jungle.add_object(ElementsEnv.TREE, (5, 8))

    # Go fetch some wood
    actions = {agent_1: {Actions.FORWARD: 1},
               agent_2: {Actions.FORWARD: 1}}

    simple_jungle.step(actions)
    simple_jungle.step(actions)

    # assert there are enough logs
    assert (agent_1.wood_logs + agent_2.wood_logs) == 4

    # go back to middle
    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 1},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 1}}

    simple_jungle.step(actions)
    simple_jungle.step(actions)
    simple_jungle.step(actions)

    actions = {agent_1: {Actions.FORWARD: 1},
               agent_2: {Actions.FORWARD: 1}}

    simple_jungle.step(actions)
    simple_jungle.step(actions)
    _, rew, done = simple_jungle.step(actions)


    # assert river cell becomes empty cell
    assert simple_jungle.cell_type(5, 5) == ElementsEnv.EMPTY.value


    # assert they both get reward for building bridge (both need to be at river)
    assert rew[agent_1] == Definitions.REWARD_BUILT_BRIDGE.value
    assert rew[agent_2] == Definitions.REWARD_BUILT_BRIDGE.value

    # assert they both are not done
    assert not agent_1.done
    assert not agent_2.done


def test_climb_action():
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    # agents should do something and land on the same cell
    # then they can climb

    actions = {agent_1: { Actions.ROTATE: -1}}
    simple_jungle.step(actions)
    simple_jungle.step(actions)
    simple_jungle.step(actions)

    actions = {agent_1: { Actions.FORWARD: -1}}
    simple_jungle.step(actions)
    simple_jungle.step(actions)

    # They are now on the same cell
    assert agent_1.grid_position ==  agent_2.grid_position

    actions = {agent_1: {Actions.CLIMB: 1} }

    _, rew, done = simple_jungle.step(actions)

    # black climbs, white does not move , observability increases, small neg reward for white as black is chubby. For
    # now, lets say orientation is the direction white is facing ; so black, in climbing, changes its orientation to
    # that of white

    assert rew[agent_2] == Definitions.REWARD_CARRYING.value
    assert agent_1.on_shoulders


def test_climb_boulders():

    #   . . B 1 . . 2 .

    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)
    actions = {agent_2: {Actions.ROTATE: -1}}
    simple_jungle.step(actions)
    simple_jungle.step(actions)
    simple_jungle.step(actions)

    actions = {agent_2: {Actions.FORWARD: 1}}
    simple_jungle.step(actions)
    simple_jungle.step(actions)

    # They are now on the same cell
    assert agent_1.grid_position == agent_2.grid_position
    assert agent_1.angle == agent_2.angle

    # We place a boulder in front of agents
    simple_jungle.add_object(ElementsEnv.BOULDER, (5, 3))

    # Agent 1 tries to go to the boulder but fails
    actions = {agent_1: {Actions.FORWARD: 1}}
    _, rew, done = simple_jungle.step(actions)
    assert agent_1.grid_position == agent_2.grid_position
    assert rew[agent_1] == Definitions.REWARD_COLLISION.value

    # Now, agent 1 tries to climb first and then move forward
    actions = {agent_1: {Actions.CLIMB: 1}}
    simple_jungle.step(actions)
    assert agent_1.on_shoulders

    actions = {agent_1: {Actions.FORWARD: 1}}
    simple_jungle.step(actions)

    # Now, should be on same position as boulder
    assert agent_1.grid_position == (5,3)
    assert agent_1.on_shoulders is False

    # After that, the agent can move forward on the next empty cell

    actions = {agent_1: {Actions.FORWARD: 1}}
    _, rew, _ = simple_jungle.step(actions)

    assert agent_1.grid_position == (5, 2)
    assert rew[agent_1] == 0


def test_obs():
    # @MG I was just testing that observations are processed and returned
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: -1, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 1, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)


def test_obstacles_in_obs_cross():
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    # directly left of agent 1
    simple_jungle.add_object(ElementsEnv.TREE, (5, 3))

    # directly right of agent 2
    simple_jungle.add_object(ElementsEnv.TREE, (5, 8))

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)

    # @MG these assert statements were just to do some checks - they
    # will not be part of the final codebase
    assert agent_1.left_view_obstructed
    assert agent_2.right_view_obstructed

    # directly below agent 1
    simple_jungle.add_object(ElementsEnv.TREE, (8, 4))

    # directly above agent 2
    simple_jungle.add_object(ElementsEnv.TREE, (3, 7))

    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 1, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 1, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.bottom_view_obstructed
    assert agent_2.top_view_obstructed


def test_agent_view():
    # depending on the obstacle(tree) position , agents should be able to see / not see
    # rivers, boulders , exits etc

    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    # directly left of agent 1
    simple_jungle.add_object(ElementsEnv.TREE, (5, 3))
    # should not be able to see this boulder
    simple_jungle.add_object(ElementsEnv.BOULDER, (5, 2))
    # should be able to see this river
    simple_jungle.add_object(ElementsEnv.RIVER, (3, 3))

    # directly right of agent 2
    simple_jungle.add_object(ElementsEnv.TREE, (5, 8))
    # should not be able to see this boulder
    simple_jungle.add_object(ElementsEnv.BOULDER, (5, 9))
    # should be able to see this river
    simple_jungle.add_object(ElementsEnv.RIVER, (3, 9))

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)

    assert ElementsEnv.RIVER.value in obs[agent_1]
    assert ElementsEnv.BOULDER.value not in obs[agent_1]

    assert ElementsEnv.RIVER.value in obs[agent_2]
    assert ElementsEnv.BOULDER.value not in obs[agent_2]


def test_obstacles_in_obs_diagonal():
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    # bottom left diagonal for agent 1
    simple_jungle.add_object(ElementsEnv.TREE, (6, 3))
    # top right diagonal agent 2
    simple_jungle.add_object(ElementsEnv.TREE, (3, 8))

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)

    # @MG these assert statements were just to do some checks - they
    # will not be part of the final codebase
    assert agent_1.bottom_left_obstructed
    assert agent_2.top_right_obstructed


def test_diagonal_view_bottom_left():
    # test for bottom left

    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    # bottom left diagonal for agent 1
    simple_jungle.add_object(ElementsEnv.TREE, (6, 3))

    # should not be able to see around the diagonal
    simple_jungle.add_object(ElementsEnv.RIVER, (6, 2))
    simple_jungle.add_object(ElementsEnv.RIVER, (7, 2))
    simple_jungle.add_object(ElementsEnv.RIVER, (7, 3))

    # empty actions to pass to the step function

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)
    assert agent_1.bottom_left_obstructed

    assert ElementsEnv.RIVER.value not in obs[agent_1]


def test__diagonal_view_top_right():
    # test for top right

    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    # bottom left diagonal for agent 1
    simple_jungle.add_object(ElementsEnv.TREE, (4, 7))

    # should not be able to see around the diagonal
    simple_jungle.add_object(ElementsEnv.RIVER, (4, 8))
    simple_jungle.add_object(ElementsEnv.RIVER, (3, 7))
    simple_jungle.add_object(ElementsEnv.RIVER, (3, 8))

    # empty actions to pass to the step function

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)

    assert agent_2.top_right_obstructed

    assert ElementsEnv.RIVER.value not in obs[agent_2]


def test__diagonal_view_bottom_right():
    # test for top right

    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    # bottom left diagonal for agent 1
    simple_jungle.add_object(ElementsEnv.TREE, (6, 7))

    # should not be able to see around the diagonal
    simple_jungle.add_object(ElementsEnv.RIVER, (6, 8))
    simple_jungle.add_object(ElementsEnv.RIVER, (7, 7))
    simple_jungle.add_object(ElementsEnv.RIVER, (7, 8))

    # empty actions to pass to the step function

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)

    print(obs[agent_2])
    assert agent_2.bottom_right_obstructed

    assert ElementsEnv.RIVER.value not in obs[agent_2]


def test_obs_cooperation_sequence():
    # agent 2's view is obstructed

    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    simple_jungle.add_object(ElementsEnv.TREE, (4, 7))

    # should not be able to see around the diagonal
    simple_jungle.add_object(ElementsEnv.RIVER, (4, 8))
    simple_jungle.add_object(ElementsEnv.RIVER, (3, 7))
    simple_jungle.add_object(ElementsEnv.RIVER, (3, 8))

    # empty actions to pass to the step function

    # agent 1 turns towards agent 2
    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: -1, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)
    obs, rew, done = simple_jungle.step(actions)
    obs, rew, done = simple_jungle.step(actions)

    assert agent_2.top_right_obstructed

    assert ElementsEnv.RIVER.value not in obs[agent_2]

    # agent 1 moves towards agent 2
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)
    obs, rew, done = simple_jungle.step(actions)

    assert agent_1.grid_position == (5, 6)
    assert agent_2.grid_position == (5, 6)

    # agent 2 climbs on the shoulders of agent 1

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 1}}
    obs, rew, done = simple_jungle.step(actions)

    assert agent_2.on_shoulders

    # agent 2's observability is restored to full
    assert ElementsEnv.RIVER.value in obs[agent_2]

def test_boulders():
    # cannot cross boulders
    agent_1 = Agent(range_observation=4)
    agent_2 = Agent(range_observation=4)

    simple_jungle = EmptyJungle(size=11)
    simple_jungle.add_agents(agent_1, agent_2)

    simple_jungle.add_object(ElementsEnv.BOULDER, (4, 7))
    simple_jungle.add_object(ElementsEnv.BOULDER, (6, 6))

    print(agent_2.grid_position)

    # agent 2 moves to top right boulder, gets neg reward, stays at original position
    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 1, Actions.CLIMB: 0}}
    obs, rew, done = simple_jungle.step(actions)

    # assert rew[agent_2] == Definitions.REWARD_COLLISION.value
    # assert agent_2.grid_position == (5,6)

    print(agent_1.grid_position, agent_1.angle)
    print(agent_2.grid_position, agent_2.angle)

    # agent 1 turns towards agent 2
    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: -1, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)
    obs, rew, done = simple_jungle.step(actions)
    obs, rew, done = simple_jungle.step(actions)

    # agent 1 moves towards agent 2
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0}}

    obs, rew, done = simple_jungle.step(actions)
    obs, rew, done = simple_jungle.step(actions)

    print(agent_1.grid_position , agent_1.angle)
    print(agent_2.grid_position, agent_2.angle)





    # agent 1 moves to agent 2, agent 2 gets on agent 1's shoulders

    #TODO need to set

    actions = {agent_1: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 0},
               agent_2: {Actions.FORWARD: 0, Actions.ROTATE: 0, Actions.CLIMB: 1}}
    obs, rew, done = simple_jungle.step(actions)

    #assert agent_2.on_shoulders


    # both agents move together to bottom boulder

    # agent 2 can cross the boulder, agent 1 remains on the prior cell

    #assert agent_2.grid_position == (6,6)
    #assert agent_1.grid_position == (5,6)



