from jungle.jungle import EmptyJungle
from jungle.utils import ElementsEnv


class EasyExit(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        self.exit_1 = self.select_random_exit()
        self.exit_2 = self.select_random_exit()
        self.add_objects()
        print('we here ')

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_EASY, self.exit_1.coordinates)
        self.add_object(ElementsEnv.RIVER, self.exit_2.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.exit_2.surrounding_2)



class RiverExit(EmptyJungle):

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
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.exit_1.coordinates)
        self.add_object(ElementsEnv.RIVER, self.exit_1.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.exit_1.surrounding_2)


class BoulderExit(EmptyJungle):

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
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.exit_1.coordinates)
        self.add_object(ElementsEnv.BOULDER, self.exit_1.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, self.exit_1.surrounding_2)


class DoubleExitsBoulder(EmptyJungle):

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
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_EASY, self.free_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, self.boulder_exit.surrounding_2)


class DoubleExitsRiver(EmptyJungle):

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
        self.add_objects()

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs

    def add_objects(self):
        self.add_object(ElementsEnv.EXIT_EASY, self.free_exit.coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.river_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.river_exit.surrounding_2)


class RiverBoulderExits(EmptyJungle):

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


"""Three exits. RIVER is good for both.
One unobstructed exit is better for White.
The other unobstructed exit has low reward for both"""


class WhiteFavouredSimple(EmptyJungle):

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


"""Three exits. BOULDER is good for both.
One unobstructed exit is better for Black.
The other unobstructed exit has low reward for both"""


class BlackFavouredSimple(EmptyJungle):

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


"""Three exits, only BOULDER exit is advantageous to one agent(WHITE) over another"""


class WhiteFavoured(EmptyJungle):

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


"""Three exits, only RIVER exit is advantageous to one agent(BLACK) over another"""


class BlackFavoured(EmptyJungle):

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


class ConflictingExitsBiased(EmptyJungle):

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


class ConflictingExits(EmptyJungle):

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
