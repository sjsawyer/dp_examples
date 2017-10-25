'''
In the knapsack problem, you are given a list of N items, where each item
has a corresponding weight w_n and value v_n, and there is a knapsack that
has maximum weight capacity W. The goal is to fill the knapsack with a subset
of the n items so as to maximize the total value while remaining under the
weight W.

Let opt(n,w) be the optimal solution using all items up to n and max weight w.
Then it can be constructed by taking the max of two possibilities:

    opt(n,w) = max(opt(n-1, w), opt(n-1, w-w_n) + v_n)

'''


def knapsack_recursive(weights, values, W):
    '''
    Recursive approach
    weights is array of length n containing the weights
    values is array of length n containing corresponding values
    W is max weight capacity
    '''
    def opt(n, w):
        ''' optimal solution using items up to n and max weight capacity w '''
        if n == 0 or w == 0:
            return 0
        if w - weights[n-1] < 0:
            # cannot take item n, recurse on n-1
            return opt(n-1, w)
        else:
            # either (1) do not take item n, or (2) take it
            return max(opt(n-1, w), opt(n-1, w-weights[n-1]) + values[n-1])

    return opt(len(values), W)


def knapsack_topdown(weights, values, W):
    '''
    Topdown approach. Same as the recursive, except we save values that we
    have already calculated.
    '''
    # table to store the values
    # table[n][w] is the max value using items up to index n and weight
    # capacity w
    table = [[None for col in range(W+1)] for row in range(len(values)+1)]

    def opt(n, w):
        # note item n is index n-1 in weights[] and values[]
        if n == 0 or w == 0:
            table[n][w] = 0
            return table[n][w]
        elif w - weights[n-1] < 0:
            table[n][w] = opt(n-1, w)
            return table[n][w]
        else:
            table[n][w] = max(opt(n-1, w),
                              opt(n-1, w-weights[n-1]) + values[n-1])
            return table[n][w]

    return opt(len(values), W)


def knapsack_bottomup(weights, values, W):
    '''
    Bottom up approach. Here we start with the base case and store solutions
    for all possible subproblems up to the desired solution, building off
    of previously calculated solutions as necessary.
    '''
    # table to store the values
    # table[n][w] is the max value using items up to index n and weight
    # capacity w
    # (n+1) for n = 0 (no items) and w = 0 (max weight capacity 0)
    table = [[None for col in range(W+1)] for row in range(len(values)+1)]

    # fill in table with base case
    for row in range(len(values)+1):
        table[row][0] = 0
    for col in range(W+1):
        table[0][col] = 0

    for n in range(1, len(values)+1):
        for w in range(1, W+1):
            # weights[n-1] is weight of item n here
            if w-weights[n-1] < 0:
                table[n][w] = table[n-1][w]
            else:
                table[n][w] = max(table[n-1][w],
                                  table[n-1][w-weights[n-1]] + values[n-1])

    opt_val = table[len(values)][W]

    # For the bottom up approach we will work backwards using the optimal
    # value and the dp table to obtain the items chosen
    n_, w_ = len(values), W
    items = []
    while table[n_][w_]:
        if w_ - weights[n_-1] < 0:
            n_, w_ = n_-1, w_
        elif table[n_-1][w-weights[n_-1]] + values[n_-1] > table[n_-1][w_]:
            items.append(n_-1)
            n_, w_ = n_-1, w_-weights[n_-1]
        else:
            n_, w_ = n_-1, w_

    return opt_val, items


if __name__ == '__main__':
    values = [60, 100, 120]
    weights = [10, 20, 30]
    W = 50

    print knapsack_recursive(weights, values, W)
    print knapsack_topdown(weights, values, W)

    opt_val, items = knapsack_bottomup(weights, values, W)
    print "Max value: {}".format(opt_val)
    print "Values: {}".format([values[n] for n in items])
    print "Total weight: {}".format(sum(weights[n] for n in items))
