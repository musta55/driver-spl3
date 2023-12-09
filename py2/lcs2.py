def longest_common_subsequence(x: str, y: str):

    m = len(x)
    n = len(y)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Fill in the dynamic programming table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                match = 1
            else:
                match = 0

            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1] + match)

    seq = ""
    i, j = m, n
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            match = 1
        else:
            match = 0

        if dp[i][j] == dp[i - 1][j - 1] + match:
            if match == 1:
                seq = x[i - 1] + seq
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], seq

if __name__ == "__main__":
    string1 = "AGGTABC"
    string2 = "GXTXAYBWC"
    expected_length = 5
    expected_subseq = "GTABC"

    length, subsequence = longest_common_subsequence(string1, string2)
    print("Length of LCS:", length)
    print("Longest Common Subsequence:", subsequence)
