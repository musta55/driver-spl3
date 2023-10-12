def longest_common_subsequence(X, Y):
    m, n = len(X), len(Y)
    
    # Create a table to store the length of LCS for subproblems
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill in the DP table using a bottom-up approach
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Reconstruct the LCS from the DP table
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs.append(X[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    lcs.reverse()
    return "".join(lcs)

# Test the longest_common_subsequence function
X = "AGGTAB"
Y = "GXTXAYB"
result = longest_common_subsequence(X, Y)
print(f"The Longest Common Subsequence is '{result}'.")
