from utils import Actions, Definitions


class Agent:

    def __init__(self, initial_r, initial_c, angle,range):
        """Agent base class
        default color is black
        """
        self.color = Definitions.BLACK
        self.grid_position = initial_r, initial_c
        self.initial_position = None
        self.angle = angle
        self.range = range

        @property
        def grid_position(self):
            return self._r, self._c

        @property
        def angle(self):
            return self.angle

        def apply_actions(self):
            pass
