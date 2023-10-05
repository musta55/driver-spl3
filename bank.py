def fibonacci(n):
    # Create a list to store Fibonacci numbers
    fib = [0] * (n + 1)

    # Base cases
    fib[0] = 0
    fib[1] = 1

    # Calculate Fibonacci numbers using DP
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]

    return fib[n]

# Test the Fibonacci function
n = 10  # You can change this value to compute different Fibonacci numbers
result = fibonacci(n)
print(f"The {n}-th Fibonacci number is {result}.")
