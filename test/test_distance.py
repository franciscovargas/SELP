from numpy import arange, pi
import unittest
from app.map_graph import distance
import sqlite3


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.lat1 = arange(0, 2 * pi, 0.001 * pi) * 180 / pi
        self.long1 = arange(0, 2 * pi, 0.001 * pi) * 180 / pi
        self.lat2 = arange(0, 2 * pi, 0.001 * pi) * 180 / pi
        self.long2 = arange(0, 2 * pi, 0.001 * pi) * 180 / pi
        self.con = sqlite3.connect("app.db")

    def test_distance_does_not_raise_on_valid_input(self):
        """
        The following test inspects that the distance function
        does not break on valid inputs i.e. all possible angles
        """
        raised = False
        try:
            [distance(lat1, long1, lat2, long2)
             for lat1, long1, lat2, long2 in zip(self.lat1,
                                                 self.long1,
                                                 self.lat2,
                                                 self.long2)]
        except:
            raised = True
        self.assertFalse(raised, 'Exception raised')

    def test_distance_value(self):
        """
        The following test checks that all paths within
        an artificially created database (created by myself)
        have length less than 1km. I created such database
        using the path and only clickin and storing edges
        within the university campus area and the medows
        all constrained within 1km
        """
        self.con.create_function("distance", 4, distance)
        cur = self.con.cursor()
        cur.execute("""SELECT distance(lat_start,
                                       long_start,
                                       lat_end,
                                       long_end)
                        FROM edges""")
        results = cur.fetchall()
        # print results
        for dist in results:
            assert abs(dist[0]) <= 1


if __name__ == '__main__':
    unittest.main()
