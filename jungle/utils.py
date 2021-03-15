from enum import IntEnum, Enum, auto


class ElementsEnv(Enum):

    # by using auto you are not assigning any pr-determined value for these.
    # this becomes more flexible as you can just add any and not worry if the number is already taken.

    # you should give more meaningful names to exits.
    # e.g EXIT_HIGH_REWARD, EXIT_MIDDLE_REWARD, EXIT_LOW_REWARD, EXIT_WHITE, EXIT_BLACK

    # each exit has a specific type of reward property, based on exit type eg rivers requires
    # cooperation as they both need to have picked up logs

    FREE_EXIT = auto()
    RIVER_EXIT = auto()
    BOULDER_EXIT = auto()
    RIVER = auto()
    BOULDER = auto()
    TREE = auto()
    OBSTACLE = auto()  # non traversable, can't climb it


class Definitions(Enum):
    BLACK = 0
    WHITE = 1
    MIN_SIZE_ENVIR = 5

# Quite sure ou don't need that. see later.
# ref to test available actions
# class C_Actions(IntEnum):
#     KeepOrientation = 0
#     RotateLeft = 1
#     RotateRight = -1
#     MoveForward = 2
#     StandStill = 3
#     Climb = 4


# Just an Actions definition with enum is sufficient.
# Their effect will be decided in the code
# this is just to name things to make them more readable.
class Actions(IntEnum):
    ROTATE = auto()
    FORWARD = auto()

# we don't need that:
#Forward = [1,0]
#Rotate = [-1,0, 1]





