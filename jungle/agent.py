from jungle.utils import Definitions
from jungle.utils_agent import Actions


class Agent:

    def __init__(self, initial_r, initial_c, angle, range):
        """Agent base class
        default color is black
        """
        self._c = None
        self._r = None
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

    def apply_actions(self, actions):
            print(self.angle)
            # actions here are in the form of a dict
            r_now, c_now = self.grid_position
            angle_now = self.angle

            fow = 1
            rot_angle = 0
            # fow = agent[Actions.FORWARD]
            # rot_angle = agent[Actions.ROTATE]

            self.angle = (angle_now + rot_angle) % 6

            if fow != 0:
                self.grid_position = self.get_proximal_coordinate(r_now, c_now, self.angle)

    def get_proximal_coordinate(self, row, col, angle):

            row_new, col_new = row, col

            if angle == 0:
                col_new += 1
            elif angle == 1:
                row_new -= 1
                col_new += row % 2
            elif angle == 2:
                row_new -= 1
                col_new += row % 2 - 1
            elif angle == 3:
                col_new -= 1
            elif angle == 4:
                row_new += 1
                col_new += row % 2 - 1
            else:
                row_new += 1
                col_new += row % 2

            return row_new, col_new

    @angle.setter
    def angle(self, value):
        self._angle = value

    @grid_position.setter
    def grid_position(self, value):
        self._grid_position = value
