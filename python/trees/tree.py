from collections import deque
from typing import Any, Callable


class LCRSNode[T]:
    """
    A tree in left-child right-sibling representation.

    Parameters
    ----------
    k
        The key of the root node.
    left
        The leftmost sibling.
    right
        The right sibling.
    """

    def __init__(
        self,
        k: T,
        left: "LCRSNode[T] | None" = None,
        right: "LCRSNode[T] | None" = None,
    ):
        self.k: T = k
        self.left: LCRSNode[T] | None = left
        self.right: LCRSNode[T] | None = right

    def __len__(self) -> int:
        return LCRSNode.size(self)

    @staticmethod
    def size(root: "LCRSNode[T] | None") -> int:
        """
        Returns the size (i.e. the number of nodes) of the tree with *root* as root node.

        Parameters
        ----------
        root

        Returns
        -------
        `int`
        """
        return LCRSNode._size_it(root)

    @staticmethod
    def _size_it(root: "LCRSNode[T] | None") -> int:
        """
        Returns the size (i.e. the number of nodes) of the tree with *root* as root node.

        Implementation details
        ----------------------
        This computes the tree's size iteratively.

        Parameters
        ----------
        root

        Returns
        -------
        `int`
        """
        if root is None:
            return 0

        s = 0
        q = deque([root])
        while q:
            node = q.popleft()
            s += 1
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)

        return s

    @staticmethod
    def _size_rec(root: "LCRSNode[T] | None") -> int:
        """
        Returns the size (i.e. the number of nodes) of the tree with *root* as root node.

        Implementation details
        ----------------------
        This computes the tree's size recursively.

        Parameters
        ----------
        root

        Returns
        -------
        `int`
        """
        if root is None:
            return 0
        sl = LCRSNode._size_rec(root.left)
        sr = LCRSNode._size_rec(root.right)
        return 1 + sl + sr

    @staticmethod
    def height(root: "LCRSNode[T] | None") -> int:
        """
        Returns the height (i.e. the length of the longest path from root to leaf)
        of the tree with *root* as root node.

        Parameters
        ----------
        root

        Returns
        -------
        `int`
        """
        return LCRSNode._height_rec(root)

    @staticmethod
    def _height_rec(root: "LCRSNode[T] | None") -> int:
        """
        Returns the height (i.e. the length of the longest path from root to leaf)
        of the tree with *root* as root node.

        Implementation details
        ----------------------
        This computes the tree's height recursively.

        Parameters
        ----------
        root

        Returns
        -------
        `int`
        """
        if root is None:
            return -1

        h = 0 if root.is_leaf() else 1
        hl = 0 if root.left is None else LCRSNode._height_rec(root.left)
        hr = 0 if root.right is None else LCRSNode._height_rec(root.right)
        return h + max(hl, hr)

    def add_child(self, k: T) -> "LCRSNode[T]":
        """
        Creates a node with key *key* as a new child of this node.

        Parameters
        ----------
        k
            The key of the new child node.

        Returns
        -------
        `LCRSNode[T]`
            The created child node.
        """
        if self.left is None:
            self.left = LCRSNode(k)
            return self.left
        else:
            p = self.left
            while p.right is not None:
                p = p.right
            p.right = LCRSNode(k)
            return p.right

    def degree(self) -> int:
        """
        Returns the degree of this node, i.e. its number of children.

        Returns
        -------
        `int`
        """
        d = 0
        p = self.left
        while p is not None:
            d += 1
            p = p.right
        return d

    def is_leaf(self) -> bool:
        """
        Returns whether this node is a leaf (`True` if is a leaf, `False` otherwise).

        Returns
        -------
        `bool`
        """
        return self.left is None

    @staticmethod
    def walk(root: "LCRSNode[T] | None", f: Callable[[T], Any]):
        """
        Walks the tree with *root* as root node in a pre-order manner.

        Parameters
        ----------
        root
            The root of the tree to walk.
        f
            A function to apply on the key of each node traversed.
        """
        if root is None:
            return

        f(root.k)
        if root.left is not None:
            LCRSNode.walk(root.left, f)
        if root.right is not None:
            LCRSNode.walk(root.right, f)
