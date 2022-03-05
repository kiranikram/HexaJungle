"""
Test module for Shared Buffer
"""
import random
import pytest

from jungle.agent import Agent
from jungle.utils import (Actions, Rewards, ElementsEnv, MIN_SIZE_ENVIR, BLACK,
                          WHITE)

from jungle.jungles.basic import EmptyJungle