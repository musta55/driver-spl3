def bubble_sort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

# Predefined input
numbers = [5, 2, 9, 1, 3]

print("Before sorting:", numbers)
bubble_sort(numbers)


print("After sorting:", numbers)
