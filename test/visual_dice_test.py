from random import uniform
import matplotlib.pyplot as plt
from app.map_graph import decision_at_node_N
"""
This is rather unsual for a test. But when it
comes to a probabilistic process it is quite
hard to claim that something will always fall
within a range.

This test generates histograms which ilustrate
the sample distribution after rolling the dice
n times. By inspection I can confirm that the
sample distribution is close to that of the
parent distribution (the weights normalized).
As the number of rolls increase the sample
distribution converges/tends more and more to
the parent distribution as one would expect
"""

#Normal like symmetric distribution of weights
weights = (20, 30, 100, 100, 30, 20)
#Uniform distribution of weights
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
