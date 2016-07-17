"""
Ways to use map and reduce to compute distance between points in an iterable
"""

# Simple illustration: distance along a number line
s = [(1, 0), (3, 0), (5,0)]  # This is a map of (pt, 0)
def dist_reduce(x, y):
    print "x is %s; y is %s" % (str(x), str(y))
	return (y[0],  y[0]-x[0]+x[1])
print reduce(dist_reduce, s)

# More complex illustration: cartesian distance
# Can replace distance with great circle, vincenty, total_seconds(), or any other coord system
from math import sqrt, pow

def dist(p1, p2):
	return sqrt( pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2) )

def dist_by_reduce(x, y):
	#print "x is %s; y is %s" % (str(x), str(y))
	#print "x[1] is %s" % str(x[1])
	return (y[0], x[1] + dist(x[0], y[0]) )

points = [(1, 1), (1, 2), (2, 3), (4, 4)]
print points
m = map(lambda x: (x, 0.0), points)
r = reduce(dist_by_reduce, m)
print "Distance by Reduce: %f" % r[1]
