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


str_dict = {
    ElementsEnv.EMPTY.value: '.',
    ElementsEnv.EXIT_EASY.value: 'e',
    ElementsEnv.EXIT_DIFFICULT.value: 'E',
    ElementsEnv.EXIT_WHITE.value: 'E',
    ElementsEnv.EXIT_BLACK.value: 'E',
    ElementsEnv.RIVER.value: 'R',
    ElementsEnv.BOULDER.value: 'B',
    ElementsEnv.TREE.value: 'T',
    ElementsEnv.OBSTACLE.value: 'X'
}

display_dict = {
    ElementsEnv.EMPTY.value: [150, 250, 150],
    ElementsEnv.EXIT_EASY.value: [100, 30, 30],
    ElementsEnv.EXIT_DIFFICULT.value: [250, 30, 30],
    ElementsEnv.EXIT_WHITE.value: [255, 255, 255],
    ElementsEnv.EXIT_BLACK.value: [0, 0, 0],
    ElementsEnv.RIVER.value: [175, 238, 238],
    ElementsEnv.BOULDER.value: [205, 133, 63],
    ElementsEnv.TREE.value: [34, 139, 34],
    ElementsEnv.OBSTACLE.value: [140, 70, 20]
}


class Rewards(Enum):
    # bring all in range of (-10,10)
    REWARD_COLLISION = -1
    REWARD_CUT_TREE = -2
    REWARD_EXIT_LOW = 25
    REWARD_EXIT_AVERAGE = 50
    REWARD_EXIT_HIGH = 75
    REWARD_EXIT_VERY_HIGH = 100
    REWARD_DROWN = -100
    REWARD_FELL = -2
    REWARD_CARRYING = -3


# Just an Actions definition with enum is sufficient.
# Their effect will be decided in the code
# this is just to name things to make them more readable.
class Actions(IntEnum):
    ROTATE = auto()
    FORWARD = auto()
    CLIMB = auto()
