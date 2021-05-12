from enum import IntEnum, Enum, auto

MIN_SIZE_ENVIR = 5
MAX_WOOD_LOGS = 2
BLACK = 0
WHITE = 1


class ElementsEnv(Enum):

    EMPTY = auto()
    EXIT_EASY = auto()
    EXIT_DIFFICULT = auto()
    EXIT_WHITE = auto()
    EXIT_BLACK = auto()
    RIVER = auto()
    BOULDER = auto()
    TREE = auto()
    OBSTACLE = auto()  # non traversable, can't climb it
    BRIDGE = auto()
    AGENT = auto()

display_dict = {
    ElementsEnv.EMPTY.value:  '.',
    ElementsEnv.EXIT_EASY.value: 'e',
    ElementsEnv.EXIT_DIFFICULT.value: 'E',
    ElementsEnv.EXIT_WHITE.value: 'EW',
    ElementsEnv.EXIT_BLACK.value: 'EB',
    ElementsEnv.RIVER.value : 'R',
    ElementsEnv.BOULDER.value : 'B',
    ElementsEnv.TREE.value : 'T',
    ElementsEnv.OBSTACLE.value : 'X'
}

class Rewards(Enum):
    # bring all in range of (-10,10)
    REWARD_COLLISION = -1
    REWARD_CUT_TREE = -2
    REWARD_EXIT_LOW = 25
    # changed from 50
    REWARD_EXIT_AVERAGE = 100
    REWARD_EXIT_HIGH = 200
    REWARD_EXIT_VERY_HIGH = 200
    # changed from -100
    REWARD_DROWN = -50
    REWARD_FELL = -2
    REWARD_CARRYING = -3
    REWARD_BUILD_BRIDGE = 50

# Just an Actions definition with enum is sufficient.
# Their effect will be decided in the code
# this is just to name things to make them more readable.
class Actions(IntEnum):
    ROTATE = auto()
    FORWARD = auto()
    CLIMB = auto()
