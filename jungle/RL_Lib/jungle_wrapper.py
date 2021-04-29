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
from jungle import jungle
from jungle.rl_envs import basic
import numpy as np
import ipdb


class RLlibWrapper(MultiAgentEnv):
    """

    How it should be used, fr

    agent_1 = Agent(4)
    agent_2 = Agent(4)
    jungle = Jungle(11)

    env = RLlibWrapper(jungle)


    """

    def __init__(self, config):

        # self.jungle = jungle
        jungle_cls = getattr(basic, config['jungle'])
        self.jungle = jungle_cls(config['size'])

        agent_1 = Agent(range_observation=3)
        agent_2 = Agent(range_observation=3)
        self.jungle.add_agents(agent_1, agent_2)

        sa_action_space = spaces.MultiDiscrete([2, 3, 2])
        self.action_space = spaces.MultiDiscrete([2, 3, 2])
        self.white = "white"
        self.black = "black"
        # self.action_space = spaces.Tuple(tuple(2 * [sa_action_space]))
        # sa_observation_space = spaces.Box(low=0, high=10,
        # shape=(1,))
        # self._set_obs_space()
        self.observation_space = spaces.Box(low=0, high=1,
                                            shape=(208,), dtype=np.float64)
        # self.observation_space = spaces.Tuple(tuple(2 * [sa_observation_space]))
        # self.observation_space = spaces.Tuple(tuple(spaces.Box(low=0, high=self.jungle.size, shape=(1,))))

    def _set_obs_space(self):
        obs_dict = {self.jungle.agent_white: spaces.Box(low=0, high=10,
                                                        shape=(150,)), self.jungle.agent_black: spaces.Box(low=0, high=10,
                                                                                                         shape=(150,))}

        self.observation_space = obs_dict

    ### from docs : # A dict keyed by agent ids, e.g. {"agent-1": value}.
    # MultiAgentDict = Dict[AgentID, Any]

    def step(self, actions):
        print('step is being called')
        print(self.jungle)
        agents = [*actions]

        # if agents[0] == self.jungle.agent_white:
        # actions_white = actions[agents[0]]
        # actions_black = actions[agents[1]]

        # else:
        # actions_white = actions[agents[1]]
        # actions_black = actions[agents[0]]

        # ipdb.set_trace()
        if 'black' not in actions:
            actions_black = [0, 0, 0]
        else:
            actions_black = actions[self.black]

        if 'white' not in actions:
            actions_white = [0, 0, 0]
        else:
            actions_white = actions[self.white]

        # actions_black = actions[0]
        black_fwd = actions_black[0]
        black_rot = actions_black[1] - 1
        black_climb = actions_black[2]

        if black_fwd == 1:
            print('black moved fwd')
        if black_rot == -1:
            print ('black turned left')
        elif black_rot == 1:
            print ('black turned right')
        if black_climb == 1:
            print ('black tried to climb ')

        black_dict = {Actions.FORWARD: black_fwd, Actions.ROTATE: black_rot, Actions.CLIMB: black_climb}

        # actions_white = actions[1]
        white_fwd = actions_white[0]
        white_rot = actions_white[1] - 1
        white_climb = actions_white[2]

        if white_fwd == 1:
            print('white moved fwd')
        if white_rot == -1:
            print ('white turned left')
        elif white_rot == 1:
            print ('white turned right')
        if white_climb == 1:
            print ('white tried to climb ')

        white_dict = {Actions.FORWARD: white_fwd, Actions.ROTATE: white_rot, Actions.CLIMB: white_climb}

        # actions_black = actions['agent_black']
        # here modify actions_black so that the format is understood by jungle.

        # actions_white = actions['agent_white']
        # here modify actions_white so that the format is understood by jungle.

        actions_dict = {self.jungle.agent_white: white_dict,
                        self.jungle.agent_black: black_dict}

        obs, rewards, done = self.jungle.step(actions_dict)

        print('in wrapper, done is ')
        print(done)
        print('**************')

        # Here modify obs, rewards and done so that they are understood by rllib

        # if done:
        # done = dict({"__all__": True}, **{agent_id: True for agent_id in self.agents})
        # else:
        # done = dict({"__all__": False})

        info = {}

        obs, rewards = self.convert_to_wrapper_agents(obs, rewards)

        return obs, rewards, done, info

    def reset(self):
        print('reset is  being called')

        obs = self.jungle.reset()
        obs = self._convert_to_wrapper_agents(obs)

        # obs = {self.jungle.agent_white: self.generate_agent_obs(self.agent_white),
        # self.jungle.agent_black: self.generate_agent_obs(self.agent_black)}

        return obs

    def convert_to_str(self, obs, rew):
        new_obs = {'white': obs[self.jungle.agent_white], 'black': obs[self.jungle.agent_black]}
        new_reward = {'white': rew[self.jungle.agent_white], 'black': rew[self.jungle.agent_black]}
        # new_done = {'white': done[self.jungle.agent_white], 'black': done[self.jungle.agent_black]}

        return new_obs, new_reward

    def convert_to_wrapper_agents(self, obs, rew):
        import ipdb
        # ipdb.set_trace()
        # if 'black' not in obs:
        # ipdb.set_trace()

        # if 'white' not in obs:
        # ipdb.set_trace()
        new_obs = {self.white: obs['white'], self.black: obs['black']}
        new_reward = {self.white: rew['white'], self.black: rew['black']}

        return new_obs, new_reward

    def _convert_to_str(self, obs):
        new_obs = {'white': obs[self.jungle.agent_white], 'black': obs[self.jungle.agent_black]}
        return new_obs

    def _convert_to_wrapper_agents(self, obs):
        import ipdb
        # ipdb.set_trace()
        new_obs = {self.white: obs['white'], self.black: obs['black']}
        return new_obs
