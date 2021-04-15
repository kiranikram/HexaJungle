import numpy as np
import random
from enum import Enum, IntEnum

import itertools
from collections import defaultdict
from jungle.agent import Agent
from jungle.utils import ElementsEnv, Actions, Definitions


def generate_actions():
    fwd = random.choice([-1, 0, 1])
    rot = random.choice([1, 0])
    climb = random.choice([1, 0])
    agent_actions = {Actions.FORWARD: fwd, Actions.ROTATE: rot, Actions.CLIMB: climb}

    return agent_actions


def run_check():
    agent_1 = Agent()
    agent_2 = Agent()
    agents = [agent_1, agent_2]

    actions = {}

    for agent in agents:
        actions[agent] = generate_actions()

    return actions


def run_one_episode(max_steps, agents, env, agent_1,agent_2):

    for x in range(max_steps):
        print('step', x)
        actions = {}
        for agent in agents:
            actions[agent] = generate_actions()

            obs, reward, done = env.step(actions)

            if agent_1.done and agent_2.done:
                break
            if not agent_1.done:
                print(agent_1.grid_position,reward[agent_1],obs[agent_1])
            if not agent_2.done:
                print(agent_2.grid_position, reward[agent_2], obs[agent_2])







