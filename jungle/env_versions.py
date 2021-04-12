import numpy as np
import random
import math

from jungle.agent import Agent
from jungle.jungle import EmptyJungle
from jungle.utils import ElementsEnv, Actions, Definitions

"""Basic Env with Unobstructed exits.Exit 1 is better off for White,
Exit 2 is better off for Black"""


class EasyJungle(EmptyJungle):
    def __init__(self, size=11):
        super().__init__(size = size)



    def add_free_exit(self):
        pass












"""Env that requires cooperation. River Exit has a high reward for both. 
Free exit has a very low reward."""


class MediumJungle(EmptyJungle):
    def __init__(self, size=11):
        super().__init__(size=size)

    def add_difficult_exit(self):
        # coordinates for this should be top right corner.
        exit_row = 1
        exit_col = self.size - 2

        self.add_object(ElementsEnv.EXIT_DIFFICULT, (exit_row, exit_col))
        self.add_object(ElementsEnv.RIVER, )
        self.add_object(ElementsEnv.RIVER, )

    def add_free_exit(self):
        pass

    def add_trees(self):
        pass


# given a specific area, not counting where agents are,
# add a certain number of trees depending on the size of the env




"""Env that requires communication + cooperation. River Exit has a 
high reward for both. Boulder exits carry a certain degree of risk. 
Boulder exit A has a high reward for agent 1 and a low reward for 
agent2. For Boulder Exit B, the converse is true.
Free exit has a very low reward."""

# class DifficultJungle(EmptyJungle):
# super().__init__(size=11)
# pass
