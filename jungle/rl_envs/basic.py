from jungle.jungle import EmptyJungle
from jungle.utils import ElementsEnv


class EasyExit(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        self.exit_1 = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_EASY, self.exit_1.coordinates)


class RiverExit(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        self.exit_1 = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.exit_1.coordinates)
        self.add_object(ElementsEnv.RIVER, self.exit_1.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.exit_1.surrounding_2)

        self.add_trees()

    def reset(self):
        self.reinitialize_grid()

        self.swap_agent_positions()
        self.calculate_exit_coordinates()

        # exit_1 = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self.exit_1.coordinates)
        self.add_object(ElementsEnv.RIVER, self.exit_1.surrounding_1)
        self.add_object(ElementsEnv.RIVER, self.exit_1.surrounding_2)

        obs = {'white': self.generate_agent_obs(self.agent_white),
               'black': self.generate_agent_obs(self.agent_black)}

        return obs


class BoulderExit(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        exit_1 = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, exit_1.coordinates)
        self.add_object(ElementsEnv.BOULDER, exit_1.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, exit_1.surrounding_2)

        self.add_trees()


class DoubleExitsBoulder(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        free_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_EASY, free_exit.coordinates)

        boulder_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, boulder_exit.surrounding_2)

        self.add_trees()


class DoubleExitsRiver(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        free_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_EASY, free_exit.coordinates)

        river_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, river_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, river_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, river_exit.surrounding_2)

        self.add_trees()


class RiverBoulderExits(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        free_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_EASY, free_exit.coordinates)

        boulder_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, boulder_exit.surrounding_2)

        river_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, river_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, river_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, river_exit.surrounding_2)

        self.add_trees()


"""Three exits. RIVER is good for both.
One unobstructed exit is better for White.
The other unobstructed exit has low reward for both"""


class WhiteFavouredSimple(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        white_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_WHITE, white_exit.coordinates)

        # low reward for both
        free_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_EASY, free_exit.coordinates)

        # high reward for both
        river_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, river_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, river_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, river_exit.surrounding_2)

        self.add_trees()


"""Three exits. BOULDER is good for both.
One unobstructed exit is better for Black.
The other unobstructed exit has low reward for both"""


class BlackFavouredSimple(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        black_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_BLACK, black_exit.coordinates)

        # low reward for both
        free_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_EASY, free_exit.coordinates)

        # high reward for both
        boulder_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, boulder_exit.surrounding_2)

        self.add_trees()


"""Three exits, only BOULDER exit is advantageous to one agent(WHITE) over another"""


class WhiteFavoured(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        free_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_EASY, free_exit.coordinates)

        white_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_WHITE, white_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, white_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, white_exit.surrounding_2)

        river_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, river_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, river_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, river_exit.surrounding_2)

        self.add_trees()


"""Three exits, only RIVER exit is advantageous to one agent(BLACK) over another"""


class BlackFavoured(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        free_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_EASY, free_exit.coordinates)

        boulder_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, boulder_exit.surrounding_2)

        black_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_BLACK, black_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, black_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, black_exit.surrounding_2)

        self.add_trees()


class ConflictingExitsBiased(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        free_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_EASY, free_exit.coordinates)

        white_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_WHITE, white_exit.coordinates)

        boulder_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, boulder_exit.surrounding_2)

        black_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_BLACK, black_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, black_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, black_exit.surrounding_2)

        self.add_trees()


class ConflictingExits(EmptyJungle):

    def __init__(self, size):
        super().__init__(size)

        black_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_BLACK, black_exit.coordinates)

        white_exit = self.select_random_exit()
        self.add_object(ElementsEnv.WHITE, white_exit.coordinates)

        boulder_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, boulder_exit.coordinates)
        self.add_object(ElementsEnv.BOULDER, boulder_exit.surrounding_1)
        self.add_object(ElementsEnv.BOULDER, boulder_exit.surrounding_2)

        river_exit = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, river_exit.coordinates)
        self.add_object(ElementsEnv.RIVER, river_exit.surrounding_1)
        self.add_object(ElementsEnv.RIVER, river_exit.surrounding_2)

        self.add_trees()
