from jungle.utils import Definitions


"""For Rotation angles reference:
 . . . . . .  . .
. . . . 2 1 . . .
 . . . 3 A 0 . .
. . . . 4 5 . . .
 . . . . . . . . """





class Agent:

    def __init__(self, range_observation=None):

        self.color = None
        self.range_observation = range_observation
        self.grid_position = None
        self.starting_position = None
        self.starting_angle = None

        # similar to angle, use a property instead to make sure that you don't go beyond max number of logs allowed
        self.wood_logs = 0
        self.on_shoulders = False

        self.current_actions = None

        # @MG these is temporary , will be removed from final codebase - only to help me build
        self.left_view_obstructed = False
        self.right_view_obstructed = False
        self.bottom_view_obstructed = False
        self.top_view_obstructed = False
        self.top_left_obstructed = False
        self.top_right_obstructed = False
        self.bottom_left_obstructed = False
        self.bottom_right_obstructed = False

        self.last_obs = None

        self.done = False

    @property
    def wood_logs(self):
        return self._wood_logs

    @wood_logs.setter
    def wood_logs(self, wood_log):
        self._wood_logs = wood_log
        if self._wood_logs > 2:
            self._wood_logs = 2

    @property
    def done(self):
        return self._done

    @done.setter
    def done(self, done_bool):
        if done_bool:
            self.grid_position = None
        self._done = done_bool

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

    def apply_action(self, actions):
        if self.done:
            actions = {k: a * 0 for k, a in actions.items()}

        self.current_actions = actions
        print(self.current_actions.items())


