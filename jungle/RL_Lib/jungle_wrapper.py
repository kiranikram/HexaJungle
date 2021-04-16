import argparse
import os
import ray
import random
from ray import tune
from gym import spaces
from gym.spaces import MultiDiscrete, Dict, Discrete
from collections import namedtuple
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from ray.rllib.utils.annotations import override
from ray.rllib.utils.typing import MultiAgentDict, PolicyID, AgentID
from jungle.rl_envs.basic import RiverExit
from jungle.utils import ElementsEnv, Actions, Definitions
from jungle.observations import restrict_observations
from jungle.agent import Agent
from jungle.jungle import EmptyJungle





class Jungle2(MultiAgentEnv):
    def __init__(self, config):


        self.Jungle = EmptyJungle(config['size'])
        self.action_space = spaces.Dict(
            {'Forward': spaces.Discrete(3), 'Rotate': spaces.Discrete(3), 'Climb': spaces.Discrete(2)})
        self.observation_space = spaces.Dict(spaces.Box(low=0, high=15, shape=(2,)))
        self.instantiate_agents()

    def instantiate_agents(self):
        agent_1 = Agent(range_observation=4)
        agent_2 = Agent(range_observation=4)

        self.Jungle.add_agents(agent_1, agent_2)



    def step(self, actions):

        obs, rewards, done = self.Jungle.step(actions)

        if done:
            done = dict({"__all__": True}, **{agent_id: True for agent_id in self.agents})
        else:
            done = dict({"__all__": False})

        return obs, rewards, done

    def reset(self):

        # reset grid position s
        # agents have to go back to original position
        # could actually switch role ; reassign role
        # reset trees
        actions = {}
        obs, _, _ = self.Jungle.step(actions)

        return obs
