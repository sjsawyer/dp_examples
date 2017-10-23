'''
Given an amount `c`, we want to find the total number of ways to use
coins of denomination in `denominations` to make up `c`.

Ex: c = 5, denominations=[1, 2, 5]
    We can make 5 using
        1,1,1,1,1
        1, 1, 1, 2
        1, 2, 2
        5
    So the solution is 4.

Recurrence relation:
Let count(c, m) be the total number of ways to make change for amount `c`
using denominations of indices 0 to m

    count(c, m) = count(c - values[m], m) + count(c, m-1)

'''

def make_change_recursive(c, values):

    def _count(c, m):
        '''
        Total number of ways to make change `c` using denominations up to
        index `m` in `values`
        '''
        if c == 0:
            return 1
        elif c < 0:
            return 0
        elif m < 0:
            return 0
        else:
            return _count(c - values[m], m) + _count(c, m-1)

    num_solutions = _count(c, len(values)-1)

    # enumerate all solutions
    solutions = []

    def _generate_solutions(c, m, l):
        if c < 0 or m < 0:
            pass
        elif c == 0:
            solutions.append(l)
        else:
            l1 = l[:]  # copy
            l2 = l[:]  # copy
            l1.append(values[m])
            _generate_solutions(c-values[m], m, l1)
            _generate_solutions(c, m-1, l2)

    _generate_solutions(c, len(values)-1, [])

    return num_solutions, solutions


def make_change_topdown(c, values):

    # create table of dimensions (c+1) X len(values)
    count_table = [[None for col in values] for row in range(c+1)]

    def _count(c, m):
        if c < 0 or m < 0:
            return 0
        if c == 0:
            count_table[c][m] = 1
            return count_table[c][m]
        if count_table[c][m] is not None:
            return count_table[c][m]
        else:
            count_table[c][m] = _count(c - values[m], m) + _count(c, m-1)
            return count_table[c][m]

    num_solutions = _count(c, len(values)-1)

    # enumerate all solutions
    solutions = [[] for i in range(num_solutions)]

    def _generate_solutions(c, m, min_index, max_index):
        '''
        Populate the array `solutions` from index `min_index` to `max_index`
        with the different ways to make change `c` from denominatons in
        `values`up to index `m`, using `count_table`.
        '''
        if count_table[c][m] is None or m < 0:
            pass
        elif c-values[m] < 0:
            # No solution with m, so do not append m
            _generate_solutions(c, m-1, min_index, max_index)
        else:
            # To make change `c`, we either used m or we didnt
            num_ways_using_m = count_table[c-values[m]][m]
            num_ways_not_using_m = count_table[c][m-1]
            # Add m to the first num_ways_using_m lists and recurse on them
            for i in range(num_ways_using_m):
                solutions[min_index+i].append(values[m])
            _generate_solutions(c-values[m], m,
                                min_index,
                                min_index+num_ways_using_m-1)
            # Do not add m to the remaining lists and recurse on the rest
            if num_ways_not_using_m is not None:
                _generate_solutions(c, m-1,
                                    min_index+num_ways_using_m,
                                    max_index)

    # populate `solutions`
    _generate_solutions(c, len(values)-1, 0, len(values)-1)

    return num_solutions, solutions


def make_change_bottomup(c, values):
    '''
    For the bottom up approach, we start with the base case and build up
    our solution table without recursion.
    '''
    count_table = [[None for col in values] for row in range(c+1)]
    for amount in range(c+1):
        for m in range(len(values)):
            if count_table[amount][m] is not None:
                pass
            elif m == 0:
                # If values[0] divides the amount, we count 1
                count_table[amount][0] = int(amount % values[0] == 0)
            elif amount == 0:
                count_table[amount][m] = 1
            elif count_table[amount][m] is None:
                if amount - values[m] < 0:
                    count_table[amount][m] = count_table[amount][m-1]
                else:
                    count_table[amount][m] = count_table[amount - values[m]][m] + \
                                             count_table[amount][m-1]
    num_solutions = count_table[c][len(values)-1]

    '''
    Backtrack to get the solutions. count_table[c][m] is the number of ways
    to make `c` using values up to index `m`, and is a sum of the number of
    solutions using `m` (count_table[amount-values[m]][m]) and not using `m`
    (count_table[amount][m-1])
    '''
    solutions = [[] for i in range(num_solutions)]
    def _get_solutions(c, m, lo, hi):
        if m < 0 or c < 0:
            pass
        elif count_table[c][m] == 0:
            pass
        else:
            if c - values[m] < 0:
                num_using_m = 0
            else:
                num_using_m = count_table[c - values[m]][m]
            num_not_using_m = c - num_using_m
            if num_using_m:
                for i in range(num_using_m):
                    solutions[lo+i].append(values[m])
                _get_solutions(c - values[m], m, lo, lo+num_using_m-1)
            if num_not_using_m:
                _get_solutions(c, m-1, lo+num_using_m, hi)

    # Populate `solutions`
    _get_solutions(c, len(values)-1, 0, len(values)-1)

    return num_solutions, solutions


if __name__ == '__main__':

    import argparse
    import time
    p = argparse.ArgumentParser()
    p.add_argument('change', type=int,
                   help="The total amount of change to make.")
    p.add_argument('denominations', nargs='+', type=int,
                   help="Denominations of the coins to use")
    p.add_argument('-s', '--strategy', nargs='?',
                   choices=['topdown', 'bottomup', 'recursive'], default='bottomup',
                   help="Algorithmic approach to use")
    p.add_argument('-v', '--verbose', action='store_true',
                   help="Specify to include solutions in output")
    args = p.parse_args()

    if args.strategy == 'topdown':
        t0 = time.time()
        num_solutions, solutions = make_change_topdown(args.change, args.denominations)
        sol_time = time.time() - t0
    elif args.strategy == 'bottomup':
        t0 = time.time()
        num_solutions, solutions = make_change_bottomup(args.change, args.denominations)
        sol_time = time.time() - t0
    elif args.strategy == 'recursive':
        t0 = time.time()
        num_solutions, solutions = make_change_recursive(args.change, args.denominations)
        sol_time = time.time() - t0

    print "{:d} solutions in {:.6f} seconds".format(num_solutions, sol_time)
    if args.verbose:
        for solution in solutions:
            print solution
