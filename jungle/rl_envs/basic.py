from jungle.jungle import EmptyJungle
from jungle.utils import ElementsEnv


class EasyExit(EmptyJungle):

    def __init__(self, size):

        super().__init__(size)

        exit_1 = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_EASY, exit_1.coordinates)


class RiverExit(EmptyJungle):

    def __init__(self, size):

        super().__init__(size)

        exit_1 = self.select_random_exit()
        self.add_object(ElementsEnv.EXIT_DIFFICULT, exit_1.coordinates)
        self.add_object(ElementsEnv.RIVER, exit_1.surrounding_1)
        self.add_object(ElementsEnv.RIVER, exit_1.surrounding_2)
