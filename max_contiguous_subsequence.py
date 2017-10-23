def max_contiguous_subsequence_topdown(A):
    '''
    A is the sequence of negative and positive integers

    Let M(j) = max sum over all slices ending at j
    Recurrence relation:
        M(j) = max( M(j-1) + A[j], A[j] )
    '''
    # initialize the values we've calcuted so far
    M = [None] * len(A)

    def _max_contiguous_subsequence_td(i):
        ''' Max contiguous subsequence up to index i '''
        if M[i] is not None:
            return M[i]
        if i == 0:
            M[i] = A[i]
            return M[i]
        else:
            M[i] = max(_max_contiguous_subsequence_td(i-1) + A[i], A[i])
            return M[i]

    # Calculate the values for M
    _max_contiguous_subsequence_td(len(A)-1)
    # Choose the max sum
    max_sum = max(M)
    max_idx = M.index(max_sum)
    max_seq = _sequence_from_sum(A, max_sum, max_idx)
    return max_seq


def max_contiguous_subsequence_bottomup(A):
    '''
    A is the sequence of negative and positive integers

    Let M(j) = max sum over all slices ending at j
    Recurrence relation:
        M(j) = max( M(j-1) + A[j], A[j] )
    '''
    M = [None] * len(A)
    for i in range(len(A)):
        if i == 0:
            M[i] = A[i]
        else:
            M[i] = max(M[i-1]+A[i], A[i])

    # the max sum
    max_sum = max(M)
    max_idx = M.index(max_sum)
    max_seq = _sequence_from_sum(A, max_sum, max_idx)
    return max_seq


def _sequence_from_sum(A, max_sum, j):
    '''
    Calculate the contiguous sequence with the maximum sum given the
    maximum sum, the original sequence and the index at which the
    maximal contiguous subsequence ends.
    '''
    seq = []
    sub_sum = max_sum
    sub_index = j
    while sub_sum > 0:
        seq.append(A[sub_index])
        sub_sum = sub_sum - A[sub_index]
        sub_index -= 1

    # Reverse the sequence to be in correct order
    return seq[::-1]


def quick_and_dirty(A):
    if len(A) < 2:
        return A
    maxsofar = A[0]
    maxendinghere = A[0]
    for i in range(1, len(A)):
        maxendinghere = max(maxendinghere + A[i], A[i])
        maxsofar = max(maxsofar, maxendinghere)
    return maxsofar



if __name__ == '__main__':

    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('sequence', nargs='+', type=int,
                   help="Sequence from which to find the contiguous "
                        "subsequence whose sum is maximal")
    p.add_argument('-s', '--strategy', nargs='?',
                   choices=['topdown', 'bottomup'], default='bottomup',
                   help="Algorithmic approach to use")
    args = p.parse_args()

    if args.strategy == 'topdown':
        maxseq = max_contiguous_subsequence_topdown(args.sequence)
    elif args.strategy == 'bottomup':
        maxseq = max_contiguous_subsequence_bottomup(args.sequence)
    print "Max sum: {}".format(sum(maxseq))
    print "Max seq: {}".format(maxseq)
