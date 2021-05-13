from jungle.jungle import Jungle
from jungle.utils import ElementsEnv


class EmptyJungle(Jungle):
    def _set_exits(self):
        pass

    def _set_elements(self):
        pass

class EasyJungle(Jungle):
    """
    Jungle with river  exit, easy exit and elements.
    """
    def _set_exits(self):

        self.add_object(ElementsEnv.EXIT_EASY, self._exits[0].coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self._exits[1].coordinates)
        self.add_object(ElementsEnv.RIVER, self._exits[1].surrounding_1)
        self.add_object(ElementsEnv.RIVER, self._exits[1].surrounding_2)


    def _set_elements(self):

        quantity_trees = 8
        quantity_other_elements = 3

        for i in range(quantity_trees):

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.TREE, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.BOULDER, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.OBSTACLE, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.RIVER, (r, c))

        for i in range(quantity_other_elements):
            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.RIVER, (r, c))

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.OBSTACLE, (r, c))
class RiverOnlyJungle(Jungle):
    """
    Jungle with river  exit, easy exit and elements.
    """
    def _set_exits(self):

        self.add_object(ElementsEnv.EXIT_EASY, self._exits[0].coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self._exits[1].coordinates)
        self.add_object(ElementsEnv.RIVER, self._exits[1].surrounding_1)
        self.add_object(ElementsEnv.RIVER, self._exits[1].surrounding_2)


    def _set_elements(self):

        quantity_trees = 8
        quantity_other_elements = 3

        for i in range(quantity_trees):

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.TREE, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.BOULDER, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.OBSTACLE, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.RIVER, (r, c))

        for i in range(quantity_other_elements):
            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.RIVER, (r, c))

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.OBSTACLE, (r, c))

class DifficultJungle(Jungle):
    """
    Jungle with river  exit, black exit and elements.
    """
    def _set_exits(self):

        self.add_object(ElementsEnv.EXIT_EASY, self._exits[0].coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self._exits[1].coordinates)
        self.add_object(ElementsEnv.RIVER, self._exits[1].surrounding_1)
        self.add_object(ElementsEnv.RIVER, self._exits[1].surrounding_2)
        self.add_object(ElementsEnv.EXIT_BLACK, self._exits[2].coordinates)
        self.add_object(ElementsEnv.BOULDER, self._exits[2].surrounding_1)
        self.add_object(ElementsEnv.BOULDER, self._exits[2].surrounding_2)


    def _set_elements(self):

        quantity_trees = 9
        quantity_other_elements = 4

        for i in range(quantity_trees):

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.TREE, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.BOULDER, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.OBSTACLE, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.RIVER, (r, c))

        for i in range(quantity_other_elements):
            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.RIVER, (r, c))

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.OBSTACLE, (r, c))

class WhiteJungle(Jungle):
    """
    Jungle with river  exit, easy exit and elements.
    """
    def _set_exits(self):

        self.add_object(ElementsEnv.EXIT_EASY, self._exits[0].coordinates)
        self.add_object(ElementsEnv.EXIT_WHITE, self._exits[1].coordinates)
        self.add_object(ElementsEnv.BOULDER, self._exits[1].surrounding_1)
        self.add_object(ElementsEnv.BOULDER, self._exits[1].surrounding_2)


    def _set_elements(self):

        quantity_trees = 9
        quantity_other_elements = 4

        for i in range(quantity_trees):

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.TREE, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.BOULDER, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.OBSTACLE, (r, c))

            #r, c = self.get_random_empty_location()
            #self.add_object(ElementsEnv.RIVER, (r, c))

        for i in range(quantity_other_elements):
            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.RIVER, (r, c))

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.OBSTACLE, (r, c))




class FullJungle(Jungle):
    """
    Jungle with all possible exits and elements.
    """
    def _set_exits(self):

        self.add_object(ElementsEnv.EXIT_BLACK, self._exits[0].coordinates)
        self.add_object(ElementsEnv.EXIT_WHITE, self._exits[1].coordinates)
        self.add_object(ElementsEnv.EXIT_EASY, self._exits[2].coordinates)
        self.add_object(ElementsEnv.EXIT_DIFFICULT, self._exits[3].coordinates)

    def _set_elements(self):

        quantity_each_elem = 4

        for i in range(quantity_each_elem):

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.TREE, (r, c))

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.BOULDER, (r, c))

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.OBSTACLE, (r, c))

            r, c = self.get_random_empty_location()
            self.add_object(ElementsEnv.RIVER, (r, c))


class TreeEmptyJungle(Jungle):
    """
    Empty Jungle with half the empty cells with trees.
    No Exit.
    """
    def _set_exits(self):
        pass

    def _set_elements(self):

        quantity_trees = int((self.size - 2)**2 / 2)

        for i in range(quantity_trees):

            r, c = self.get_random_empty_location()
            self.grid_env[r, c] = ElementsEnv.TREE.value


class EasyExitJungle(Jungle):
    """
    Empty Jungle with half the empty cells with trees.
    No Exit.
    """
    def _set_exits(self):
        pass

    def _set_elements(self):

        quantity_trees = int((self.size - 2)**2 / 2)

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

        quantity_elems = int((self.size - 2)**2 / 4)

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
