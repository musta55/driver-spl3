import inspect

def merge_sort(collection: list) -> list:
    """A pure Python implementation of merge sort algorithm
    :param collection: a mutable collection of comparable items
    :return: the same collection ordered by ascending
    Examples:
    >>> merge_sort([0, 5, 3, 2, 2])
    [0, 2, 2, 3, 5]
    >>> merge_sort([])
    []
    >>> merge_sort([-2, 5, 0, -45])
    [-45, -2, 0, 5]
    """
    def merge(left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    if len(collection) < 2:
        return collection

    mid = len(collection) // 2
    left_half = merge_sort(collection[:mid])
    right_half = merge_sort(collection[mid:])
    return merge(left_half, right_half)

user_input = "32,13,56,24,87,5,12,5".strip()
unsorted = [int(item) for item in user_input.split(",")]
print(merge_sort(unsorted))
