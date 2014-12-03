from json import dumps, loads
from random import uniform
import matplotlib.pyplot as plt

#  (lat1, lat1, long1 ) provided from click in the interactive map whilst
# lofed in
QUERY1 = """SELECT edges.lat_start,
                   edges.long_start,
                   edges.lat_end,
                   edges.long_end
            FROM edges
            WHERE acos(sin(?) * sin(edges.lat_start)
            + cos(?) * cos(Lat) * cos(Lon - (?))) * 6371 <= 1
            ORDER BY edges.rank DESC
            LIMIT 6;
        """


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

if __name__ == '__main__':
    r = uniform(0, 1.0)
    probabilities = (0.1, 0.2, 0.4, 0.05, 0.05, 0.2)
    test = []
    for i in range(1000000):
        test += [decision_at_node(probabilities)]
    n, bins, patches = plt.hist(test, normed=True)
    plt.show()
