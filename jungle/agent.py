from jungle.utils import Definitions
from jungle.utils_agent import Actions

"""For Rotation angles reference:
 . . . . . .  . .
. . . . 2 1 . . .
 . . 3 . A . 0 . .
. . . . 4 5 . . .
 . . . . . . . . """

class Agent:

    def __init__(self, range_observation):

        self.color = None
        self.range_observation = range_observation
        self.grid_position = None

        # similar to angle, use a property instead to make sure that you don't go beyond max number of logs allowed
        self.wood_logs = 0

        self.done = False

    @property
    def grid_position(self):
        return self._r, self._c

    @grid_position.setter
    def grid_position(self, pos):

        if pos is None:
            self._r = None
            self._c = None

        else:
            self._r, self._c = pos

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):

        # Make sure that angles are between 0 to 5
        self._angle = angle % 6

    # @property
    # def carthesian_coordinates(self):
    #
    #     # TODO: convert grid_position to cartesian position
    #     x = ...
    #     y = /




