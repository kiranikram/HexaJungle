from jungle import Agent, EmptyJungle
from jungle.utils import Definitions, Actions


def test_rl_loop():

    agent_1 = Agent(range=4)
    agent_2 = Agent(range=6)

    simple_jungle = EmptyJungle(size=11)

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


def test_movements():

    agent_1 = Agent(range=4)
    agent_2 = Agent(range=6)

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)

    # position should be in cartesian coordinates
    assert agent_1.position == (4, 5, 3)
    assert agent_2.position == (6, 5, 0)

    # First rotation, then forward
    actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: -1},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: 1}
               }

    obs, rew, done = simple_jungle.step(actions)
    assert agent_1.position == (4, 6, 2)
    assert agent_2.position == (7, 4, 5)

    # Check that 6 rotations bring to the original position
    actions = {agent_1: {Actions.ROTATE: -1},
               agent_2: {Actions.ROTATE: 1}
               }

    for _ in range(6):
        obs, rew, done = simple_jungle.step(actions)

    assert agent_1.position == (4, 6, 2)
    assert agent_2.position == (7, 4, 5)


