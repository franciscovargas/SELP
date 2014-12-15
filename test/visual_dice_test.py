from random import uniform
import matplotlib.pyplot as plt
from app.map_graph import decision_at_node_N
r = uniform(0, 1.0)
weights = (20, 30, 100, 100, 20, 30, 10)
test = []
test2 = []
for j in range(100,10000,100):
	for i in range(j):
	    test += [decision_at_node_N(weights)]
	    # test2 += [decision_at_node(probabilities)]
	plt.figure()
	n, bins, patches = plt.hist(test, normed=True)
	plt.savefig('test%s.png'%j)