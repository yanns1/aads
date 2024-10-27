import copy
from typing import Iterator

from option import Option


class SLLNode[T]:
    """
    A node of `SinglyLinkedList[T]`.

    Parameters
    ----------
    v
        The value of the node.
    """

    def __init__(self, v: T):
        self._v: T = v
        self._nxt: SLLNode[T] | None = None

    @property
    def v(self):
        return self._v

    @property
    def nxt(self):
        return self._nxt

    def __repr__(self) -> str:
        """
        Printable representation of `SLLNode`, used for debugging.

        Returns
        -------
        `str`
        """
        nxt_str = str(self._nxt._v) if self._nxt is not None else "None"
        return f"{{val:{self._v}, nxt:{nxt_str}}}"


class SLLIterator[T](Iterator):
    """
    An iterator over `SinglyLinkedList[T]`.

    Note
    ----
    Time complexity (in all cases) of iteration is `O(n)` where `n` is the length of the list.
    """

    def __init__(self, start_node: SLLNode[T] | None):
        self._cur_node = start_node  # current node

    def __next__(self) -> T:
        if self._cur_node is None:
            raise StopIteration

        n = self._cur_node._v
        self._cur_node = self._cur_node._nxt
        return n


class SinglyLinkedList[T]:
    """
    A singly-linked list.
    """

    def __init__(self, lst: list[T] = []):
        self._hd: SLLNode[T] | None = None
        self._size: int = 0

        for i in range(len(lst) - 1, -1, -1):
            self.prepend(lst[i])

    def __repr__(self) -> str:
        """
        Printable representation of `SinglyLinkedList`, used for debugging.

        Note
        ----
        Time complexity (in all cases) is `O(n)` where `n` is the length of the list.

        Returns
        -------
        `str`
        """
        s = "["

        node = self._hd
        while node is not None:
            s += f"{node._v}"
            if node._nxt is not None:
                s += " > "

            node = node._nxt

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

    def __iter__(self) -> SLLIterator[T]:
        return SLLIterator(self._hd)

    @property
    def is_empty(self) -> bool:
        """
        Returns whether the list is empty (no elements) or not.

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
        if not isinstance(other, SinglyLinkedList):
            return False

        len1 = len(self)
        len2 = len(other)
        if len1 != len2:
            return False

        for el1, el2 in zip(self, other):
            if el1 != el2:
                return False

        return True

    def get(self, node: SLLNode[T]) -> T:
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

    def get_at_idx(self, i: int) -> Option[SLLNode[T]]:
        """
        Returns the node at index *i*.

        Note
        ----
        A value of -1 for *i* is accepted and refers to the last element of
        the list, as for Python lists.

        Complexity
        ----------
        Best-case time complexity is `O(1)` (accessing the head).
        Worst-case time complexity is `O(n)` (accessing the tail).

        Parameters
        ----------
        i
            The index (0-based) of the node to get.

        Returns
        -------
        `Option[SLLNode[T]]`
            The node at index *i* if it exists or `Option.NONE()`
            if index out of bounds.
        """
        if i == -1:
            i = self._size - 1
        if i < 0 or i >= self._size:
            return Option.NONE()

        if i == 0:
            return Option.Some(self._hd)

        j = 1
        node = self._hd._nxt  # type: ignore
        while j < i:
            j += 1
            node = node._nxt  # type: ignore

        return Option.Some(node)

    def get_by_val(self, v: T) -> Option[SLLNode[T]]:
        """
        Returns the first node with value *v*.

        Complexity
        ----------
        Best-case time complexity is `O(1)` (element with value *v* is the head).
        Worst-case time complexity is `O(n)` (element with value *v* is the tail, or not found).

        Parameters
        ----------
        v
            The value of the node to get.

        Returns
        -------
        `Option[SLLNode[T]]`
            The first node with value *v* if it exists, `Option.NONE()` if
            *v* not found.
        """
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

    def set(self, node: SLLNode[T], v: T):
        """
        Sets the value of *node* to *v*.

        Parameters
        ----------
        node
        v
        """
        node._v = v

    def set_at_idx(self, i: int, v: T) -> Option[SLLNode[T]]:
        """
        Sets the value of node at index *i* to *v*.

        Parameters
        ----------
        i
        v

        Returns
        -------
        `Option[SLLNode[T]]`
            The node at index *i*, or `Option.NONE()` if *i* out of bounds.
        """
        node = self.get_at_idx(i)
        if node.is_none:
            return Option.NONE()

        node = node.unwrap()
        node._v = v
        return Option.Some(node)

    def set_by_val(self, v: T, new_v: T) -> Option[SLLNode[T]]:
        """
        Sets the value of first encountered node with value *v* to *new_v*.

        Parameters
        ----------
        v
        new_v

        Returns
        -------
        `Option[SLLNode[T]]`
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

        res = self.set_at_idx(key, value)
        if res.is_none:
            raise IndexError()

    def insert(self, v: T, neighbor: Option[SLLNode[T]]) -> SLLNode[T]:
        """
        Inserts an element before or *after* the node *neighbor*.

        Complexity
        ----------
        Time complexity (in all cases) is `O(1)`.

        Parameters
        ----------
        v
            The element to insert.
        neighbor
            The neighbor of the node to create.

            If `None`, inserts at the beginning of the list.

        Returns
        -------
        `SLLNode[T]`
            The newly created node.
        """
        new_node = SLLNode(v)

        if neighbor == Option.NONE():
            if self._hd is not None:
                new_node._nxt = self._hd
            self._hd = new_node
            self._size += 1
            return new_node

        nbr = neighbor.unwrap()
        new_node._nxt = nbr._nxt
        nbr._nxt = new_node
        self._size += 1
        return new_node

    def insert_at_idx(self, i: int, v: T) -> Option[SLLNode[T]]:
        """
        Inserts an element with value *v* at index (0-based) *i*.

        Note
        ----
        A value of -1 for *i* is accepted and means inserting at
        the end of the list.

        Complexity
        ----------
        Best-case time complexity is `O(1)` (inserting at the beginning).
        Worst-case time complexity is `O(n)` (inserting at the end).

        Parameters
        ----------
        i
        v

        Returns
        -------
        `Option[SLLNode[T]]`
            The newly created node, or `Option.NONE()` if index out
            of bounds.
        """
        if i == -1:
            i = self._size
        # Do nothing if index out of bounds.
        if i < 0 or i > self._size:
            return Option.NONE()

        # Instantiate new node.
        new_node = SLLNode(v)

        # Handle case when inserting at the beginning of the list (aka. prepend).
        if i == 0:
            new_node._nxt = self._hd
            self._hd = new_node
            self._size += 1
            return Option.Some(new_node)

        # Handle the "normal" case.
        # Start by finding the place where to insert the node.
        prv_node = self.get_at_idx(i - 1).unwrap()
        # Re-arrange pointers.
        new_node._nxt = prv_node._nxt
        prv_node._nxt = new_node

        # Increment count.
        self._size += 1

        return Option.Some(new_node)

    def prepend(self, v: T) -> SLLNode[T]:
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
        `SLLNode[T]`
            The newly created node.
        """
        return self.insert_at_idx(0, v).unwrap()

    def append(self, v: T) -> SLLNode[T]:
        """
        Appends an element to the list, meaning inserts it at the end of the list.

        Complexity
        ----------
        Time complexity (in all cases) is `O(n)` (equivalent to inserting at the end).

        Parameters
        ----------
        v
            The element to insert.

        Returns
        -------
        `SLLNode[T]`
            The newly created node.
        """
        return self.insert_at_idx(self._size, v).unwrap()

    def delete(self, node: SLLNode[T]):
        """
        Deletes a *node* from the list.

        Complexity
        ----------
        Best-case time complexity is `O(1)` (when deleting the head).
        Worst-case time complexity is `O(n)` (when deleting the tail).

        Parameters
        ----------
        node
            The node to delete.
        """
        if node == self._hd:
            # Re-arrange pointers.
            self._hd = node._nxt
            node._nxt = None
            # Decrement count.
            self._size -= 1
            return

        # Find the node before the one to delete.
        prv_node = self._hd
        while prv_node is not None and prv_node._nxt != node:
            prv_node = prv_node._nxt

        if prv_node is None:
            # Didn't found the node to delete in the list.
            return

        # Re-arrange pointers.
        prv_node._nxt = node._nxt
        node._nxt = None

        # Decrement count.
        self._size -= 1

    def delete_at_idx(self, i: int) -> Option[SLLNode[T]]:
        """
        Deletes the node at index (0-based) *i*.

        Note
        ----
        A value of -1 for *i* is accepted and refers to the last element of
        the list, as for Python lists.

        Complexity
        ----------
        Best-case time complexity is `O(1)` (deleting the head).
        Worst-case time complexity is `O(n)` (deleting the tail).

        Parameters
        ----------
        idx
            The index (0-based) of the node to delete.

        Returns
        -------
        `Option[SLLNode[T]]`
            The deleted node or `Option.NONE()` if index is out of bounds.
        """
        if i == -1:
            i = self._size - 1
        if i < 0 or i >= self._size:
            return Option.NONE()

        # Handle case where deleting at the beginning.
        if i == 0:
            node = self._hd
            # Re-arrange pointers.
            self._hd = node._nxt  # type: ignore
            node._nxt = None  # type: ignore
            # Decrement count.
            self._size -= 1
            return Option.Some(node)

        # Find node before the one to delete.
        j = 0
        prv_node = self._hd
        while j < i - 1:
            j += 1
            prv_node = prv_node._nxt  # type: ignore
        node = prv_node._nxt  # type: ignore

        # Re-arrange pointers
        prv_node._nxt = node._nxt  # type: ignore
        node._nxt = None  # type: ignore

        # Decrement count.
        self._size -= 1

        return Option.Some(node)

    def delete_by_val(self, v: int) -> Option[SLLNode[T]]:
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
        `Option[SLLNode[T]]`
            The deleted node or `Option.NONE()` if there is no node with value *v*.
        """
        if self._size == 0:
            return Option.NONE()
        assert self._hd is not None

        # Find the node to delete.
        prv_node = None
        node = self._hd
        while node is not None and node._v != v:
            prv_node = node
            node = node._nxt

        # Return early if nothing found.
        if node is None:
            return Option.NONE()

        # Re-arrange pointers.
        if prv_node is not None:
            prv_node._nxt = node._nxt
        else:  # `node` is the head
            self._hd = node._nxt
        node._nxt = None

        # Decrement count.
        self._size -= 1

        return Option.Some(node)

    def __delitem__(self, key):
        if not isinstance(key, int):
            raise TypeError("key should be int")

        if key == -1:
            key = self._size - 1

        res = self.delete_at_idx(key)
        if res.is_none:
            raise IndexError()

    def extend(self, lst: "SinglyLinkedList[T]") -> "SinglyLinkedList[T]":
        """
        Extends this list with elements in *lst*.

        This is equivalent to appending the elements of *lst* one-by-one,
        from left to right.

        Parameters
        ----------
        lst

        Returns
        -------
        `SinglyLinkedList[T]`
            This list (useful for chaining operations).
        """
        # Could do more efficient if kept track of the tail of the list.
        # In fact, that is not the only operation that would benefit
        # from that. Append would to.
        for el in lst:
            self.append(el)
        return self

    def __add__(self, other) -> "SinglyLinkedList[T]":
        """
        Extends this list with elements in *other*.

        This is equivalent to appending the elements of *lst* one-by-one,
        from left to right.

        Parameters
        ----------
        lst

        Returns
        -------
        `SinglyLinkedList[T]`
            This list (useful for chaining operations).
        """
        if not isinstance(other, SinglyLinkedList):
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

    def clone(self) -> "SinglyLinkedList[T]":
        """
        Returns a clone (i.e. a deep copy) of this list.

        Returns
        -------
        `SinglyLinkedList[T]`
        """
        return copy.deepcopy(self)
