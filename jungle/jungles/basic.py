from jungle.jungle import Jungle
from jungle.utils import ElementsEnv


class TreeJungle(Jungle):
    """
    Empty Jungle with half the empty cells with trees.
    No Exit.
    """

    def _set_exits(self):
        pass

    def _set_elements(self):

        quantity_trees = int( (self.size - 2)**2 / 2)

        for i in range(quantity_trees):

            r, c = self.get_random_empty_location()
            self.grid_env[r, c] = ElementsEnv.TREE.value


class TreeBoulders(Jungle):
    """
    Empty Jungle with half the empty cells with trees and boulders.
    No Exit.
    """

    def _set_exits(self):
        pass

    def _set_elements(self):

        quantity_elems = int( (self.size - 2)**2 / 4)

        for i in range(quantity_elems):
            r, c = self.get_random_empty_location()
            self.grid_env[r, c] = ElementsEnv.TREE.value

            r, c = self.get_random_empty_location()
            self.grid_env[r, c] = ElementsEnv.BOULDER.value



class Rivers(Jungle):
    """
    Empty Jungle with half the empty cells with trees and boulders.
    No Exit.
    """

    def _set_exits(self):
        pass

    def _set_elements(self):

        for i in range(10):
            r, c = self.get_random_empty_location()
            self.grid_env[r, c] = ElementsEnv.RIVER.value





