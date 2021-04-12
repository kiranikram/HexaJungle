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


def run(max_steps, agents, env, agent_1,agent_2):
    for x in range(max_steps):
        print('step', x)
        actions = {}
        for agent in agents:
            actions[agent] = generate_actions()

            obs, reward, done = env.step(actions)
            print('obs',obs)
            print(agent_1.grid_position)
            print(agent_2.grid_position)





def run_one_episode(env, verbose=False):
    env.reset()
    sum_reward = 0

    # change here
    for i in range(env.MAX_STEPS):
        action = env.action_space.sample()

        if verbose:
            print("action:", action)

        obs, rewards, done = env.step(action)
        sum_reward += rewards

        if done:
            if verbose:
                print("done @ step {}".format(i))

            break

    if verbose:
        print("cumulative reward", sum_reward)

    return sum_reward


acts = run_check()
print(acts)
