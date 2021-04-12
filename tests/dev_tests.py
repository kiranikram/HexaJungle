import math
import pytest
import nose
import random

from jungle.agent import Agent
from jungle.jungle import EmptyJungle
from jungle.utils import Actions, Definitions, ElementsEnv
from jungle.env_versions import EasyJungle
from jungle.exp_trainer import run
from jungle.rl_envs.basic import RiverExit

from jungle import jungle


def generate_actions():
    fwd = random.choice([-1, 0, 1])
    rot = random.choice([1, 0])
    climb = random.choice([1, 0])
    agent_actions = {Actions.FORWARD: fwd, Actions.ROTATE: rot, Actions.CLIMB: climb}

    return agent_actions


def test_run_check():
    agent_1 = Agent()
    agent_2 = Agent()
    agents = [agent_1, agent_2]

    actions = {}

    for agent in agents:
        actions[agent] = generate_actions()
    print(actions)

    return actions


# TODO make a really small env with one easy exit --
# set the engine loop with actions/terminations/episodes

def test_engine():
    agent_1 = Agent(range_observation=3)
    agent_2 = Agent(range_observation=3)

    simple_jungle = EmptyJungle(size=5)

    simple_jungle.add_agents(agent_1, agent_2)
    simple_jungle.add_object(ElementsEnv.EXIT_EASY, (0, 4))
    print(agent_1.grid_position, agent_2.grid_position)

    run(100, simple_jungle.agents, simple_jungle, agent_1, agent_2)


def test_instantiation():
    agent_1 = Agent(range_observation=3)
    agent_2 = Agent(range_observation=3)

    new_jungle = RiverExit(size=11)
    new_jungle.add_agents(agent_1, agent_2)

    run(200, new_jungle.agents, new_jungle, agent_1, agent_2)
