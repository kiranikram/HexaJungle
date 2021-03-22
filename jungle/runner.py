import math
import pytest
from enum import IntEnum, Enum, auto


from jungle.agent import Agent
# from jungle.utils import Actions, Definitions, ElementsEnv

from jungle.jungle import EmptyJungle

class Actions(IntEnum):
    ROTATE = auto()
    FORWARD = auto()


simple_jungle = EmptyJungle(size=11)
agent_1 = Agent(range_observation=4)
agent_2 = Agent(range_observation=4)
simple_jungle.add_agents(agent_1, agent_2)

print ('INITIALIZED')
print(agent_1.grid_position )
print( agent_1.angle )
print(agent_2.grid_position )
print( agent_2.angle )
print(" ")



actions = {agent_1: {Actions.FORWARD: 1, Actions.ROTATE: 1},
               agent_2: {Actions.FORWARD: 1, Actions.ROTATE: -1}
               }

obs, rew, done = simple_jungle.step(actions)

print ('POST STEP')
print(agent_1.grid_position )
print( agent_1.angle )
print(agent_2.grid_position )
print( agent_2.angle )
print(" ")

