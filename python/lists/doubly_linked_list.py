import copy
from typing import Iterator

from option import Option


class DLLNode[T]:
    """
    A node of `DoublyLinkedList[T]`.

    Parameters
    ----------
    v
        The value of the node.
    """

    def __init__(self, v: T):
        self._v: T = v
        self._prv: DLLNode[T] | None = None
        self._nxt: DLLNode[T] | None = None

    @property
    def v(self) -> T:
        return self._v

    @property
    def prv(self) -> "DLLNode[T] | None":
        return self._prv

    @property
    def nxt(self) -> "DLLNode[T] | None":
        return self._nxt

    def __repr__(self) -> str:
        """
        Printable representation of `DLLNode`, used for debugging.

        Returns
        -------
        `str`
        """
        prv_str = str(self._prv._v) if self._prv is not None else "None"
        nxt_str = str(self._nxt._v) if self._nxt is not None else "None"
        return f"{{prv:{prv_str}, val:{self._v}, nxt:{nxt_str}}}"


class DLLIterator[T](Iterator):
    """
    An iterator over `DoublyLinkedList[T]`.

    Note
    ----
    Time complexity (in all cases) of iteration is `O(n)` where `n` is the length of the list.
    """

    def __init__(self, start_node: DLLNode[T] | None):
        self._cur_node = start_node  # current node

    def __next__(self) -> T:
        if self._cur_node is None:
            raise StopIteration

        v = self._cur_node._v
        self._cur_node = self._cur_node._nxt
        return v


class DoublyLinkedList[T]:
    """
    A non-circular doubly-linked list.
    """

    def __init__(self, lst: list[T] = []):
        self._hd: DLLNode | None = None
        self._tl: DLLNode | None = None
        self._size: int = 0

        for el in lst:
            self.append(el)

    def __repr__(self) -> str:
        """
        Printable representation of `DoublyLinkedList`, used for debugging.

        Complexity
        ----------
        Time complexity (in all cases) is `O(n)` where `n` is the length of the list.

        Returns
        -------
        `str`
        """
        s = "["

        i = 0
        node = self._hd
        while i < self._size:
            assert node is not None

            if node._prv is not None:
                s += "< "
            s += f"{node._v}"
            if node._nxt is not None:
                s += " >"

            node = node._nxt
            i += 1

        s += "]"

        return s

    def __len__(self) -> int:
        """
        Returns the length of the list, i.e. its number of elements.

        Complexity
        ----------
        Time complexity (in all cases) is `O(1)` (constant).

        Returns
        -------
        `int`
        """
        return self._size

    def __iter__(self) -> DLLIterator:
        return DLLIterator(self._hd)

    @property
    def is_empty(self) -> bool:
        """
        Returns whether the list is empty (has no elements) or not.

        Complexity
        ----------
        Time complexity (in all cases) is `O(1)` (constant).

        Returns
        -------
        `bool`
            `True` if the list is empty, `False` otherwise.
        """
        return self._size == 0

    def __bool__(self) -> bool:
        """
        Returns `True` if this list is non-empty, `False` otherwise.

        Returns
        -------
        `bool`
        """
        return not self.is_empty

    def __eq__(self, other) -> bool:
        if not isinstance(other, DoublyLinkedList):
            return False

        len1 = len(self)
        len2 = len(other)
        if len1 != len2:
            return False

        for el1, el2 in zip(self, other):
            if el1 != el2:
                return False

        return True

    def get(self, node: DLLNode[T]) -> T:
        """
        Returns the value of *node*.

        Parameters
        ----------
        node

        Returns
        -------
        `T`
        """
        return node._v

    def get_at_idx(self, i: int) -> Option[DLLNode[T]]:
        """
        Returns the node at index *i*.

        Note
        ----
        A value of -1 for *i* is accepted and refers to the last element of
        the list, as for Python lists.

        Complexity
        ----------
        Best-case time complexity is `O(1)` (accessing the head or the tail).
        Worst-case time complexity is `O(n/2)`, which amounts to linear (accessing the middle element).

        Parameters
        ----------
        i
            The index (0-based) of the node to get.

        Returns
        -------
        `Option[DLLNode[T]]`
            The node at index *idx* if it exists, `None` otherwise
            (if list is empty or *idx* is out of bounds).
        """
        if i == -1:
            i = self._size - 1
        if i < 0 or i >= self._size:
            return Option.NONE()

        if i == 0:
            return Option.Some(self._hd)
        if i == self._size - 1:
            return Option.Some(self._tl)

        if i <= (self._size - 1) // 2:
            # ... then the element we search is in the first half of the list,
            #  so start from the head.
            j = 1
            node = self._hd._nxt  # type: ignore
            while j < i:
                assert node is not None
                j += 1
                node = node._nxt
        else:
            # ... then the element we search is in the second half of the list,
            #  so start from the tail.
            j = self._size - 2
            node = self._tl._prv  # type: ignore
            while j > i:
                assert node is not None
                j -= 1
                node = node._prv

        return Option.Some(node)

    def get_by_val(self, v: T) -> Option[DLLNode[T]]:
        """
        Returns the first node with value *v* if found.

        Complexity
        ----------
        Best-case time complexity is `O(1)` (element with value *val* is the head).
        Worst-case time complexity is `O(n)` (element with value *val* is the tail, or not found).

        Parameters
        ----------
        v
            The value of the node to get.

        Returns
        -------
        `Option[DLLNode[T]]`
        """
        if self._size == 0:
            return Option.NONE()
        assert self._hd is not None

        node = self._hd
        while node is not None and node._v != v:
            node = node._nxt

        if node is None:
            return Option.NONE()
        return Option.Some(node)

    def __getitem__(self, key) -> T:
        if not isinstance(key, int):
            raise TypeError("key should be int")

        res = self.get_at_idx(key)
        if res.is_none:
            raise IndexError()
        return res.unwrap()._v

    def set(self, node: DLLNode[T], v: T):
        """
        Sets the value of *node* to *v*.

        Parameters
        ----------
        node
        v
        """
        node._v = v

    def set_at_idx(self, i: int, v: T) -> Option[DLLNode[T]]:
        """
        Sets the value of node at index *i* to *v*.

        Parameters
        ----------
        i
        v

        Returns
        -------
        `Option[DLLNode[T]]`
            The node at index *i*, or `Option.NONE()` if *i* out of bounds.
        """
        node = self.get_at_idx(i)
        if node.is_none:
            return Option.NONE()

        node = node.unwrap()
        node._v = v
        return Option.Some(node)

    def set_by_val(self, v: T, new_v: T) -> Option[DLLNode[T]]:
        """
        Sets the value of first encountered node with value *v* to *new_v*.

        Parameters
        ----------
        v
        new_v

        Returns
        -------
        `Option[DLLNode[T]]`
            The first encountered node with value *v*, or `Option.NONE()` if not found.
        """
        node = self.get_by_val(v)
        if node.is_none:
            return Option.NONE()

        node = node.unwrap()
        node._v = new_v
        return Option.Some(node)

    def __setitem__(self, key, value: T):
        if not isinstance(key, int):
            raise TypeError("key should be int")

        if key == -1:
            key = len(self) - 1
        if key < 0 or key >= self._size:
            raise IndexError()

        self.set_at_idx(key, value)

    def insert(self, v: T, neighbor: DLLNode, after: bool = True) -> DLLNode[T]:
        """
        Inserts an element before or *after* the node *neighbor*.

        Complexity
        ----------
        Time complexity (in all cases) is `O(1)`.

        Parameters
        ----------
        val
            The element to insert.
        neighbor
            The neighbor of the node to create.
        after
            Whether to insert the new node after *neighbor* or before.

        Returns
        -------
        `DLLNode[T]`
            The newly created node.
        """
        new_node = DLLNode(v)

        if after:
            new_node._prv = neighbor
            if neighbor._nxt is not None:
                new_node._nxt = neighbor._nxt
                neighbor._nxt._prv = new_node
            neighbor._nxt = new_node

            if neighbor == self._tl:
                self._tl = new_node
        else:
            new_node._nxt = neighbor
            if neighbor._prv is not None:
                new_node._prv = neighbor._prv
                neighbor._prv._nxt = new_node
            neighbor._prv = new_node

            if neighbor == self._hd:
                self._hd = new_node

        self._size += 1
        return new_node

    def insert_at_idx(self, i: int, v: T) -> Option[DLLNode[T]]:
        """
        Inserts an element at index (0-based) *i*.

        Note
        ----
        A value of -1 for *i* is accepted and refers to the last element of
        the list, as for Python lists.

        Complexity
        ----------
        Best-case time complexity is `O(1)` (inserting at the beginning or the end).
        Worst-case time complexity is `O(n/2)`, which amounts to linear (inserting in the middle).

        Parameters
        ----------
        i
        v

        Returns
        -------
        `Option[DLLNode[T]]`
            The inserted node or `Option.NONE()` if *i* is out of bounds.
        """
        if i == -1:
            i = self._size
        if i < 0 or i > self._size:
            return Option.NONE()

        # Instantiate new node.
        new_node = DLLNode(v)

        # Handle case where list is empty.
        if self._size == 0:
            self._hd = new_node
            self._tl = new_node
            self._size += 1
            return Option.Some(new_node)

        # Handle case when inserting at the beginning of the list (aka. prepend).
        if i == 0:
            self._hd._prv = new_node  # type: ignore
            new_node._nxt = self._hd
            self._hd = new_node
            self._size += 1
            return Option.Some(new_node)

        # Handle case when inserting at the end of the list (aka. append).
        if i == self._size:
            self._tl._nxt = new_node  # type: ignore
            new_node._prv = self._tl
            self._tl = new_node
            self._size += 1
            return Option.Some(new_node)

        # Handle the "normal" case.
        # Start by finding the place where to insert the node.
        nxt_node = self.get_at_idx(i).unwrap()
        prv_node = nxt_node._prv
        # Re-arrange pointers.
        new_node._prv = prv_node
        new_node._nxt = nxt_node
        new_node._prv._nxt = new_node  # type: ignore
        new_node._nxt._prv = new_node

        # Increment size.
        self._size += 1

        return Option.Some(new_node)

    def prepend(self, v: T) -> DLLNode[T]:
        """
        Prepends an element to the list, meaning inserts it at the beginning of the list.

        Complexity
        ----------
        Time complexity (in all cases) is `O(1)` (equivalent to inserting at the beginning).

        Parameters
        ----------
        v
            The element to insert.

        Returns
        -------
        `DLLNode[T]`
            The newly created node.
        """
        return self.insert_at_idx(0, v).unwrap()

    def append(self, v: T) -> DLLNode[T]:
        """
        Appends an element to the list, meaning inserts it at the end of the list.

        Complexity
        ----------
        Time complexity (in all cases) is `O(1)` (equivalent to inserting at the end).

        Parameters
        ----------
        v
            The element to insert.

        Returns
        -------
        `DLLNode[T]`
            The newly created node.
        """
        # We know that inserting at index `self._cnt` should always succeed.
        return self.insert_at_idx(self._size, v).unwrap()

    def delete(self, node: DLLNode[T]):
        """
        Deletes a *node* from the list.

        Note
        ----
        Time complexity (in all cases) is `O(1)`.

        Parameters
        ----------
        node
            The node to delete.
        """
        if node == self._hd and node == self._tl:
            self._hd = None
            self._tl = None
        elif node == self._hd:
            self._hd = node._nxt
            node._nxt._prv = None  # type: ignore
        elif node == self._tl:
            self._tl = node._prv
            node._prv._nxt = None  # type: ignore
        else:
            node._prv._nxt = node._nxt  # type: ignore
            node._nxt._prv = node._prv  # type: ignore

        # Detach node from the list.
        node._prv = None
        node._nxt = None

        # Decrement size.
        self._size -= 1

    def delete_at_idx(self, i: int) -> Option[DLLNode[T]]:
        """
        Deletes the node at index (0-based) *i*.

        Note
        ----
        A value of -1 for *i* is accepted and refers to the last element of
        the list, as for Python lists.

        Note
        ----
        The list will remain unchanged if *i* is out of bounds,
        and `Option.NONE()` will be returned.

        Complexity
        ----------
        Best-case time complexity is `O(1)` (deleting at the beginning or the end).
        Worst-case time complexity is `O(n/2)`, which amounts to linear (deleting in the middle).

        Parameters
        ----------
        i
            The index (0-based) of the node to delete.

        Returns
        -------
        `Option[DLLNode]`
            The deleted node or `Option.NONE()` if *i* is out of bounds.
        """
        if i == -1:
            i = self._size - 1
        if i < 0 or i >= self._size:
            return Option.NONE()

        # Handle case where list contains only one element.
        if self._size == 1:
            node = self._hd
            self._hd = None
            self._tl = None
            self._size -= 1
            return Option.Some(node)

        # Handle case when deleting at the beginning of the list.
        if i == 0:
            node = self._hd
            self._hd._nxt._prv = None  # type: ignore
            self._hd = self._hd._nxt  # type: ignore
            self._size -= 1
            return Option.Some(node)
        # Handle case when deleting at the end of the list.
        if i == self._size - 1:
            node = self._tl
            self._tl._prv._nxt = None  # type: ignore
            self._tl = self._tl._prv  # type: ignore
            self._size -= 1
            return Option.Some(node)

        # Handle the "normal" case.
        node = self.get_at_idx(i).unwrap()
        # Re-arrange pointers.
        node._prv._nxt = node._nxt  # type: ignore
        node._nxt._prv = node._prv  # type: ignore
        # Decrement size.
        self._size -= 1

        return Option.Some(node)

    def delete_by_val(self, v: T) -> Option[DLLNode[T]]:
        """
        Deletes the first node with value *v*, if found.

        Complexity
        ----------
        Best-case time complexity is `O(1)` (element with value *v* is the head).
        Worst-case time complexity is `O(n)` (element with value *v* is the tail, or not found).

        Parameters
        ----------
        v

        Returns
        -------
        `Option[DLLNode]`
            The deleted node or `Option.NONE()` if there is no node with value *v*.
        """
        if self._size == 0:
            return Option.NONE()

        # Find the node to delete.
        node = self._hd
        while node is not None and node._v != v:
            node = node._nxt

        # Return early if nothing found.
        if node is None:
            return Option.NONE()

        # Re-arrange pointers.
        if node._prv is not None:
            node._prv._nxt = node._nxt
        else:  # `node` is the head
            self._hd = node._nxt
        if node._nxt is not None:
            node._nxt._prv = node._prv
        else:  # `node` is the tail
            self._tl = node._prv

        # Decrement size.
        self._size -= 1

        return Option.Some(node)

    def __delitem__(self, key):
        if not isinstance(key, int):
            raise TypeError("key should be int")

        if key == -1:
            key = self._size - 1
        if key < 0 or key >= self._size:
            raise IndexError()

        self.delete_at_idx(key)

    def rotate(self, r: int) -> "DoublyLinkedList[T]":
        """
        Rotates (in-place) the list so that so that item `i` becomes item `(i + r) mod n`,
        for all `i` in `[[0, n-1]]` (`n` being the length of the list).

        Complexity
        ----------
        Best-case time complexity is `O(1)` (offset congruent to zero modulo n).
        Worst-case time complexity is `O(n/2)`, which amounts to linear (offset congruent to half of n modulo n).

        Parameters
        ----------
        r
            Rotation offset.

        Returns
        -------
        `DoublyLinkedList[T]`
            This list (useful for chaining operations).
        """
        n = self._size

        # If the list is empty or contains one element, nothing to do.
        if n < 2:
            return self
        assert self._hd is not None
        assert self._tl is not None

        r = r % n
        # Moving on, we know that 0 <= r < n.

        # If no offset, nothing to do.
        if r == 0:
            return self
        # Moving on, we know that 0 < r < n.

        # Connect old head and tail because they aren't anymore.
        # This makes the list (temporarily) circular.
        self._hd._prv = self._tl
        self._tl._nxt = self._hd

        # Find which node is the new head, and which is the new tail.
        # Use the pointers we already have to old head and tail.
        # The following could be simplified but keep exact formula for clarity.
        i = (0 + r) % n  # start from the head
        node = self._hd
        while i > 0:
            i -= 1
            node = node._prv
            assert node is not None

        # Head (and thus tail) found.
        self._hd = node
        self._tl = self._hd._prv
        # "Detach" the new head and tail.
        self._hd._prv = None
        self._tl._nxt = None  # type: ignore

        return self

    def reverse(self) -> "DoublyLinkedList[T]":
        """
        Reverses the order of elements in the list (in-place).

        Complexity
        ----------
        Best-case time complexity is `O(1)` (empty or one-element list).
        Worst-case time complexity is `O(n)` (all other cases).

        Returns
        -------
        `DoublyLinkedList[T]`
            This list (useful for chaining operations).
        """
        # If the list is empty or contains one element, nothing to do.
        if self._size < 2:
            return self
        assert self._hd is not None

        node = self._hd
        while node is not None:
            # Swap prev and next pointers.
            tmp = node._nxt
            node._nxt = node._prv
            node._prv = tmp
            node = tmp

        # Swap head and tail.
        tmp = self._hd
        self._hd = self._tl
        self._tl = tmp

        return self

    def extend(self, lst: "DoublyLinkedList[T]") -> "DoublyLinkedList[T]":
        """
        Extends this list with elements in *lst*.

        This is equivalent to appending the elements of *lst* one-by-one,
        from left to right.

        Parameters
        ----------
        lst

        Returns
        -------
        `DoublyLinkedList[T]`
            This list (useful for chaining operations).
        """
        for el in lst:
            self.append(el)
        return self

    def __add__(self, other) -> "DoublyLinkedList[T]":
        """
        Extends this list with elements in *other*.

        This is equivalent to appending the elements of *lst* one-by-one,
        from left to right.

        Parameters
        ----------
        lst

        Returns
        -------
        `DoublyLinkedList[T]`
            This list (useful for chaining operations).
        """
        if not isinstance(other, DoublyLinkedList):
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
        for el in self:
            py_lst.append(el)
        return py_lst

    def clone(self) -> "DoublyLinkedList[T]":
        """
        Returns a clone (i.e. a deep copy) of this list.

        Returns
        -------
        `DoublyLinkedList[T]`
        """
        return copy.deepcopy(self)

    def selection_sort(self):
        """
        Sorts this list using selection sort (in-place).
        """
        n1 = self._hd
        while n1 is not None:
            nmin = n1
            n2 = n1._nxt
            while n2 is not None:
                if n2._v < nmin._v:
                    nmin = n2
                n2 = n2._nxt

            tmp = n1._v
            n1._v = nmin._v
            nmin._v = tmp
            n1 = n1._nxt

    def insertion_sort(self):
        """
        Sorts this list using insertion sort (in-place).
        """
        if self._size <= 1:
            return

        n1 = self._hd._nxt  # type: ignore
        while n1 is not None:
            n2 = n1
            while n2._prv is not None and n1._v < n2._prv._v:
                n2 = n2._prv

            if n2 == n1:
                n1 = n1._nxt
                continue

            n = n1
            n1 = n1._nxt

            if n._nxt is not None:
                n._prv._nxt = n._nxt  # type: ignore
                n._nxt._prv = n._prv
            else:
                n._prv._nxt = None  # type: ignore
                self._tl = n._prv

            n._nxt = n2
            if n2._prv is not None:
                n._prv = n2._prv
                n2._prv._nxt = n
            else:
                n._prv = None
                self._hd = n
            n2._prv = n

    def quicksort(self):
        """
        Sorts this list using quicksort (in-place).
        """
        DoublyLinkedList._quicksort(self._hd, self._tl, self._size)

    @staticmethod
    def _quicksort(hd: DLLNode[T] | None, tl: DLLNode[T] | None, cnt: int):
        if cnt <= 1:
            return

        pivot, pidx = DoublyLinkedList._partition(hd, tl, tl)  # type: ignore
        DoublyLinkedList._quicksort(hd, pivot._prv, pidx)
        DoublyLinkedList._quicksort(pivot._nxt, tl, cnt - pidx - 1)

    @staticmethod
    def _partition(
        hd: DLLNode[T], tl: DLLNode[T], pivot: DLLNode
    ) -> tuple[DLLNode[T], int]:
        """
        Partitions the list with head *hd* and tail *tl* around a *pivot*, which
        must be a node between *hd* and *tl* (can be *hd* or *tl* as well).

        Parameters
        ----------
        hd
            The head of the list.
        tl
            The tail of the list.
        pivot
            The node chosen to be the pivot around which to do the partitioning.

        Returns
        -------
        `tuple[DLLNode[T], int]`
            Returns the pivot node and its 0-based index in the list (useful for the
            base case of quicksort).
        """
        # Swap the pivot with the tail to continue while knowing
        # the place of the pivot in the list.
        tmp = pivot._v
        pivot._v = tl._v
        tl._v = tmp
        pivot = tl

        tpivot = hd  # temporary pivot
        pidx = 0  # 0-based index of the pivot in the list
        n = hd  # current node
        # Swap all nodes inferior to the pivot with the
        # temporary pivot note.
        while n != tl:
            if n._v <= pivot._v:
                tmp = n._v
                n._v = tpivot._v
                tpivot._v = tmp

                tpivot = tpivot._nxt
                assert tpivot is not None
                pidx += 1

            n = n._nxt
            assert n is not None

        # Swap the temporary pivot with the actual pivot.
        tmp = tpivot._v
        tpivot._v = pivot._v
        pivot._v = tmp
        pivot = tpivot

        return pivot, pidx
