from math import floor
from typing import Callable, Generic, TypeVar

from option import Option

K = TypeVar("K")
Number = TypeVar("Number", int, float)


class Item(Generic[K, Number]):
    """
    An item of `BinaryHeap`, the conjunction of a key and a priority.

    Parameters
    ----------
    k
    priority
    """

    def __init__(self, k: K, p: Number):
        self._k: K = k
        self._p: Number = p

    def __repr__(self) -> str:
        return f"{self._k} ({self._p})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Item):
            return False
        return other._p == self._p and other._k == self._k

    @property
    def k(self):
        return self._k

    @property
    def p(self):
        return self._p


class BinaryHeap(Generic[K, Number]):
    """
    A binary heap with (total) order *o*.

    This data structure thus preserves the heap invariant:

        For each node, the node's key is greater (according to *o*)
        than the keys in the node's children.

    Parameters
    ----------
    items
        A list of initial items to insert into the heap.

        An item takes the form of a tuple with the first element
        being the key of the item and the second element its
        priority.
    o
        The order between elements of the heap.

        For any two items *it1* et *it2*, if `o(it1.p, it2.p) == True`, then
        *it1* is considered greater than *it2*, meaning this heap will serve
        *it1* before *it2*.

        Defaults to `lambda a, b: a >= b`, i.e. a binary *max* heap.
    """

    def __init__(
        self,
        o: Callable[[Number, Number], bool] = lambda a, b: a >= b,
        items: list[tuple[K, Number]] = [],
    ) -> None:
        self._arr: list[Item[K, Number]] = list(map(lambda t: Item(t[0], t[1]), items))
        self._o: Callable[[Number, Number], bool] = o

        n = len(self._arr)
        i_start = floor(n / 2) - 1
        for i_parent in range(i_start, -1, -1):
            self._percolate_down(i_parent)

    def __repr__(self) -> str:
        return str(self._arr)

    def __eq__(self, bh) -> bool:
        if not isinstance(bh, BinaryHeap):
            return False
        return self._arr == bh._arr

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        return not self.is_empty

    def __iter__(self):
        return self

    def __next__(self) -> Item[K, Number]:
        item = self.pop()
        if item.is_some:
            return item.unwrap()
        else:
            raise StopIteration

    @property
    def is_empty(self) -> bool:
        """
        Whether this heap is empty (i.e. no items).
        """
        return len(self._arr) == 0

    @property
    def size(self) -> int:
        """
        The size of this heap, i.e. its number of items.
        """
        return len(self._arr)

    def push(self, item: Item[K, Number]) -> "BinaryHeap[K, Number]":
        """
        Pushes an *item* onto this heap.

        Parameters
        ----------
        item
        """
        i_item = len(self._arr)
        i_parent = self._parent_idx(i_item)

        # Insert the new item at the end of the heap.
        self._arr.append(item)

        # "Percolate up" the new item by swapping it with its parent
        # if it has a greater priority than it.
        while i_item > 0 and self._o(self._arr[i_item]._p, self._arr[i_parent]._p):
            self._arr[i_item], self._arr[i_parent] = (
                self._arr[i_parent],
                self._arr[i_item],
            )
            i_item, i_parent = i_parent, self._parent_idx(i_parent)

        return self

    def pop(self) -> Option[Item[K, Number]]:
        """
        Pops the item on top of this heap, and returns it.

        Returns
        -------
        `Option[Item[K, Number]]`
        """
        if self.is_empty:
            return Option.NONE()
        item = self._arr[0]
        self._delete_at_idx(0)
        return Option.Some(item)

    def peek(self) -> Option[Item[K, Number]]:
        """
        Returns the item on top of this heap.

        Returns
        -------
        `Option[Item[K, Number]]`
        """
        if self.is_empty:
            return Option.NONE()
        return Option.Some(self._arr[0])

    def delete(self, k: K) -> bool:
        """
        Deletes the item with key *k* in this heap (if found).

        Parameters
        ----------
        k

        Returns
        -------
        `bool`
            `True` if an item with key *k* was found and thus deleted,
            `False` if no such node was found.
        """
        # Search the item to delete.
        i = 0
        n = len(self._arr)
        while i < n and self._arr[i]._k != k:
            i += 1

        # If not found, return early.
        if i >= n:
            return False

        # Swap the element to delete with the last element.
        self._arr[i] = self._arr[-1]
        # Remove the last element (i.e. the one we want to delete).
        del self._arr[-1]
        n -= 1
        self._percolate_down(i)

        return True

    def _delete_at_idx(self, i: int):
        if i == -1:
            i = len(self._arr) - 1
        if i < 0 or i >= len(self._arr):
            return

        n = len(self._arr)
        self._arr[i] = self._arr[-1]
        del self._arr[-1]
        n -= 1
        self._percolate_down(i)

    @staticmethod
    def _children_idxs(parent_idx: int) -> tuple[int, int]:
        """
        Returns the indexes of *parent_idx*'s children.

        Parameters
        ----------
        parent_idx

        Returns
        -------
        `tuple[int, int]`
        """
        return 2 * parent_idx + 1, 2 * parent_idx + 2

    @staticmethod
    def _parent_idx(child_idx: int) -> int:
        """
        Returns the index of the parent of *child_idx*.

        Parameters
        ----------
        child_idx

        Returns
        -------
        `int`
        """
        return floor((child_idx - 1) / 2)

    def _percolate_down(
        self,
        i: int,
    ):
        """
        Percolates down item at index *i*.

        In other words, move item *i* down the tree by swapping it with its
        highest priority child if it has a lower priority than it.

        Parameters
        ----------
        i
        """
        i_end = len(self._arr) - 1
        if not (0 <= i <= i_end):
            return

        parent_priority = self._arr[i]._p
        i_child1, i_child2 = self._children_idxs(i)
        i_sup_child = i_child1
        if i_child1 <= i_end and i_child2 <= i_end:
            if self._o(self._arr[i_child2]._p, self._arr[i_child1]._p):
                i_sup_child = i_child2
        if i_child1 > i_end and i_child2 <= i_end:
            i_sup_child = i_child2
        # if i_child2 > i_end and i_child1 <= i_end:
        # stay as is
        # if i_child1 > i_end and i_child2 > i_end:
        # should not happen however, because we only consider nodes with at least one child
        # stay as is; will not be able to enter while loop anyway

        while i_sup_child <= i_end and self._o(
            self._arr[i_sup_child]._p, parent_priority
        ):
            # swap parent and sup_child
            self._arr[i], self._arr[i_sup_child] = self._arr[i_sup_child], self._arr[i]

            # determine new sup_child
            i = i_sup_child
            parent_priority = self._arr[i]._p
            i_child1, i_child2 = self._children_idxs(i)
            i_sup_child = i_child1
            if i_child1 <= i_end and i_child2 <= i_end:
                if self._o(self._arr[i_child2]._p, self._arr[i_child1]._p):
                    i_sup_child = i_child2
            if i_child1 > i_end and i_child2 <= i_end:
                i_sup_child = i_child2


class BinaryMinHeap(Generic[K, Number], BinaryHeap[K, Number]):
    """
    A subclass of `BinaryHeap` with order:

    .. code-block:: python

        lambda a, b: a <= b

    giving a binary min heap.

    Parameters
    ----------
    items
        A list of initial items to insert in the heap.
    """

    def __init__(self, items: list[tuple[K, Number]] = [], **kwargs):
        super().__init__(items=items, o=lambda a, b: a <= b, **kwargs)


class BinaryMaxHeap(Generic[K, Number], BinaryHeap[K, Number]):
    """
    A subclass of `BinaryHeap` with order:

    .. code-block:: python

        lambda a, b: a >= b

    giving a binary max heap.

    Parameters
    ----------
    items
        A list of initial items to insert in the heap.
    """

    def __init__(self, items: list[tuple[K, Number]] = [], **kwargs):
        super().__init__(items=items, o=lambda a, b: a >= b, **kwargs)
