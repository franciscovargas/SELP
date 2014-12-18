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


    def test_dice_ouput(self):
        """
        The following test inspects that the dice function
        outputs values in the range [0,5] for a 6 choice run
        """
        for i in range(0,100):
            weights2 = [randint(0,101) for i in range(0,6)]
	    self.assertTrue(decision_at_node_N(weights2) <= 5)
            self.assertTrue(decision_at_node_N(weights2) >= 0)


if __name__ == '__main__':
    unittest.main()
