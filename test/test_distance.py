from numpy import arange, pi
import unittest
from app.map_graph import distance

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.lat1 = arange(0,2*pi,0.001*pi)*180/pi
        self.long1 = arange(0,2*pi,0.001*pi)*180/pi
        self.lat2 = arange(0,2*pi,0.001*pi)*180/pi
        self.long2 = arange(0,2*pi,0.001*pi)*180/pi

    def test_distance_does_not_raise_on_valid_input(self):
        raised = False
        try:
            [distance(lat1, long1, lat2, long2) 
             for lat1, long1, lat2, long2 in zip(self.lat1,
                                                 self.long1,
                                                 self.lat2,
                                                 self.long2)]
        except:
            raised = True
            raise
        self.assertFalse(raised, 'Exception raised')



if __name__ == '__main__':
    unittest.main()