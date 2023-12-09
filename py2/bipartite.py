def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# Test input
sorted_list = [2, 4, 7, 10, 13, 18, 23, 29, 35, 50]
target_value = 18

# Perform binary search and print the result
result_index = binary_search(sorted_list, target_value)
if result_index != -1:
    print(f"Target {target_value} found at index {result_index}.")
else:
    print(f"Target {target_value} not found in the list.")
