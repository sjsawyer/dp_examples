import numpy as np

'''
Dynamic Time Warping

A dynamic programming approach to measuring the distance between two
temporal sequences. Ideal for sequences that may vary in speed or in phase.
'''


def distance(x, y):
    ''' Generic euclidean distance function '''
    return np.sqrt(np.sum((x - y)**2))


def dtw(a, b):
    '''
    Returns the DTW distance between sequences `a` and `b`.

    Parameters:
    -----------
    a : numpy array
    b : numpy array

    Returns:
    --------
    dist : float
    The distance between sequences `a` and `b`
    '''
    # Ensure inputs are np arrays
    a = np.asarray(a)
    b = np.asarray(b)

    # dtw_table[i,j] is the dtw distance up to and including a[i-1] and b[j-1]
    dtw_table = np.empty((a.size+1, b.size+1))
    # Initialize first row and column
    dtw_table[:, 0] = np.inf
    dtw_table[0, :] = np.inf
    dtw_table[0, 0] = 0.

    for i in xrange(1, a.size+1):
        for j in xrange(1, b.size+1):
            cost = distance(a[i-1], b[j-1])
            dtw_table[i, j] = cost + min(dtw_table[i-1, j],
                                         dtw_table[i, j-1],
                                         dtw_table[i-1, j-1])

    return dtw_table[a.size, b.size], dtw_table


def display_grid(grid):
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.imshow(grid, interpolation='None')
    for (j, i), label in np.ndenumerate(grid):
        ax.text(i, j, label, ha='center', va='center')
    plt.show()


def main():
    np.set_printoptions(suppress=True, precision=1)
    a = np.array([0, 5, 8, 9, 3, 0])
    b = np.array([5, 8, 9, 3])

    distance, table = dtw(a, b)
    print distance
    display_grid(table)


if __name__ == '__main__':
    main()
