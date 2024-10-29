import copy
from collections import deque
from typing import Deque

from option import Option


class BSTNode[T]:
    """
    A node of `BSTree[T]`.

    Parameters
    ----------
    k
        The value stored in the node.
    left
        (Optional) The left child of the node.

        Defaults to `None`.
    right
        (Optional) The right child of the node.

        Defaults to `None`.
    """

    def __init__(
        self,
        k: T,
        left: "BSTNode[T] | None" = None,
        right: "BSTNode[T] | None" = None,
    ):
        self._k: T = k
        self._left: BSTNode[T] | None = left
        self._right: BSTNode[T] | None = right

    @property
    def k(self) -> T:
        return self._k

    @property
    def left(self) -> "BSTNode[T] | None":
        return self._left

    @property
    def right(self) -> "BSTNode[T] | None":
        return self._right


class BSTree[T]:
    r"""
    A binary search tree.

    Parameters
    ----------
    ks
        (Optional) A list of keys to insert in the tree.

        Defaults to `[]`.

    Examples
    --------
    .. code-block:: python
        
        bst = BSTree([10, 5, 15, 2, 12, 7, 17])
        print(bst)
        #      10
        #   /¯¯¯ ¯¯¯\
        #   5      15
        # /¯ ¯\   /¯ ¯\
        # 2   7  12  17
    """

    def __init__(self, ks: list[T] = []):
        self._root: BSTNode[T] | None = None
        for k in ks:
            self.insert(k)

    def __repr__(self) -> str:
        """
        Returns a string representation of this binary search tree (useful for debugging).

        Note
        ----
        It is hard to a readable tree representation in all cases, but this implementation should be
        sufficient for simple trees.

        Note
        ----
        This implementation is highly inspired by
        https://stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python.

        Returns
        -------
        `str`
        """
        nlevels = self.height
        width = pow(2, nlevels + 1)

        q: Deque[tuple[(BSTNode[T] | None, int, int, str)]] = deque(
            [(self._root, 0, width, "c")]
        )
        levels = []

        while q:
            node, level, x, align = q.popleft()
            if node is not None:
                if len(levels) <= level:
                    levels.append([])

                levels[level].append([node, level, x, align])
                seg = width // (pow(2, level + 1))
                q.append((node._left, level + 1, x - seg, "l"))
                q.append((node._right, level + 1, x + seg, "r"))

        s = ""
        for i, lst in enumerate(levels):
            pre = 0
            preline = 0
            linestr = ""
            pstr = ""
            seg = width // (pow(2, i + 1))
            for t in lst:
                valstr = str(t[0]._k)
                if t[3] == "r":
                    linestr += (
                        " " * (t[2] - preline - 1 - seg - seg // 2)
                        + "¯" * (seg + seg // 2)
                        + "\\"
                    )
                    preline = t[2]
                if t[3] == "l":
                    linestr += " " * (t[2] - preline - 1) + "/" + "¯" * (seg + seg // 2)
                    preline = t[2] + seg + seg // 2
                pstr += (
                    " " * (t[2] - pre - len(valstr)) + valstr
                )  # correct the position according to the number size
                pre = t[2]
            s += linestr + "\n" + pstr + "\n"
        return s

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        """
        Whether this binary search tree is non-empty.

        Return
        -------
        `bool`
            `True` if non-empty, `False` otherwise.
        """
        return self._root is not None

    @property
    def is_empty(self) -> bool:
        """
        Whether this binary search tree is empty.
        """
        return self._root is None

    def __eq__(self, other) -> bool:
        if not isinstance(other, BSTree):
            return False

        q1: Deque[BSTNode[T] | None] = deque([self._root])
        q2: Deque[BSTNode[T] | None] = deque([other._root])
        n1: BSTNode[T] | None = None
        n2: BSTNode[T] | None = None
        while q1 and q2:
            n1 = q1.popleft()
            n2 = q2.popleft()

            if n1 == None:
                ns_eq = n2 == None
            elif n2 == None:
                ns_eq = n1 == None
            else:
                ns_eq = n1._k == n2._k

            if not ns_eq:
                return False
            if n1 != None:
                q1.append(n1._left)
                q1.append(n1._right)
            if n2 != None:
                q2.append(n2._left)
                q2.append(n2._right)

        # If one queue got empty before the other, then the trees don't have the same
        # number of nodes. This check may not be necessary, as if a tree has less nodes
        # than the other, it will have a None leaf that will fail the equality check
        # in the while loop.
        if q1 or q2:
            return False
        return True

    @property
    def size(self) -> int:
        """
        The size of this tree, i.e. its number of nodes.
        """
        return BSTree._size_rec(self._root)

    @staticmethod
    def _size_rec(node: BSTNode[T] | None) -> int:
        """
        Returns the size of the tree with root *node*.

        Parameters
        ----------
        node

        Returns
        -------
        `int`
        """
        if node is None:
            return 0
        return 1 + BSTree._size_rec(node._left) + BSTree._size_rec(node._right)

    @property
    def height(self) -> int:
        """
        The height of this tree, i.e. the length of the longest path from the root to a leaf.
        """
        return BSTree._height_rec(self._root)

    @staticmethod
    def _height_rec(node: BSTNode[T] | None) -> int:
        """
        Returns the height of the tree with root *node*.

        Parameters
        ----------
        node

        Returns
        -------
        `int`
        """
        if node is None:
            return -1
        return 1 + max(BSTree._height_rec(node._left), BSTree._height_rec(node._right))

    def contains(self, k: T) -> bool:
        """
        Returns whether the value *k* was found in this tree.

        Parameters
        ----------
        k

        Returns
        -------
        `bool`
        """
        return self._contains_it(k)

    def _contains_it(self, k: T) -> bool:
        """
        Returns whether the value *k* was found in this tree.

        Implementation details
        ----------------------
        This function finds the key iteratively.

        Parameters
        ----------
        k

        Returns
        -------
        `bool`
        """
        node = self._root
        while node is not None:
            if k < node._k:  # type: ignore
                node = node._left
            elif k > node._k:  # type: ignore
                node = node._right
            else:
                return True

        return False

    def _contains_rec(self, k: T) -> bool:
        """
        Returns whether the value *k* was found in this tree.

        Implementation details
        ----------------------
        This function finds the key recursively.

        Parameters
        ----------
        k

        Returns
        -------
        `bool`
        """
        return BSTree._contains_rec_helper(self._root, k)

    @staticmethod
    def _contains_rec_helper(root: BSTNode[T] | None, k: T) -> bool:
        if root is None:
            return False
        if k < root._k:  # type: ignore
            return BSTree._contains_rec_helper(root._left, k)
        elif k > root._k:  # type: ignore
            return BSTree._contains_rec_helper(root._right, k)
        else:
            return True

    def insert(self, k: T) -> BSTNode[T]:
        """
        Inserts value *k* into this binary search tree.

        Parameters
        ----------
        k

        Returns
        -------
        `BSTNode[T]`
            The newly created node, or the already existing node
            with value *k* if found in the tree.
        """
        return self._insert_it(k)

    def _insert_it(self, k: T) -> BSTNode[T]:
        """
        Inserts value *k* into this binary search tree.

        Implementation details
        ----------------------
        This function inserts a new value iteratively.

        Parameters
        ----------
        k

        Returns
        -------
        `BSTNode[T]`
            The newly created node, or the already existing node
            with value *k* if found in the tree.
        """
        # Find the parent/previous node to the one we want to insert.
        cur_node = self._root
        prv_node = None
        while cur_node is not None:
            prv_node = cur_node
            if k < cur_node._k:  # type: ignore
                cur_node = cur_node._left
            elif k > cur_node._k:  # type: ignore
                cur_node = cur_node._right
            else:
                break

        # Insert the new node if needed.
        if prv_node is None:
            new_node = BSTNode(k)
            self._root = new_node
            return new_node
        elif k < prv_node._k:  # type: ignore
            new_node = BSTNode(k)
            prv_node._left = BSTNode(k)
            return new_node
        elif k > prv_node._k:  # type: ignore
            new_node = BSTNode(k)
            prv_node._right = BSTNode(k)
            return new_node
        else:
            return prv_node

    def _insert_rec(self, k: T) -> BSTNode[T]:
        """
        Inserts value *k* into this binary search tree.

        Implementation details
        ----------------------
        This function inserts a new value recursively.

        Parameters
        ----------
        k

        Returns
        -------
        `BSTNode[T]`
            The newly created node, or the already existing node
            with value *k* if found in the tree.
        """
        self._root, new_node = BSTree._insert_rec_helper(self._root, k)
        return new_node

    @staticmethod
    def _insert_rec_helper(
        node: BSTNode[T] | None, k: T
    ) -> tuple[BSTNode[T], BSTNode[T]]:
        if node is None:
            new_node = BSTNode(k)
            return new_node, new_node

        if k < node._k:  # type: ignore
            node._left, new_node = BSTree._insert_rec_helper(node._left, k)
        elif k > node._k:  # type: ignore
            node._right, new_node = BSTree._insert_rec_helper(node._right, k)
        else:  # k == node.key
            new_node = node

        return node, new_node

    def get(self, k: T) -> Option[BSTNode[T]]:
        """
        Returns the node with key *k* if found.

        Parameters
        ----------
        k

        Returns
        -------
        `Option[BSTNode[T]]`
        """
        return self._get_it(k)

    def _get_it(self, k: T) -> Option[BSTNode[T]]:
        """
        Returns the node with key *k* if found.

        Implementation details
        ----------------------
        This function performs an interative binary search.

        Parameters
        ----------
        k

        Returns
        -------
        `Option[BSTNode[T]]`
        """
        n = self._root
        while n is not None:
            if n._k == k:
                return Option.Some(n)
            elif k < n._k:  # type: ignore
                n = n.left
            else:
                n = n.right

        return Option.NONE()

    def _get_rec(self, k: T) -> Option[BSTNode[T]]:
        """
        Returns the node with key *k* if found.

        Implementation details
        ----------------------
        This function performs a recursive binary search.

        Parameters
        ----------
        k

        Returns
        -------
        `Option[BSTNode[T]]`
        """
        node = self._get_rec_helper(self._root, k)
        return Option.Some(node) if node is not None else Option.NONE()

    def _get_rec_helper(self, node: BSTNode[T] | None, key: T) -> BSTNode[T] | None:
        if node == None:
            return None
        elif node._k == key:
            return node
        elif key < node._k:  # type: ignore
            return self._get_rec_helper(node.left, key)
        else:
            return self._get_rec_helper(node.right, key)

    def delete(self, k: T) -> Option[BSTNode[T]]:
        """
        Deletes the node with key *k*, if present in this tree.

        Parameters
        ----------
        k

        Returns
        -------
        `Option[BSTNode[T]]`
            The node with key *k* that was found in the tree and deleted,
            `Option.NONE()` if no such node was found.
        """
        return self._delete_it(k)

    def _delete_it(self, k: T) -> Option[BSTNode[T]]:
        """
        Deletes the node with key *k*, if present in this tree.

        Parameters
        ----------
        k

        Returns
        -------
        `Option[BSTNode[T]]`
            The node with key *k* that was found in the tree and deleted,
            `Option.NONE()` if no such node was found.
        """
        # If empty tree, return early.
        if self._root is None:
            return Option.NONE()

        # Find the node to delete.
        parent = None
        node = self._root
        while node is not None and node._k != k:
            if k < node._k:  # type: ignore
                parent = node
                node = node._left
            elif k > node._k:  # type: ignore
                parent = node
                node = node._right

        # Didn't found a node with key *k*.
        if node is None:
            return Option.NONE()

        clone = copy.deepcopy(node)
        # Delete the node.
        if node._left is None and node._right is None:  # node is a leaf
            # Just detach the node from its parent.
            if parent is None:  # then node is the root
                self._root = None
            else:
                if parent._left == node:
                    parent._left = None
                else:
                    parent._right = None
        elif (
            node._left is not None and node._right is not None
        ):  # node has two children
            # Replace node by the one with the smallest greater key than node.key (aka. the successor).
            # First find the node with the smallest greater key.
            sg_node = node._right
            sg_parent = node
            while sg_node._left is not None:
                sg_parent = sg_node
                sg_node = sg_node._left
            # Change the key of node to be that of sg_node.
            node._k = sg_node._k
            # Detach sg_node.
            if sg_parent._left == sg_node:
                sg_parent._left = None
            else:
                sg_parent._right = None
        elif node._left is not None:  # node has only one (left) child
            if parent is None:  # then node is the root
                self._root = node._left
            else:
                # node.left takes the place of node
                if parent._left == node:
                    parent._left = node._left
                else:
                    parent._right = node._left
        elif node._right is not None:  # node has only one (right) child
            if parent is None:  # then node is the root
                self._root = node._right
            else:
                # node.left takes the place of node
                if parent._left == node:
                    parent._left = node._right
                else:
                    parent._right = node._right

        return Option.Some(clone)

    @staticmethod
    def min(node: BSTNode[T]) -> BSTNode[T]:
        """
        Returns the minimum value in the (sub)tree with root *node*,
        if it exists.

        Returns
        -------
        `BSTNode[T]`
        """
        n = node
        prv = n
        while n != None:
            prv = n
            n = n._left
        return prv

    @staticmethod
    def max(node: BSTNode[T]) -> BSTNode[T]:
        """
        Returns the maximum value in the (sub)tree with root *node*,
        if it exists.

        Returns
        -------
        `BSTNode[T]`
        """
        n = node
        prv = n
        while n != None:
            prv = n
            n = n._right
        return prv

    @staticmethod
    def successor(node: BSTNode[T]) -> Option[BSTNode[T]]:
        """
        Returns the sucessor of *node* if it exists.

        The successor of a node *n* in a binary search tree (with all the keys distinct)
        is the node that has the smallest key greater than *n*'s key.

        Parameters
        ----------
        node

        Returns
        -------
        `Option[BSTNode[T]]`
        """
        if node._right == None:
            return Option.NONE()
        else:
            return Option.Some(BSTree.min(node._right))

    @staticmethod
    def predecessor(node: BSTNode[T]) -> Option[BSTNode[T]]:
        """
        Returns the predecessor of *node* if it exists.

        The predecessor of a node *n* in a binary search tree (with all the keys distinct)
        is the node that has the largest key smaller than *n*'s key.

        Parameters
        ----------
        node

        Returns
        -------
        `Option[BSTNode[T]]`
        """
        if node._left == None:
            return Option.NONE()
        else:
            return Option.Some(BSTree.max(node._left))
