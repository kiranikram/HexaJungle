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


class RLlibWrapper(MultiAgentEnv):

    """

    How it should be used, fr

    agent_1 = Agent(4)
    agent_2 = Agent(4)
    jungle = Jungle(11)

    env = RLlibWrapper(jungle)


    """

    def __init__(self, jungle):

        self.jungle = jungle
        self.action_space = spaces.Dict(
            {'Forward': spaces.Discrete(2), 'Rotate': spaces.Discrete(3), 'Climb': spaces.Discrete(2)})
        self.observation_space = spaces.Dict(spaces.Box(low=0, high=15, shape=(2,)))

        # @KI not sure you need to add agents separately, you can add them when you create the jungle.
    #     self.instantiate_agents()
    #
    # def instantiate_agents(self):
    #     agent_1 = Agent(range_observation=4)
    #     agent_2 = Agent(range_observation=4)
    #
    #     self.jungle.add_agents(agent_1, agent_2)

    def step(self, actions):

        actions_black = actions['agent_black']
        # here modify actions_black so that the format is understood by jungle.

        actions_white = actions['agent_black']
        # here modify actions_white so that the format is understood by jungle.

        actions_dict = {self.jungle.agent_white: actions_white,
                        self.jungle.agent_black: actions_black}

        obs, rewards, done = self.Jungle.step(actions)

        # Here modify obs, rewards and done so that they are understood by rllib

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

        # you need to implement reset in jungle
        obs = self.jungle.reset()

        # modify obs to make it compatible with rllib,

        return obs
