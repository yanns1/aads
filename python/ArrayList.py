from ctypes import Array, c_int
from random import randint
from timeit import timeit
from copy import deepcopy
from typing import Callable


def alloc(m: int) -> Array:
    IntArrayType = c_int * m  # création d'un type "tableau de m entiers"
    return IntArrayType()  # déclaration et initialisation à zéro du tableau


class ArrayList:
    def __init__(self, max_size: int, l: list[int] | str = "random") -> None:
        if l == "random":
            tab: Array = alloc(max_size)
            for i in range(max_size):
                tab[i] = randint(0, 999)

            self.__tab = tab
            self.__capacity = max_size
            self.__size = max_size
            self.__i_next = 0
        else:
            size = len(l)
            while size > max_size:
                max_size *= 2

            tab: Array = alloc(max_size)
            for i in range(size):
                tab[i] = l[i]

            self.__tab = tab
            self.__capacity = max_size
            self.__size = size
            self.__i_next = 0

    def __len__(self):
        return self.__size

    def __repr__(self) -> str:
        length = len(self)
        res = "(ArrayList) ["
        for i in range(length - 1):
            res += str(self.get(i)) + ", "
        res += str(self.get(length - 1)) + "]"
        return res

    # See this for how to make a class a generator, or more precisely, an iterator: https://stackoverflow.com/questions/42983569/how-to-write-a-generator-class
    def __next__(self) -> int:
        if self.__i_next < self.__size:
            val = self.get(self.__i_next)
            self.__i_next += 1
            return val
        else:
            # reset
            self.__i_next = 0
            raise StopIteration

    def __iter__(self):
        return self

    def is_equal_to(self, other: "ArrayList") -> bool:
        len1 = len(self)
        len2 = len(other)
        if len1 != len2:
            return False
        for i in range(len1):
            if self.get(i) != other.get(i):
                return False
        return True

    def is_empty(self) -> bool:
        return self.__size == 0

    def get(self, i: int) -> int:
        if i == -1:
            i = len(self) - 1
        if i < 0 or i >= self.__size:
            raise Exception("Tried to get element out of bounds of ArrayList.")
        return self.__tab[i]

    def set(self, i: int, item: int) -> "ArrayList":
        if i == -1:
            i = len(self) - 1
        if i < 0 or i >= self.__capacity:
            raise Exception("Tried to set element out of bounds of ArrayList.")
        self.__tab[i] = item
        return self

    def lookup(self, item: int) -> int | None:
        for i in range(len(self)):
            if self.get(i) == item:
                return i
        return None

    def remove(self, i: int) -> "ArrayList":
        if i == -1:
            i = self.__size - 1

        if i < 0 or i >= self.__size:
            raise Exception("Tried to set element out of bounds of ArrayList.")

        for j in range(i, self.__size - 1):
            self.set(j, self.get(j + 1))

        # on réduit la taille du tableau de 1
        self.__size -= 1

        return self

    def insert(self, i: int, item: int) -> "ArrayList":
        if i < -1:
            raise Exception(f"Try to insert at index {i}. It's impossible.")

        if i == -1:
            i = self.__size

        if i >= self.__capacity or self.__size >= self.__capacity:
            # débordement de capacité, on double la capacité du tableau (tableau dynamique, voir https://en.wikipedia.org/wiki/Dynamic_array pour d'autres variantes)

            if self.__capacity <= 0:
                self.__capacity = 1
            # Need to do it at least one time in case it's the condition self.__size >= self.__capacity that's true.
            self.__capacity *= 2
            while i >= self.__capacity:
                self.__capacity *= 2
            tab: Array = alloc(self.__capacity)
            for j in range(i):
                tab[j] = self.get(j)
            tab[i] = item
            for j in range(i, self.__size):
                tab[j + 1] = self.get(j)
            self.__tab = tab
        else:
            # pas de débordement de capacité...
            # décalage des éléments vers la droite à partir de l'index i
            for j in range(len(self), i, -1):
                self.set(j, self.get(j - 1))
            # on insert item à l'index i
            self.set(i, item)

        # on augmente la taille du tableau de 1
        self.__size += 1

        return self

    def prepend(self, item: int) -> "ArrayList":
        return self.insert(0, item)

    def append(self, item: int) -> "ArrayList":
        return self.insert(self.__size, item)

    def extend(self, tab: "ArrayList") -> "ArrayList":
        for i in range(len(tab)):
            self.append(tab.get(i))

        return self

    def is_sorted(self, order: Callable[[int, int], bool]) -> bool:
        for i in range(self.__size - 1):
            if not order(self.get(i), self.get(i + 1)):
                return False
        return True

    def __swap(self, i: int, j: int) -> "ArrayList":
        if j == -1:
            j = self.__size - 1
        if i != j:
            val = self.get(i)
            self.set(i, self.get(j))
            self.set(j, val)

        return self

    def __partition(self, i_start: int, i_end: int, pivot: int) -> int:
        self.__swap(pivot, i_end)
        i = i_start
        j = i_start

        for i in range(i_start, i_end):
            if self.get(i) <= self.get(i_end):
                self.__swap(i, j)
                j += 1

        self.__swap(j, i_end)
        return j

    def quicksort(self, i_start: int = 0, i_end: int | None = None) -> "ArrayList":
        # I would like the default for i_end to be self.__size-1, but there is no way to define a default value that depends on previous parameters. So as advised here: https://stackoverflow.com/questions/21804615/how-can-i-make-the-default-value-of-an-argument-depend-on-another-argument-in-p, I give it the default None, and catch it later...
        if i_end is None:
            i_end = self.__size - 1

        if i_start < i_end:  # si au moins deux cases dans le tableau
            pivot = randint(i_start, i_end)
            pivot = self.__partition(i_start, i_end, pivot)
            self.quicksort(i_start, pivot - 1)
            self.quicksort(pivot + 1, i_end)

        return self

    def selection_sort(self, i_start: int = 0, i_end: int | None = None) -> "ArrayList":
        if i_end is None:
            i_end = self.__size - 1

        j = i_start
        for j in range(i_start, i_end):
            i_min = j
            minimum = self.get(i_min)
            for i in range(j, i_end + 1):
                el = self.get(i)
                if el < minimum:
                    i_min = i
                    minimum = el
            self.__swap(j, i_min)

        return self

    def insertion_sort(self, i_start: int = 0, i_end: int | None = None) -> "ArrayList":
        if i_end is None:
            i_end = self.__size - 1

        for i in range(i_start + 1, i_end + 1):
            el = self.get(i)
            j = i - 1
            while j >= i_start and el < self.get(j):
                self.set(j + 1, self.get(j))
                j -= 1
            self.set(j + 1, el)

        return self

    def bubble_sort(self, i_start: int = 0, i_end: int | None = None) -> "ArrayList":
        if i_end is None:
            i_end = self.__size - 1

        j = i_end
        for j in range(i_end, 0, -1):
            for i in range(i_start, j):
                if self.get(i) > self.get(i + 1):
                    self.__swap(i, i + 1)

        return self

    def to_python_list(self) -> list[int]:
        res = []
        for i in range(0, self.__size):
            res.append(self.get(i))

        return res

    # ex 15
    def compare_sort_algorithms(self) -> None:
        copy1 = deepcopy(self)
        copy2 = deepcopy(self)
        copy3 = deepcopy(self)
        copy4 = deepcopy(self).to_python_list()
        sort_algorithms = [
            ("bubble sort", self.bubble_sort),
            ("quicksort", copy1.quicksort),
            ("selection sort", copy2.selection_sort),
            ("insertion sort", copy3.insertion_sort),
            ("python sort", copy4.sort),
        ]
        results: list[tuple[str, float]] = []

        for name, f in sort_algorithms:
            results.append(
                (
                    name,
                    timeit(lambda: f(), number=1, globals=globals()) * 1000,
                )
            )

        results.sort(key=lambda t: t[1])

        i = 1
        first_col_len = 12
        second_col_len = 20
        name_first_col = "Position"
        name_second_col = "Sort algorithm"
        name_third_col = "Execution time in ms"
        print(
            name_first_col
            + " " * (first_col_len - len(name_first_col))
            + name_second_col
            + " " * (second_col_len - len(name_second_col))
            + name_third_col
        )
        for algo, time in results:
            print(
                str(i)
                + " " * (first_col_len - len(str(i)))
                + algo
                + " " * (second_col_len - len(algo))
                + str(time)
            )
            i += 1


if __name__ == "__main__":

    print("ArrayList.__init__/ArrayList.__repr__", end="")
    arr = ArrayList(3, [1, 2, 3])
    expected = "(ArrayList) [1, 2, 3]"
    got = str(arr)
    assert got == expected, f"Expected {expected}, got {got}."
    arr = ArrayList(10)
    expected = 10
    got = len(arr)
    assert got == expected, f"Expected array length to be {expected}, but got {got}."
    print(": tests passed!")

    print("ArrayList.__len__", end="")
    arr = ArrayList(10, [1, 2, 3, 4, 5])
    expected = 5
    got = len(arr)
    assert got == expected, f"Expected array length to be {expected}, but got {got}."
    print(": tests passed!")

    print("ArrayList.is_equal_to", end="")
    arr1 = ArrayList(1, [])
    arr2 = ArrayList(10, [])
    assert arr1.is_equal_to(arr2), f"Expected {arr1} to be equal to {arr2}."
    arr1 = ArrayList(1, [1, 2, 3])
    arr2 = ArrayList(10, [1, 2, 3])
    assert arr1.is_equal_to(arr2), f"Expected {arr1} to be equal to {arr2}."
    arr1 = ArrayList(1, [1, 2, 3])
    arr2 = ArrayList(10, [2, 3, 4])
    assert not arr1.is_equal_to(arr2), f"Expected {arr1} to be equal to {arr2}."
    arr1 = ArrayList(1, [3, 2, 1])
    arr2 = ArrayList(10, [3, 2, 1])
    assert arr1.is_equal_to(arr2) == arr2.is_equal_to(
        arr1
    ), f"Expected ArrayList.is_equal_to to be commutative."
    arr1 = ArrayList(1, [3, 2, 1])
    arr2 = ArrayList(10, [4, 3, 2])
    assert arr1.is_equal_to(arr2) == arr2.is_equal_to(
        arr1
    ), f"Expected ArrayList.is_equal_to to be commutative."
    print(": tests passed!")

    print("ArrayList.is_empty", end="")
    arr = ArrayList(10, [])
    assert arr.is_empty(), "Expected array to be empty."
    arr = ArrayList(10, [1, 2, 3, 4, 5])
    assert not arr.is_empty(), "Expected array to not be empty."
    print(": tests passed!")

    print("ArrayList.get", end="")
    expected = 3
    arr = ArrayList(10, [1, 2, expected, 4, 5])
    got = arr.get(2)
    assert got == expected, f"Expected {expected}, but got {got}."
    expected = 5
    arr = ArrayList(10, [1, 2, 3, 4, expected])
    got = arr.get(-1)
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(10, [])
    got_exception = False
    try:
        arr.get(5)
    except Exception as e:
        got_exception = True
    assert (
        got_exception
    ), f"Expected exception to be raised because tried to get element out of bounds."
    print(": tests passed!")

    print("ArrayList.set", end="")
    arr = ArrayList(4, [1, 2, 3])
    arr.set(0, 10)
    expected = [10, 2, 3]
    assert arr.to_python_list() == expected, f"Expected {expected} but got {arr}."
    arr = ArrayList(4, [1, 2, 3])
    arr.set(2, 4)
    expected = [1, 2, 4]
    assert arr.to_python_list() == expected, f"Expected {expected} but got {arr}."
    arr = ArrayList(0, [])
    got_exception = False
    try:
        arr.set(5, 10)
    except Exception as e:
        got_exception = True
    assert (
        got_exception
    ), f"Expected exception to be raised because tried to set element out of bounds."
    print(": tests passed!")

    print("ArrayList.__iter__/ArrayList.__next__", end="")
    arr = ArrayList(5, [1, 2, 3, 4, 5])
    i: int = 1
    for el in arr:
        assert i == el, f"Expected element to be {i}, but got {el}."
        i += 1
    assert i == 6, f"Expected i to equal 6, but got {i}."
    print(": tests passed!")

    print("ArrayList.lookup", end="")
    arr = ArrayList(10, [0, 1, 2, 3, 4])
    got = arr.lookup(0)
    expected = 0
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(10, [0, 1, 2, 3, 4])
    got = arr.lookup(4)
    expected = 4
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(10, [0, 1, 2, 3, 4])
    got = arr.lookup(3)
    expected = 3
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(10, [0, 1, 2, 3, 4])
    got = arr.lookup(10)
    expected = None
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(10, [0, 1, 2, 3, 4])
    got = arr.lookup(-10)
    expected = None
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(10, [])
    got = arr.lookup(1)
    expected = None
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("ArrayList.insert", end="")
    arr = ArrayList(5, [])
    arr.insert(0, 0)
    arr.insert(1, 1)
    arr.insert(2, 2)
    expected = [0, 1, 2]
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(3, [0, 2, 4])
    arr.insert(1, 1)
    arr.insert(3, 3)
    expected = [0, 1, 2, 3, 4]
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(3, [1, 2, 3])
    arr.insert(0, 0)
    expected = [0, 1, 2, 3]
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(3, [1, 2, 3])
    arr.insert(-1, 4)
    expected = [1, 2, 3, 4]
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(0, [])
    got_exception = False
    try:
        arr.insert(-5, 10)
    except Exception as e:
        got_exception = True
    assert (
        got_exception
    ), f"Expected exception to be raised because tried to insert element at negative index."
    print(": tests passed!")

    print("ArrayList.remove", end="")
    arr = ArrayList(3, [1, 2, 3])
    arr.remove(0)
    expected = [2, 3]
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(3, [1, 2, 3])
    arr.remove(1)
    expected = [1, 3]
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(3, [1, 2, 3])
    arr.remove(2)
    expected = [1, 2]
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(0, [])
    got_exception = False
    try:
        arr.remove(5)
    except Exception as e:
        got_exception = True
    assert (
        got_exception
    ), f"Expected exception to be raised because tried to remove element at index out of bounds."
    print(": tests passed!")

    print("ArrayList.prepend", end="")
    arr = ArrayList(3, [1, 2, 3])
    arr.prepend(0)
    expected = [0, 1, 2, 3]
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(0, [])
    arr.prepend(0)
    expected = [0]
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("ArrayList.append", end="")
    arr = ArrayList(3, [1, 2, 3])
    arr.append(4)
    expected = [1, 2, 3, 4]
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    arr = ArrayList(0, [])
    arr.append(0)
    expected = [0]
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("ArrayList.extend", end="")
    arr1 = ArrayList(3, [1, 2, 3])
    arr2 = ArrayList(3, [4, 5, 6])
    arr1.extend(arr2)
    expected = [1, 2, 3, 4, 5, 6]
    got = arr1.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    expected = [4, 5, 6]
    got = arr2.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    arr1 = ArrayList(3, [])
    arr2 = ArrayList(3, [1, 2, 3])
    arr1.extend(arr2)
    expected = [1, 2, 3]
    got = arr1.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    got = arr2.to_python_list()
    assert got == expected, f"Expected {expected}, but got {got}."
    print(": tests passed!")

    print("ArrayList.to_python_list", end="")
    expected = []
    arr = ArrayList(5, expected)
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected} but got {got}."
    expected = [1, 2, 3, 4, 5]
    arr = ArrayList(5, expected)
    got = arr.to_python_list()
    assert got == expected, f"Expected {expected} but got {got}."
    print(": tests passed!")

    print("ArrayList.quicksort", end="")
    arr = ArrayList(100)
    arr.quicksort()
    assert arr.is_sorted(lambda x, y: x <= y), "Expected array to be sorted."
    print(": tests passed!")

    print("ArrayList.insertion_sort", end="")
    arr = ArrayList(100)
    arr.insertion_sort()
    assert arr.is_sorted(lambda x, y: x <= y), "Expected array to be sorted."
    print(": tests passed!")

    print("ArrayList.selection_sort", end="")
    arr = ArrayList(100)
    arr.selection_sort()
    assert arr.is_sorted(lambda x, y: x <= y), "Expected array to be sorted."
    print(": tests passed!")

    print("ArrayList.bubble_sort", end="")
    arr = ArrayList(100)
    arr.bubble_sort()
    assert arr.is_sorted(lambda x, y: x <= y), "Expected array to be sorted."
    print(": tests passed!")

    print("All tests passed!")

    n: int = 1_000
    print(f"\nComparison of time taken by sort algorithms (n = {n})")
    tab = ArrayList(n)
    tab.compare_sort_algorithms()
    # Le sort() de Python semble 100 fois plus rapide que mon quicksort!
    # Quelques recherches suggestent que l'algorithme derrière le sort de Python est un algo. inventé par Tim Peters (un contributeur majeur au développement de Python), qui s'appelle maintenant "timsort" (voir https://fr.wikipedia.org/wiki/Timsort, https://stackoverflow.com/questions/1517347/about-pythons-built-in-sort-method)

    pass
