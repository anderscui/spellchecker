def edit_dist(s1, s2, sub_op=2):
    m = len(s1)
    n = len(s2)

    # initialize
    dist = [[0 for j in range(n+1)] for i in range(m+1)]
    for i in range(m+1):
        dist[i][0] = i
    for j in range(n+1):
        dist[0][j] = j

    for i in range(1, m+1):
        for j in range(1, n+1):

            d1 = dist[i-1][j] + 1
            d2 = dist[i][j-1] + 1
            d3 = dist[i-1][j-1]
            if s1[i-1] != s2[j-1]:
                d3 += sub_op
            dist[i][j] = min(d1, d2, d3)

    return dist[m][n]