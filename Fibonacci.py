def fibonacci(n):
    f = [0, 1]
    for i in range(2, n+1):
        f.append(f[i-1] + f[i-2])
    return f[n]
# Calling the fibonacci function with n = 10
result = fibonacci(10)

# Printing the result
print(result)
