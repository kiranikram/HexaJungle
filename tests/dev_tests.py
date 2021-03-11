import math
import pytest

from jungle.utils import Definitions
from jungle import baseline_env


EmptyJungle = baseline_env.JungleGrid


def test_jungle_instantiates():
    simple_jungle = EmptyJungle(size=11)

