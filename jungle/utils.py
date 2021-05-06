from enum import IntEnum, Enum, auto

MIN_SIZE_ENVIR = 5
MAX_WOOD_LOGS = 2


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
    ElementsEnv.EXIT_WHITE.value: 'E',
    ElementsEnv.EXIT_BLACK.value: 'E',
    ElementsEnv.RIVER.value : 'R',
    ElementsEnv.BOULDER.value : 'B',
    ElementsEnv.TREE.value : 'T',
    ElementsEnv.OBSTACLE.value : 'X'
}



class Definitions(Enum):
    # bring all in range of (-10,10)
    BLACK = 0
    WHITE = 1
    # kill this
    LOG_RATE = 3
    # kill this as well
    RANGE_INCREASE = 2
    REWARD_COLLISION = -1
    REWARD_CUT_TREE = -2
    REWARD_EXIT_AVERAGE = 100
    REWARD_EXIT_HIGH = 50
    REWARD_EXIT_VERY_HIGH = 100
    REWARD_EXIT_LOW = 5
    REWARD_DROWN = -100
    # probably should not have this
    REWARD_BUILT_BRIDGE = 35
    # or this actually
    REWARD_CROSS_BOULDER = 35
    REWARD_FELL = -2
    REWARD_CARRYING = -5
    # remove: replace with reward fell!
    REWARD_BOTH_CLIMBED = -20
    REWARD_INVIABLE_CLIMB = -100



# Just an Actions definition with enum is sufficient.
# Their effect will be decided in the code
# this is just to name things to make them more readable.
class Actions(IntEnum):
    ROTATE = auto()
    FORWARD = auto()
    CLIMB = auto()
