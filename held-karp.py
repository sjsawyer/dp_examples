'''
held-karp.py
Implementation of the Bellman-Held-Karp Algorithm to exactly solve TSPs.
'''
import sys


def held_karp(distance_matrix):
    '''
    Solution to TSP using the Bellman-Held-Karp Algorithm

    Given the adjacency matrix to a corresponding tsp problem, find the
    minimum cost Hamiltonian cycle through the graph, as well as the
    corresponding path
    '''
    d = distance_matrix
    n = len(d)

    def f(i, visited):
        '''
        Let f(i, unvisited) be the path of minimum distance from node i to node 0,
        that passes through all remaining unvisited cities in `visited`, where
        visited is a bitmask such that the bit in the jth position being 1 represents
        city j having been visited, and bit j being 0 represents city j having not
        been visited.
        Then the solution we want is f(0, 0), and the following recursive relation holds:
        f(i, visited) = min_{j in unvisited} ( d(i,j) + f(j, visited | (1<<j)) )
        '''
        # copy the path
        if visited == (1 << n) - 1:
            # we have visited all cities, return to 0
            return d[i][0]
        # visit all unvisited cities
        unvisited = filter(lambda j: not (1 << j) & visited, range(n))
        return min(d[i][j] + f(j, visited | (1 << j)) for j in unvisited)

    return f(0, 0)


class Vertex:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


def distance(v1, v2):
    ''' distance between two `Vertex` instances '''
    return ((v1.x - v2.x)**2 + (v1.y - v2.y)**2)**0.5


def main():
    vs = [Vertex(0, 0),
          Vertex(4, 4),
          Vertex(4, 0),
          Vertex(0, 4)]
    d = [[None for v in vs] for v in vs]
    for i in range(len(d)):
        for j in range(len(d[i])):
            d[i][j] = distance(vs[i], vs[j])


    print held_karp(d)



if __name__ == '__main__':
    main()
