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

class JungleWrapper(MultiAgentEnv):
    def __init__(self, RiverExit):
        agent_1 = Agent()
        agent_2 = Agent

        self.RiverExit = RiverExit
        self.action_space = spaces.Dict({'Forward': spaces.Discrete(3), 'Rotate': spaces.Discrete(3), 'Climb':spaces.Discrete(2)})
        self.observation_space = spaces.Box(low=0, high=15, shape=(2,))
        self.add_agents(agent_1,agent_2)

    def step(self, actions):

        # First Physical move
        if not self.agent_white.done:
            rew_white = self.move(self.agent_white, actions)
            white_climbs = actions.get(self.agent_white, {}).get(Actions.CLIMB, 0)
        else:
            rew_white = 0
            white_climbs = False

        if not self.agent_black.done:
            rew_black = self.move(self.agent_black, actions)
            black_climbs = actions.get(self.agent_black, {}).get(Actions.CLIMB, 0)
        else:
            rew_black = 0
            black_climbs = False

        # Then Test for different cases

        # If both on same position:
        # This will be false if one agent is done

        if self.agent_white.grid_position == self.agent_black.grid_position:

            r, c = self.agent_white.grid_position

            # TREE
            if self.grid_env[r, c] == ElementsEnv.TREE.value:
                # If they are on a tree they cut it
                self.grid_env[r, c] = ElementsEnv.EMPTY.value

                # one of them only gets the log
                if random.random() > 0.5:
                    self.agent_black.wood_logs += 1
                else:
                    self.agent_white.wood_logs += 1

                # But both have neg reward from the effort
                rew_white += Definitions.REWARD_CUT_TREE.value
                rew_black += Definitions.REWARD_CUT_TREE.value

            # RIVER
            if self.grid_env[r, c] == ElementsEnv.RIVER.value:

                # If they have enough logs they build a bridge
                if self.agent_white.wood_logs + self.agent_black.wood_logs == 4:
                    self.agent_white.wood_logs = 0
                    self.agent_black.wood_logs = 0
                    self.grid_env[r, c] = ElementsEnv.EMPTY.value
                    rew_black += Definitions.REWARD_BUILT_BRIDGE.value
                    rew_white += Definitions.REWARD_BUILT_BRIDGE.value

                # else they will drown, but we will see that later.
                else:
                    self.agent_white.done = True
                    # @MG white was repeated, so changed to black
                    self.agent_black.done = True
                    rew_white += Definitions.REWARD_DROWN.value
                    rew_black += Definitions.REWARD_DROWN.value

            # BOULDER

            if self.grid_env[r, c] == ElementsEnv.BOULDER.value:
                # if one agent is on shoulders, they can cross
                if self.agent_white.on_shoulders or self.agent_black.on_shoulders:
                    rew_white += Definitions.REWARD_CROSS_BOULDER.value
                    rew_black += Definitions.REWARD_CROSS_BOULDER.value

            # CLIMB Behavior if they are on the same cell

            if white_climbs and not black_climbs:
                self.agent_white.on_shoulders = True
                rew_black += Definitions.REWARD_CARRYING.value

            elif black_climbs and not white_climbs:
                self.agent_black.on_shoulders = True
                rew_white += Definitions.REWARD_CARRYING.value

            elif black_climbs and white_climbs:
                rew_white += Definitions.REWARD_FELL.value
                rew_black += Definitions.REWARD_FELL.value

        # If not on the same cell
        else:

            # If agent was on shoulders, but other agent moved:
            if self.agent_black.on_shoulders:
                self.agent_black.on_shoulders = False
                rew_black += Definitions.REWARD_FELL.value

            if self.agent_white.on_shoulders:
                self.agent_white.on_shoulders = False
                rew_white += Definitions.REWARD_FELL.value

            # If try to climb, fails
            if black_climbs:
                rew_black += Definitions.REWARD_FELL.value

            if white_climbs:
                rew_white += Definitions.REWARD_FELL.value

        # Apply environment rules

        if not self.agent_black.done:
            rew, self.agent_black.done = self.apply_rules(self.agent_black)
            rew_black += rew

        if not self.agent_white.done:
            rew, self.agent_white.done = self.apply_rules(self.agent_white)
            rew_white += rew

        # All rewards and terminations are now calculated
        rewards = {self.agent_black: rew_black, self.agent_white: rew_white}

        if self.agent_white.done and self.agent_black.done:
            done = dict({"__all__": True}, **{agent_id: True for agent_id in self.agents})
        else:
            done = dict({"__all__": False})

        # Now we calculate the observations
        obs = {}
        # obs[self.agent_white] = []#self.generate_agent_obs(self.agent_white)
        # obs[self.agent_black] = []#self.generate_agent_obs(self.agent_black)
        if not self.agent_white.done:
            obs[self.agent_white] = self.generate_agent_obs(self.agent_white)
        if not self.agent_black.done:
            obs[self.agent_black] = self.generate_agent_obs(self.agent_black)

        return obs, rewards, done

    def reset(self):

        # returns starting obs for each agent
        obs = {}
        # obs[self.agent_white] = []#self.generate_agent_obs(self.agent_white)
        # obs[self.agent_black] = []#self.generate_agent_obs(self.agent_black)
        if not self.agent_white.done:
            obs[self.agent_white] = self.generate_agent_obs(self.agent_white)
        if not self.agent_black.done:
            obs[self.agent_black] = self.generate_agent_obs(self.agent_black)

        return obs
