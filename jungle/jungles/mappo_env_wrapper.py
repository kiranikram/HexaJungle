import numpy as np
from abc import ABC
from gym import spaces
from gym.spaces import MultiDiscrete, Dict, Discrete

from jungle.jungle import Jungle
from jungle.jungles import basic, rl
from jungle.jungles.rl import EasyExit
from jungle.agent import Agent
from jungle.utils import ElementsEnv, Actions, Rewards


# in config, need to add jungle class specification

class JungleWrapper(Jungle, ABC):
    def __init__(self, config, size: int):
        super().__init__(size)

        self.jungle = EasyExit(size=12)
        agent_1 = Agent(range_observation=4)
        agent_2 = Agent(range_observation=4)
        self.jungle.add_agents(agent_1, agent_2)

        self.n_agents = 2  # should come from config
        self.action_space = []
        self.observation_space = []
        self.share_observation_space = []

        for idx in range(self.n_agents):
            self.observation_space.append(spaces.Box(low=-1, high=1,
                                                     shape=(258,), dtype=np.int64))
            self.action_space.append(spaces.MultiDiscrete([2, 3, 2]))

        self.share_observation_space = [spaces.Box(low=1, high=1, shape=(258,), dtype=np.int64) for _ in
                                        range(self.n_agents)]
