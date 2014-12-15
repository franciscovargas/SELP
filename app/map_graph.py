from random import uniform
import matplotlib.pyplot as plt
from math import fsum, acos, asin, cos, sin, pi


"""
QUERY1 DISECTION:
- The first clause ensures that the start of the edges
    are within 1KM range of the starting point.
- The second clause aims to gaurantee that the end of 
    the nodes queried is closer to the end point
- The third caluse checks that the start of the edges
    queried are closer to the end point than the current
    edge
"""

QUERY1 = """SELECT edges.lat_start,
                   edges.long_start,
                   edges.lat_end,
                   edges.long_end,
                   edges.rank,
                   edges.id
            FROM edges
            WHERE distance(?,?,edges.lat_start,edges.long_start)<= 1
            AND  distance(edges.lat_end, edges.long_end,?,?)<
            distance(?,?,?,?)
            AND distance(edges.lat_start, edges.long_start,?,?)<
            distance(?,?,?,?)
            ORDER BY edges.rank DESC
            LIMIT 6;
        """


def distance(lat1, lon1, lat2, lon2):
    """
    This method computes a distance via the law of cosines
    derivation may be found here (Calculation of Distance on 
    the Earth using Latitude and Longitude):
    1 . http://www.math.unl.edu/~shartke2/teaching/2011m896/SphericalLawOfCosines.pdf
    addapted to 2. using the fact that sin(pi - x) = cos(x) and cos(pi -x) = sin(x)
    2.http://www.movable-type.co.uk/scripts/latlong.html
    """
    coord = map(lambda x: float(x) * pi / 180.0, [lat1, lon1, lat2, lon2])
    inverse_arc = sin(coord[0]) * sin(coord[2]) + \
        cos(coord[0]) * cos(coord[2]) * cos(coord[1] - (coord[3]))
    arc_dist = acos(min(1, max(inverse_arc, -1))) * 6371
    return arc_dist


def decision_at_node_N(end_point_edge_weights):
    """
    This function looks at the nodes that are can be reached
    from your current state and roles a dice biased on the
    edge ranks to determine which node to progress to.
    The underlying mathematicsis quite simple and the dice can 
    have the sides of the input. Computes a cumulative_distribution
    and checks for a random number lying within ranges of the 
    distribution
    """
    norm = sum(end_point_edge_weights)
    p = [float(x) / float(norm) for x in end_point_edge_weights]
    cumulative_distribution = [fsum(p[:i + 1]) for i, x in enumerate(p)]
    r = uniform(0, 1.0)  # generates a pseudo random rumber \in [0,1]
    index = 0
    for i, cu in enumerate(cumulative_distribution[:-1]):
        if r > cu:
            index = i + 1
    return index


if __name__ == '__main__':
    """
    Structure for visual tests to be done for the dice.
    """
    r = uniform(0, 1.0)
    probabilities = (20, 30)
    test = []
    test2 = []
    for i in range(100000):
        test += [decision_at_node_N(probabilities)]
        # test2 += [decision_at_node(probabilities)]
    n, bins, patches = plt.hist(test, normed=True)
    # n2, bins2, patches2 = plt.hist(test2, normed=True)
    plt.show()
