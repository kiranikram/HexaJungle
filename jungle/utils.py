from enum import IntEnum, Enum, auto


class ElementsEnv(Enum):
    # by using auto you are not assigning any pr-determined value for these.
    # this becomes more flexible as you can just add any and not worry if the number is already taken.

    # you should give more meaningful names to exits.
    # e.g EXIT_HIGH_REWARD, EXIT_MIDDLE_REWARD, EXIT_LOW_REWARD, EXIT_WHITE, EXIT_BLACK

    # each exit has a specific type of reward property, based on exit type eg rivers requires
    # cooperation as they both need to have picked up logs

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


class Definitions(Enum):
    BLACK = 0
    WHITE = 1
    MIN_SIZE_ENVIR = 5
    LOG_RATE = 3
    REWARD_BUMP = -5
    REWARD_CUT_TREE = -2
    REWARD_EXIT_AVERAGE = 15
    REWARD_EXIT_HIGH = 50
    REWARD_EXIT_VERY_HIGH = 100
    REWARD_EXIT_LOW = 5
    REWARD_DROWN = -50
    REWARD_BUILT_BRIDGE = 35




# Just an Actions definition with enum is sufficient.
# Their effect will be decided in the code
# this is just to name things to make them more readable.
class Actions(IntEnum):
    ROTATE = auto()
    FORWARD = auto()


