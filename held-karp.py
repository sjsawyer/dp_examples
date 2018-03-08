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

    def f(i, visited, path_so_far):
        '''
        Let f(i, unvisited, path_so_far) be the path of minimum distance from city i to
        city 0, that passes through all remaining unvisited cities in
        `visited`, where visited is a bitmask such that the bit in the jth
        position being 1 represents city j having been visited, and bit j
        being 0 represents city j having not been visited, and `path_so_far` is
        the current path of minimum distance from city 0 up to city i.

        Then the solution we want is f(0, 0, []), and the following recursive
        relation holds:

            f(i, visited) = min_{j in unvisited} ( d(i,j) + f(j, visited | (1<<j)) )

        NOTE: Must be careful not to mutate
        '''
        # Base case: check if all cities have been visited
        if visited == (1 << n) - 1:
            # we have visited all cities, return to 0
            return d[i][0], path_so_far + [0,]

        min_dist = sys.maxint
        # visit all unvisited cities
        for j in range(n):
            if not (1 << j) & visited:
                dist_from_j, path_with_j = \
                    f(j, visited | (1 << j), path_so_far + [j,])
                # Distance with j
                dist_with_j = d[i][j] + dist_from_j
                if dist_with_j < min_dist:
                    min_dist = dist_with_j
                    min_path = path_with_j

        return min_dist, min_path

    return f(0, 0, [])


def held_karp_dp(distance_matrix):
    '''
    Above algorithm, but making use of memoization to avoid recomputing
    overlapping subproblems
    '''
    d = distance_matrix
    n = len(d)

    '''
    We need a dp table that will store the minimum distances from city i
    to city 0 that passes through all unvisitied cities in the bit mask.
    There are n cities, and 2^n possible binary strings of length n, so our
    table will have dimensions n x 2^n
    '''
    dp = [[None for i in xrange(2**n)] for j in xrange(n)]

    def f(i, visited, path_so_far):
        '''
        f is defined as in the purely recursive implementation above.
        The only difference here is that we check if the value we are
        looking for is already in the defined dp table.

        To retrive the path, we also need to keep track of the parent node
        for any given i and remaining unvisited cities in the mask.
        '''
        # Check the table
        if dp[i][visited]:
            return dp[i][visited]
        # Base case: check if all cities have been visited
        if visited == (1 << n) - 1:
            # we have visited all cities, return to 0
            return d[i][0], path_so_far + [0,]

        min_dist = sys.maxint
        # visit all unvisited cities
        for j in range(n):
            if not (1 << j) & visited:
                dist_from_j, path_with_j = \
                    f(j, visited | (1 << j), path_so_far + [j,])
                # Distance with j
                dist_with_j = d[i][j] + dist_from_j
                if dist_with_j < min_dist:
                    min_dist = dist_with_j
                    min_path = path_with_j

        return min_dist, min_path

    return f(0, 0, [])



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
