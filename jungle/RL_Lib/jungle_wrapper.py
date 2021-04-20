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

        sa_action_space = spaces.MultiDiscrete([2, 3, 2])
        self.action_space = spaces.MultiDiscrete([2, 3, 2])
        # self.action_space = spaces.Tuple(tuple(2 * [sa_action_space]))
        # sa_observation_space = spaces.Box(low=0, high=10,
        # shape=(1,))
        #self._set_obs_space()
        self.observation_space= spaces.Box(low=0, high=10,
                   shape=(1,))
        # self.observation_space = spaces.Tuple(tuple(2 * [sa_observation_space]))
        # self.observation_space = spaces.Tuple(tuple(spaces.Box(low=0, high=self.jungle.size, shape=(1,))))



    def _set_obs_space(self):
        obs_dict = {self.jungle.agent_white: spaces.Box(low=0, high=10,
                                                        shape=(1,)), self.jungle.agent_black: spaces.Box(low=0, high=10,
                                                                                                         shape=(1,))}
        print(obs_dict)
        self.observation_space = obs_dict

    ### from docs : # A dict keyed by agent ids, e.g. {"agent-1": value}.
    # MultiAgentDict = Dict[AgentID, Any]
    def step(self, actions):
        agents = [*actions]
        print('here', agents)
        if agents[0] == self.jungle.agent_white:
            actions_white = actions[agents[0]]
            actions_black = actions[agents[1]]

        else:
            actions_white = actions[agents[1]]
            actions_black = actions[agents[0]]

        # actions_black = actions[0]
        black_fwd = actions_black[0]
        black_rot = actions_black[1]
        black_climb = actions_black[2]

        black_dict = {Actions.FORWARD: black_fwd, Actions.ROTATE: black_rot, Actions.CLIMB: black_climb}

        # actions_white = actions[1]
        white_fwd = actions_white[0]
        white_rot = actions_white[1]
        white_climb = actions_white[2]

        white_dict = {Actions.FORWARD: white_fwd, Actions.ROTATE: white_rot, Actions.CLIMB: white_climb}

        print('here')

        # actions_black = actions['agent_black']
        # here modify actions_black so that the format is understood by jungle.

        # actions_white = actions['agent_white']
        # here modify actions_white so that the format is understood by jungle.

        actions_dict = {self.jungle.agent_white: white_dict,
                        self.jungle.agent_black: black_dict}

        print(actions_dict)

        obs, rewards, done = self.jungle.step(actions_dict)
        print(obs)

        # Here modify obs, rewards and done so that they are understood by rllib

        if done:
            done = dict({"__all__": True}, **{agent_id: True for agent_id in self.agents})
        else:
            done = dict({"__all__": False})

        # return obs, rewards, done

    def reset(self):

        # reset grid position s
        # agents have to go back to original position
        # could actually switch role ; reassign role
        # reset trees

        # you need to implement reset in jungle
        obs = self.jungle.reset()

        #obs = {self.jungle.agent_white: self.generate_agent_obs(self.agent_white),
               #self.jungle.agent_black: self.generate_agent_obs(self.agent_black)}
        return obs

        # modify obs to make it compatible with rllib,


