import copy
import random

import numpy as np
from option import Option


class ArrayList[T]:
    def __init__(self, lst: list[T] = []):
        self._size: int = len(lst)
        self._capacity: int = 8
        while self._size >= self._capacity:
            self._capacity *= 2
        self._arr = np.empty(self._capacity, dtype=object)
        for i in range(self._size):
            self._arr[i] = lst[i]

        self._it_idx: int = 0

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        if self._size == 0:
            return "[]"

        s = "["
        for i in range(self._size - 1):
            s += str(self._arr[i]) + ", "
        s += str(self._arr[self._size - 1]) + "]"

        return s

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self._it_idx < self._size:
            val = self._arr[self._it_idx]
            self._it_idx += 1
            return val
        else:
            self._it_idx = 0
            raise StopIteration

    def __eq__(self, other) -> bool:
        if not isinstance(other, ArrayList):
            return False

        len1 = len(self)
        len2 = len(other)
        if len1 != len2:
            return False

        for i in range(len1):
            if self._arr[i] != other._arr[i]:
                return False

        return True

    def __bool__(self) -> bool:
        """
        Returns `True` if this list is non-empty, `False` otherwise.

        Returns
        -------
        `bool`
        """
        return not self.is_empty

    @property
    def is_empty(self) -> bool:
        """
        Whether this list is empty.
        """
        return self._size == 0

    def get_at_idx(self, i: int) -> Option[T]:
        """
        Returns the value at index *i* in this list.

        Note
        ----
        A value of -1 for *i* is accepted and refers to the last element of
        the list, as for Python lists.

        Parameters
        ----------
        i

        Return
        -------
        `Option[T]`
            The value at index *i*, or `Option.NONE` if *i* is out of bounds.
        """
        if i == -1:
            i = len(self) - 1
        if i < 0 or i >= self._size:
            return Option.NONE()
        return Option.Some(self._arr[i])

    def __getitem__(self, key) -> T:
        if not isinstance(key, int):
            raise TypeError("key should be int")

        res = self.get_at_idx(key)
        if res.is_none:
            raise IndexError()
        return res.unwrap()

    def get_by_val(self, v: T) -> Option[int]:
        """
        Returns the index of the first instance (left-to-right search) of
        *v* in the list.

        Parameters
        ----------
        v

        Returns
        -------
        `Option[int]`
            The index of *v* if found, `Option.NONE` otherwise.
        """
        for i in range(self._size):
            if self._arr[i] == v:
                return Option.Some(i)
        return Option.NONE()

    def set_at_idx(self, i: int, v: T) -> "ArrayList":
        """
        Sets value at index *i* to *v*.

        If *i* is out of bounds, nothing will be done and the
        function will exit *without* error.

        Note
        ----
        A value of -1 for *i* is accepted and refers to the last element of
        the list, as for Python lists.

        Parameters
        ----------
        i
        v

        Returns
        -------
        `ArrayList`
            This list (useful for chaining operations).
        """
        if i == -1:
            i = len(self) - 1
        if i < 0 or i >= self._size:
            return self
        self._arr[i] = v
        return self

    def __setitem__(self, key, value: T):
        if not isinstance(key, int):
            raise TypeError("key should be int")

        if key == -1:
            key = len(self) - 1
        if key < 0 or key >= self._size:
            raise IndexError()

        self.set_at_idx(key, value)

    def delete_at_idx(self, i: int) -> "ArrayList":
        """
        Deletes value at index *i*.

        If *i* is out of bounds, nothing will be done and the
        function will exit *without* error.

        Note
        ----
        A value of -1 for *i* is accepted and refers to the last element of
        the list, as for Python lists.

        Parameters
        ----------
        i

        Returns
        -------
        `ArrayList`
            This list (useful for chaining operations).
        """
        if i == -1:
            i = self._size - 1
        if i < 0 or i >= self._size:
            return self

        for j in range(i, self._size - 1):
            self._arr[j] = self._arr[j + 1]
        self._size -= 1

        return self

    def __delitem__(self, key):
        if not isinstance(key, int):
            raise TypeError("key should be int")

        if key == -1:
            key = self._size - 1
        if key < 0 or key >= self._size:
            raise IndexError()

        self.delete_at_idx(key)

    def insert_at_idx(self, i: int, v: T) -> "ArrayList":
        """
        Inserts value *v* at index *i*.

        If *i* is out of bounds, nothing will be done and the
        function will exit *without* error.

        Note
        ----
        A value of -1 for *i* is accepted and means insert in
        last position.

        Parameters
        ----------
        i
        v

        Returns
        -------
        `ArrayList`
            This list (useful for chaining operations).
        """
        if i == -1:
            i = self._size
        if i < 0 or i > self._size:
            return self

        should_realloc = False
        while self._size >= self._capacity:
            self._capacity *= 2
            should_realloc = True

        if should_realloc:
            new_arr = np.empty(self._capacity, dtype=object)
            for j in range(i):
                new_arr[j] = self._arr[j]
            new_arr[i] = v
            for j in range(i, self._size):
                new_arr[j + 1] = self._arr[j]
            self._arr = new_arr
        else:
            # offset elements starting from *i*
            for j in range(self._size, i, -1):
                self._arr[j] = self._arr[j - 1]
            # then insert *v* at *i*
            self._arr[i] = v

        self._size += 1
        return self

    def prepend(self, v: T) -> "ArrayList":
        """
        Prepends *v* to this list, i.e. inserts it at the *beginning* of this list.

        Parameters
        ----------
        v

        Returns
        -------
        `ArrayList`
            This list (useful for chaining operations).
        """
        return self.insert_at_idx(0, v)

    def append(self, v: T) -> "ArrayList":
        """
        Appends *v* to this list, i.e. inserts it at the *end* of this list.

        Parameters
        ----------
        v

        Returns
        -------
        `ArrayList`
            This list (useful for chaining operations).
        """
        return self.insert_at_idx(self._size, v)

    def extend(self, arr: "ArrayList") -> "ArrayList":
        """
        Extends this list with the elements in *arr*.

        This is equivalent to appending the elements of *arr* one-by-one,
        from left to right.

        Parameters
        ----------
        arr

        Returns
        -------
        `ArrayList`
            This list (useful for chaining operations).
        """
        for i in range(len(arr)):
            self.append(arr._arr[i])

        return self

    def __add__(self, other) -> "ArrayList":
        """
        Extends this list with the elements in *other*.

        This is equivalent to appending the elements of *other* one-by-one,
        from left to right.

        Parameters
        ----------
        arr

        Returns
        -------
        `ArrayList`
            This list (useful for chaining operations).
        """
        if not isinstance(other, ArrayList):
            raise TypeError("unsupported operand for operator +")
        return self.extend(other)

    def to_python_list(self) -> list[T]:
        """
        Converts this list to a Python list.

        Returns
        -------
        `list[T]`
        """
        py_lst = []
        for i in range(self._size):
            py_lst.append(self._arr[i])
        return py_lst

    def clone(self) -> "ArrayList":
        """
        Returns a clone (i.e. a deep copy) of this list.

        Returns
        -------
        `ArrayList`
        """
        return copy.deepcopy(self)

    def selection_sort(self, start: int = 0, end: int = -1):
        """
        Sorts the elements from index *start* to index *end* (included) using selection sort.

        Note
        ----
        A value of -1 for *end* is accepted and is equivalent to
        the length of this list minus one.

        Parameters
        ----------
        start
        end
        """
        if end == -1:
            end = self._size - 1

        j = start
        for j in range(start, end):
            i_min = j
            min = self._arr[i_min]
            for i in range(j, end + 1):
                el = self._arr[i]
                if el < min:
                    i_min = i
                    min = el

            tmp = self._arr[j]
            self._arr[j] = self._arr[i_min]
            self._arr[i_min] = tmp

    def _partition(self, start: int, end: int, pivot: int) -> int:
        # Place the pivot value at the end of the array.
        tmp = self._arr[pivot]
        self._arr[pivot] = self._arr[end]
        self._arr[end] = tmp

        i_pivot = start
        for i in range(start, end):
            if self._arr[i] <= self._arr[end]:
                tmp = self._arr[i]
                self._arr[i] = self._arr[i_pivot]
                self._arr[i_pivot] = tmp
                i_pivot += 1

        # Put the pivot value where it should be.
        tmp = self._arr[i_pivot]
        self._arr[i_pivot] = self._arr[end]
        self._arr[end] = tmp

        return i_pivot

    def _quicksort_rec(self, start: int, end: int):
        if start >= end:
            return

        pivot = random.randint(start, end)
        pivot = self._partition(start, end, pivot)
        self._quicksort_rec(start, pivot - 1)
        self._quicksort_rec(pivot + 1, end)

    def quicksort(self, start: int = 0, end: int = -1):
        """
        Sorts the elements from index *start* to index *end* (included) using quicksort.

        Note
        ----
        A value of -1 for *end* is accepted and is equivalent to
        the length of this list minus one.

        Parameters
        ----------
        start
        end
        """
        if end == -1:
            end = self._size - 1

        self._quicksort_rec(start, end)

    def insertion_sort(self, start: int = 0, end: int = -1):
        """
        Sorts the elements from index *start* to index *end* (included) using insertion sort.

        Note
        ----
        A value of -1 for *end* is accepted and is equivalent to
        the length of this list minus one.

        Parameters
        ----------
        start
        end
        """
        if end == -1:
            end = self._size - 1

        for i in range(start + 1, end + 1):
            el = self._arr[i]
            j = i - 1
            while j >= start and el < self._arr[j]:
                self._arr[j + 1] = self._arr[j]
                j -= 1
            self._arr[j + 1] = el

        return self

    def bubble_sort(self, start: int = 0, end: int = -1) -> "ArrayList":
        """
        Sorts the elements from index *start* to index *end* (included) using bubble sort.

        Note
        ----
        A value of -1 for *end* is accepted and is equivalent to
        the length of this list minus one.

        Parameters
        ----------
        start
        end
        """
        if end == -1:
            end = self._size - 1

        j = end
        for j in range(end, 0, -1):
            for i in range(start, j):
                if self._arr[i] > self._arr[i + 1]:
                    tmp = self._arr[i]
                    self._arr[i] = self._arr[i + 1]
                    self._arr[i + 1] = tmp

        return self
