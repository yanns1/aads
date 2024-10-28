from typing import Any


def merge_sort_rec(xs: list[Any]) -> list[Any]:
    """
    Sorts the *xs* using merge sort.

    Parameters
    ----------
    xs
        A list of orderable elements.
    """
    start = 0
    end = len(xs)
    if start >= end - 1:
        return xs

    # Splitting
    middle = (start + end) // 2
    l1 = merge_sort_rec(xs[start:middle])
    l2 = merge_sort_rec(xs[middle:end])

    # Merging
    i = 0
    i1 = 0
    i2 = 0
    n1 = len(l1)
    n2 = len(l2)
    while i1 < n1 and i2 < n2:
        if l1[i1] <= l2[i2]:
            xs[i] = l1[i1]
            i1 += 1
        else:
            xs[i] = l2[i2]
            i2 += 1
        i += 1

    while i1 < n1:
        xs[i] = l1[i1]
        i1 += 1
        i += 1
    while i2 < n2:
        xs[i] = l2[i2]
        i2 += 1
        i += 1

    return xs
