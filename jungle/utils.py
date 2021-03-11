from enum import IntEnum, Enum


class ElementsEnv(Enum):
    EXIT_ONE = 0
    EXIT_TWO = 1
    EXIT_THREE = 3
    RIVER = 5
    BOULDER = 7
    TREE = 9


class Definitions(Enum):
    BLACK = 0
    WHITE = 1


class Actions(IntEnum):
    KeepOrientation = 0
    RotateLeft = 1
    RotateRight = -1
    MoveForward = 2
    StandStill = 3
    Climb = 4
