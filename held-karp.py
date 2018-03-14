'''
held-karp.py
Implementation of the Bellman-Held-Karp Algorithm to exactly solve TSPs,
requiring no external dependencies.
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
        Let f(i, visited, path_so_far) be the path of minimum distance from city i to
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
        for j in xrange(n):
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

    With this approach, we use another table called 'child' that keeps track
    of the child city of i for each combination of (i, visited), and we can
    use this table to backtrack through our solution to obtain the actual
    hamiltonian cycle of minimum distance.
    '''
    dp = [[None for i in xrange(2**n)] for j in xrange(n)]
    child = [[None for i in xrange(2**n)] for j in xrange(n)]

    def f(i, visited):
        '''
        f is defined as in the purely recursive implementation above.
        The only difference here is that we check if the value we are
        looking for is already in the defined dp table, and we do not
        keep track of the path as we go along, as looking up a solution
        for any given value would require having stored the path for
        that solution as well, which would be expensive.

        As such, we use the `child` table to keep track of where we
        came from.
        '''
        # Check the table
        if dp[i][visited]:
            return dp[i][visited]
        # Base case: check if all cities have been visited
        if visited == (1 << n) - 1:
            # we have visited all cities, return to 0
            dp[i][visited] = d[i][0]
            child[i][visited] = 0
            return d[i][0]

        min_dist = sys.maxint
        chosen_j = None
        # visit all unvisited cities
        for j in xrange(n):
            if not (1 << j) & visited:
                dist_with_j = d[i][j] + f(j, (1 << j) | visited)
                if dist_with_j < min_dist:
                    min_dist = dist_with_j
                    chosen_j = j

        dp[i][visited] = min_dist
        child[i][visited] = chosen_j
        return min_dist

    # The value we are interested in
    ans = f(0,1)

    # Can optain the optimal path using the parent matrix
    path = [0]
    i, visited = 0, 1
    next_ = child[i][visited]
    while next_ is not None:
        path.append(next_)
        visited |= (1 << next_)
        next_ = child[next_][visited]

    # Can also optain the optimal path working backwards using
    # the table and the knowledge of the cost of the optimal path
    path = [0]
    i, visited = 0, 1
    cost_from_i = dp[i][visited]
    while visited != (1 << n)-1:
        for j in range(n):
            if not visited & (1 << j):
                cost_from_j = dp[j][visited | (1 << j)]
                # require a tolerance for real valued distances
                if abs((cost_from_i - cost_from_j) - d[i][j]) < 0.001:
                    # j was the city selected in the opt solution
                    path.append(j)
                    i, visited = j, visited | (1 << j)
                    cost_from_i = cost_from_j 
                    break
    path.append(0)

    return ans, path


def held_karp_dp_bottomup(distance_matrix):
    '''
    In the bottom up implementation, we compute all possible solutions for the
    values `i` and `visited` as in the implementations above, and then
    simply look up the value for f(0,0).
    With this approach, we use another table called 'child' that keeps track
    of the child city of i for each combination of (i, visited), and we can
    use this table to backtrack through our solution to obtain the actual
    hamiltonian cycle of minimum distance.
    '''
    pass


class Vertex:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)


def distance(v1, v2):
    ''' distance between two `Vertex` instances '''
    return ((v1.x - v2.x)**2 + (v1.y - v2.y)**2)**0.5


def adj_matrix(graph):
    d = [[None for v in graph] for v in graph]
    for i in xrange(len(d)):
        for j in xrange(len(d[i])):
            d[i][j] = distance(graph[i], graph[j])
    return d


def main():
    # g1: (16.0, [0, 2, 1, 3, 0])
    # g2: (15.773387165490545, [0, 3, 1, 2, 4, 0])
    #g1 = [Vertex(0, 0), Vertex(4, 4), Vertex(4, 0), Vertex(0, 4)]
    g2 = [Vertex(0, 0), Vertex(4, 4), Vertex(0, 3), Vertex(4, 0), Vertex(1, 2)]
    #sol1= held_karp(adj_matrix(g1))
    #sol2= held_karp(adj_matrix(g2))
    #sol1 = held_karp_dp(adj_matrix(g1))
    sol2 = held_karp_dp(adj_matrix(g2))

    #print sol1
    print sol2

    #assert(sol1[0]==16.0)
    assert(abs(sol2[0]-15.7733871)<0.001)



if __name__ == '__main__':
    main()
