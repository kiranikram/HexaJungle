from jungle.jungle import Jungle
from jungle.utils import ElementsEnv
from copy import deepcopy


class EasyExit(Jungle):

    def _set_exits(self):
        self.exit_1 = self.select_random_exit()
        self.exit_2 = self.select_random_exit()
        self.add_objects()

    def _set_elements(self):
        pass

    def reset(self):
        self.grid_env[:] = deepcopy(self._initial_grid)

        self._place_agents()
        self._assign_colors()
        self.add_objects()

        self.agents[0].reset()
        self.agents[1].reset()

        obs = {self.agents[0]: self.generate_agent_obs(self.agents[0]),
               self.agents[1]: self.generate_agent_obs(self.agents[1])}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_EASY, self.exit_1.coordinates)
        self.add_object(ElementsEnv.EXIT_EASY, self.exit_1.surrounding_1)
        self.add_object(ElementsEnv.EXIT_EASY, self.exit_1.surrounding_2)
        self.add_object(ElementsEnv.RIVER, self.exit_2.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.exit_2.surrounding_2)


class NotEasyExit(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.exit_1 = self.select_random_exit()
        self.exit_2 = self.select_random_exit()
        self.add_objects()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.add_objects()
        self.agent_white.done = False
        self.agent_black.done = False

        # print('IN RESET FUNC OF EASY EXIT')
        # if self.agent_white.done:
        # print('ag white done')

        # if self.agent_black.done:
        # print('ag black done')

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_EASY, self.exit_1.coordinates)
        self.add_object(ElementsEnv.EXIT_EASY, self.exit_1.surrounding_1)
        self.add_object(ElementsEnv.EXIT_EASY, self.exit_1.surrounding_2)
        self.add_object(ElementsEnv.RIVER, self.exit_2.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.exit_2.surrounding_2)


class RiverExit(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.exit_1 = self.select_random_exit()

        self.add_trees()
        self.add_objects()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.agent_white.done = False
        self.agent_black.done = False
        self.add_objects()
        self.add_trees()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.exit_1.coordinates)
        self.add_object(ElementsEnv.RIVER, self.exit_1.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.exit_1.surrounding_2)
        self.add_trees()


class BoulderExit(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.exit_1 = self.select_random_exit()

        self.add_trees()
        self.add_objects()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.agent_white.done = False
        self.agent_black.done = False
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.exit_1.coordinates)
        self.add_object(ElementsEnv.BOULDER, self.exit_1.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, self.exit_1.surrounding_2)
        self.add_trees()


class DoubleExitsBoulder(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.free_exit = self.select_random_exit()

        self.boulder_exit = self.select_random_exit()

        self.add_trees()
        self.add_objects()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.agent_white.done = False
        self.agent_black.done = False
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_EASY, self.free_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_2)
        self.add_trees()


class DoubleExitsRiver(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.free_exit = self.select_random_exit()

        self.river_exit = self.select_random_exit()

        self.add_trees()
        self.add_objects()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.agent_white.done = False
        self.agent_black.done = False
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_EASY, self.free_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.river_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_2)
        self.add_trees()


class RiverBoulderExits(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.free_exit = self.select_random_exit()

        self.boulder_exit = self.select_random_exit()

        self.river_exit = self.select_random_exit()

        self.add_objects()

        self.add_trees()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.agent_white.done = False
        self.agent_black.done = False
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_EASY, self.free_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_2)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.river_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_2)
        self.add_trees()


"""Three exits. RIVER is good for both.
One unobstructed exit is better for White.
The other unobstructed exit has low reward for both"""


class WhiteFavouredSimple(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.white_exit = self.select_random_exit()

        # low reward for both
        self.free_exit = self.select_random_exit()

        # high reward for both
        self.river_exit = self.select_random_exit()

        self.add_trees()
        self.add_objects()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.agent_white.done = False
        self.agent_black.done = False
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_WHITE, self.white_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_EASY, self.free_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.river_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_2)
        self.add_trees()


"""Three exits. BOULDER is good for both.
One unobstructed exit is better for Black.
The other unobstructed exit has low reward for both"""


class BlackFavouredSimple(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.black_exit = self.select_random_exit()

        # low reward for both
        self.free_exit = self.select_random_exit()

        # high reward for both
        self.boulder_exit = self.select_random_exit()

        self.add_trees()
        self.add_objects()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.agent_white.done = False
        self.agent_black.done = False
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_BLACK, self.black_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_EASY, self.free_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.boulder_exit.surrounding_2)
        self.add_trees()


"""Three exits, only BOULDER exit is advantageous to one agent(WHITE) over another"""


class WhiteFavoured(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.free_exit = self.select_random_exit()

        self.white_exit = self.select_random_exit()

        self.river_exit = self.select_random_exit()

        self.add_trees()
        self.add_objects()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.agent_white.done = False
        self.agent_black.done = False
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_EASY, self.free_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_WHITE, self.white_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, self.white_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, self.white_exit.surrounding_2)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.river_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_2)
        self.add_trees()


"""Three exits, only RIVER exit is advantageous to one agent(BLACK) over another"""


class BlackFavoured(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.free_exit = self.select_random_exit()

        self.boulder_exit = self.select_random_exit()

        self.black_exit = self.select_random_exit()

        self.add_trees()
        self.add_objects()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.agent_white.done = False
        self.agent_black.done = False
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_EASY, self.free_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_2)
        self.add_object(ElementsEnv.EXIT_BLACK, self.black_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, self.black_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.black_exit.surrounding_2)
        self.add_trees()


class ConflictingExitsBiased(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.free_exit = self.select_random_exit()

        self.white_exit = self.select_random_exit()

        self.boulder_exit = self.select_random_exit()

        self.black_exit = self.select_random_exit()

        self.add_trees()
        self.add_objects()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.agent_white.done = False
        self.agent_black.done = False
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_EASY, self.free_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_WHITE, self.white_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_2)
        self.add_object(ElementsEnv.EXIT_BLACK, self.black_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, self.black_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.black_exit.surrounding_2)


class ConflictingExits(Jungle):

    def __init__(self, size):
        super().__init__(size)

        self.black_exit = self.select_random_exit()

        self.white_exit = self.select_random_exit()

        self.boulder_exit = self.select_random_exit()

        self.river_exit = self.select_random_exit()

        self.add_trees()
        self.add_objects()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.agent_white.done = False
        self.agent_black.done = False
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_BLACK, self.black_exit.coordinates)
        self.add_object(ElementsEnv.WHITE, self.white_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_2)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.river_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_2)
