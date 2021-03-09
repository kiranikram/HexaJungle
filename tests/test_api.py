from jungle import Agent, EmptyJungle
from jungle.utils import Definitions


def test_environment_creation():

    agent_1 = Agent(range=4)
    agent_2 = Agent(range=6)

    simple_jungle = EmptyJungle(size=11)

    simple_jungle.add_agents(agent_1, agent_2)

    # Once added, each agent randomly takes a color for the game
    assert agent_1.color is Definitions.BLACK or agent_2.color is Definitions.BLACK
    assert agent_1.color is Definitions.WHITE or agent_2.color is Definitions.WHITE

    actions = {agent_1: {Definitions.FORWARD:1, Definitions.ROTATE:-1},
               agent_2: {Definitions.FORWARD:1, Definitions.ROTATE:0}
               }

    obs, rew, dones = simple_jungle.step(actions)
