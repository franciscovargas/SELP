from json import dumps, loads
from random import uniform
import matplotlib.pyplot as plt
from math import fsum, acos, asin, cos, sin, pi

#  (lat1, lat1, long1 ) provided from click in the interactive map
#  or entered text (this is being debated)
#  must provide  lat2, long 2 for the end point (lat2,lat2,lat2)
#  for final distance (lat1, lat1, long1,lat2,lat2,lon)
#  This is painful to understand based on knowledge from mathematics for
#  physics 2 must be tested rigourusly.


QUERY1 = """SELECT edges.lat_start,
                   edges.long_start,
                   edges.lat_end,
                   edges.long_end,
                   edges.rank
            FROM edges
            WHERE distance(?,?,edges.lat_start,edges.long_start)<= 1
            AND  distance(edges.lat_end, edges.long_end,?,?)<
            distance(?,?,?,?)
            AND distance(edges.lat_start, edges.long_start,?,?)<
            distance(?,?,?,?)
            ORDER BY edges.rank DESC
            LIMIT 6;
        """



def distance(lat1,lon1,lat2,lon2):
    """
    This method computes a distance via the law of cosines
    """
    print (lat1,lon1,lat2,lon2)
    coord= map(lambda x:float(x)*pi/180.0,[lat1,lon1,lat2,lon2])
    distance = acos(sin(coord[0]) * sin(coord[2]) + cos(coord[0]) * cos(coord[2]) *cos(coord[1] - (coord[3])))* 6371
    print distance
    return distance

def stringify(map_graph):
    """
    A function used to convert a map graph data structure
    in to a string
    """
    return dumps(map_graph)


def string_to_graph(str):
    """
    A function used to convert a string back in to a map graph
    data structure
    """
    return loads(str)


def decision_at_node(end_point_edge_weights):
    """
    This function looks at the nodes that are can be reached
    from your current state and roles a dice biased on the
    edge ranks to determine which node to progress to.
    """
    p = end_point_edge_weights
    cumulative_distribution = [p[0],
                               p[0] + p[1],
                               p[0] + p[1] + p[2],
                               p[0] + p[1] + p[2] + p[3],
                               p[0] + p[1] + p[2] + p[3] + p[4],
                               p[0] + p[1] + p[2] + p[3] + p[4] + p[5]]
    r = uniform(0, 1.0)  # generates a pseudo random rumber \in [0,1]
    if r > cumulative_distribution[4]:
        return 5
    elif r > cumulative_distribution[3]:
        return 4
    elif r > cumulative_distribution[2]:
        return 3
    elif r > cumulative_distribution[1]:
        return 2
    elif r > cumulative_distribution[0]:
        return 1
    else:
        return 0


def decision_at_node_N(end_point_edge_weights):
    """
    This function looks at the nodes that are can be reached
    from your current state and roles a dice biased on the
    edge ranks to determine which node to progress to.
    """
    norm = sum(end_point_edge_weights)
    p = [float(x)/float(norm) for x in end_point_edge_weights]
    cumulative_distribution = [fsum(p[:i + 1]) for i, x in enumerate(p)]
    r = uniform(0, 1.0)  # generates a pseudo random rumber \in [0,1]
    index = 0
    for i, cu in enumerate(cumulative_distribution[:-1]):
        if r > cu:
            index = i + 1
    return index


def find_all_reachable_nodes(lat, long, connection):
    """
    This function finds all nodes which are in a radius of
    1 km from the provided lat and long arguments
    """
    cur = connection.cursor()
    cur.execute(QUERY1, (lat, lat, long))
    return cur.fetchall()


if __name__ == '__main__':
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
