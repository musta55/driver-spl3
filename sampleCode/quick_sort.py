import inspect
def quick_sort(collection: list) -> list:
    if len(collection) < 2:
        return collection
    pivot = collection.pop()  # Use the last element as the first pivot
    greater = []  # All elements greater than pivot
    lesser = []  # All elements less than or equal to pivot
    for element in collection:
        (greater if element > pivot else lesser).append(element)
    return quick_sort(lesser) + [pivot] + quick_sort(greater)



user_input = "32,13,56,24,87,5,12,5".strip()
unsorted = [int(item) for item in user_input.split(",")]
print(quick_sort(unsorted))

# source: https://github.com/TheAlgorithms/Python
