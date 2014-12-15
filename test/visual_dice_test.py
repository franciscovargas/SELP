from random import uniform
import matplotlib.pyplot as plt
from app.map_graph import decision_at_node_N


weights = (20, 30, 100, 100, 30, 20)
weights2 = (20, 20, 20, 20, 20, 20)
test = []
test2 = []


for j in range(100, 10000, 1000):
    for i in range(j):
        test += [decision_at_node_N(weights)]
    plt.figure()
    n, bins, patches = plt.hist(test, normed=True)
    plt.savefig('test_normal%s.png' % j)


for j in range(100, 10000, 1000):
    for i in range(j):
        test2 += [decision_at_node_N(weights2)]
    plt.figure()
    n, bins, patches = plt.hist(test2, normed=True)
    plt.savefig('test_uniform%s.png' % j)
