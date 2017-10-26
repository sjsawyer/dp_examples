'''
Largest common substring

Return the largest common substring (or contiguous subsequence) of two
strings (list-like object)
    s1 = 1, 3, 8, 3, 6, 5
    s2 = 9, 6, 5, 0, 1, 8, 3, 6, 7
then the largest common subsequence would be 836.
'''


def largest_common_substring(s1, s2):
    n1, n2 = len(s1), len(s2)
    # table[i1][i2] is the longest common substring ending at i1-1 in s1 and
    # i2-1 in s2
    table = [[0 for i in range(n2+1)] for j in range(n1+1)]
    # store the lcs length and index at which it ends in s1 to retrive it later
    lcs_length, i1_opt = 0, -1
    # populate the table
    for i1 in range(1, n1+1):
        for i2 in range(1, n2+1):
            if s1[i1-1] == s2[i2-1]:
                table[i1][i2] = table[i1-1][i2-1] + 1
                # update result for the length of the lcs
                if table[i1][i2] > lcs_length:
                    lcs_length = table[i1][i2]
                    i1_opt = i1
            else:
                table[i1][i2] = 0

    lcs = s1[i1_opt - lcs_length:i1_opt]
    return lcs


if __name__ == '__main__':
    s1 = [2, 3, 8, 6, 2, 7, 6, 5]
    s2 = [1, 7, 9, 8, 3, 8, 6, 1, 5]
    print largest_common_substring(s1, s2)
    print largest_common_substring("chicken", "this hick is sick")
