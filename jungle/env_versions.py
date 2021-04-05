import numpy as np
import random
import math

from jungle.jungle import EmptyJungle
from jungle.utils import ElementsEnv, Actions, Definitions

"""Basic Env with Unobstructed exits.Exit 1 is better off for White,
Exit 2 is better off for Black"""


class EasyJungle(EmptyJungle):
    super().__init__(size=11)
    pass


"""Env that requires cooperation. River Exit has a high reward for both. 
Free exit has a very low reward."""


class MediumJungle(EmptyJungle):
    super().__init__(size=11)
    pass


"""Env that requires communication + cooperation. River Exit has a 
high reward for both. Boulder exits carry a certain degree of risk. 
Boulder exit A has a high reward for agent 1 and a low reward for 
agent2. For Boulder Exit B, the converse is true.
Free exit has a very low reward."""

class DifficultJungle(EmptyJungle):
    super().__init__(size=11)
    pass
