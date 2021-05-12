from jungle.utils import MAX_WOOD_LOGS, Actions, BLACK, WHITE
import random

"""For Rotation angles reference:
 . . . . . .  . .
. . . . 2 1 . . .
 . . . 3 A 0 . .
. . . . 4 5 . . .
 . . . . . . . . """

arrows_white = {0: 8680, 1: 11008, 2: 11009, 3: 8678, 4: 11011, 5: 11010}
arrows_black = {0: 11157, 1: 11016, 2: 11017, 3: 11013, 4: 11019, 5: 11018}


class Agent:

    def __init__(self, range_observation=2):


        self._color = None

        assert range_observation > 0
        self.range_observation = range_observation
        self.position = None

        # similar to angle, use a property instead to make sure that you don't go beyond max number of logs allowed
        self.wood_logs = 0
        self.on_shoulders = False

        self._done = False

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, col):
        self._color = col


    
    @staticmethod
    def get_random_actions():

        actions = { Actions.FORWARD: random.choice((0, 1)),
                    Actions.CLIMB: random.choice((0, 1)),
                    Actions.ROTATE: random.choice((-1, 0, 1))
        }

        return actions

    def __repr__(self):

        if self.color is BLACK:
            return chr(arrows_white[self.angle])
        elif self.color is WHITE:
            return chr(arrows_black[self.angle])

    @property
    def wood_logs(self):
        return self._wood_logs

    @wood_logs.setter
    def wood_logs(self, wood_log):
        self._wood_logs = wood_log
        if self._wood_logs > MAX_WOOD_LOGS:
            self._wood_logs = MAX_WOOD_LOGS

    @property
    def done(self):
        return self._done

    @done.setter
    def done(self, done_bool):
        if done_bool:
            self.grid_position = None
        self._done = done_bool

    @property
    def position(self):

        if self.done:
            return None

        return self._r, self._c

    @position.setter
    def position(self, pos):

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

    def apply_action(self, actions):
        if self.done:
            actions = {k: a * 0 for k, a in actions.items()}

        self.current_actions = actions

    def reset(self):
        self.wood_logs = 0
        self.on_shoulders = False
        self.done = False



