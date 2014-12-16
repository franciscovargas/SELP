from random import randint
import unittest
from app.map_graph import decision_at_node_N
import sqlite3


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.weights = [randint(0,101),
                        randint(0,101),
                        randint(0,101),
                        randint(0,101),
                        randint(0,101),
                        randint(0,101)]

    def test_dice_on_valid_input(self):
        """
        The following test inspects that the dice function
        does not break on valid inputs.
        """
        raised = False
        try:
            decision_at_node_N(self.weights)
        except:
            raised = True
        self.assertFalse(raised, 'Exception raised')


if __name__ == '__main__':
    unittest.main()
