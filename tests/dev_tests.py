import math
import pytest

from jungle.utils import Definitions
from jungle import baseline_env
from jungle.agent import Agent


EmptyJungle = baseline_env.JungleGrid


def test_jungle_instantiates(FORWARD=None, ROTATE=None):
    simple_jungle = EmptyJungle(size=11)
    agent_1 = Agent(initial_r=5, initial_c=4, angle=3, range=4)
    agent_2 = Agent(initial_r=5, initial_c=6, angle=0, range=6)

    actions = {agent_1: {FORWARD: 1, ROTATE: 1},
               agent_2: {FORWARD: 1, ROTATE: -1}
               }

    obs, rew, done = simple_jungle.step(actions)