from collections import deque
from enum import Enum
from typing import Any, Callable, Deque

from option import Option


class DFTOrder(Enum):
    PRE_ORDER = 0
    IN_ORDER = 1
    POST_ORDER = 2
    REVERSE_PRE_ORDER = 3
    REVERSE_IN_ORDER = 4
    REVERSE_POST_ORDER = 5


class BTNode[T]:
    """
    A node of `BTree[T]`.

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
        left: "BTNode[T] | None" = None,
        right: "BTNode[T] | None" = None,
    ):
        self._k: T = k
        self._left: BTNode[T] | None = left
        self._right: BTNode[T] | None = right

    @property
    def k(self) -> T:
        return self._k

    @property
    def left(self) -> "BTNode[T] | None":
        return self._left

    @property
    def right(self) -> "BTNode[T] | None":
        return self._right


class BTree[T]:
    r"""
    A binary tree.

    Parameters
    ----------
    keys
        (Optional) A list of keys to insert in the tree in a breadth-first manner
        (empty slots should be filled by `None`).

        Defaults to `[]`.

    Examples
    --------
    .. code-block:: python
        
        bt = BTree([1, 2, 3, None, 4, 5, None, None, None, 6])
        print(bt)
        #           1
        #   /¯¯¯¯¯¯   ¯¯¯¯¯¯\
        #   2               3
        #    ¯¯¯\       /¯¯¯
        #       4       5
        #     /¯
        #     6
    """

    def __init__(self, ks: list[T | None] = []):
        self._root: BTNode[T] | None = BTree._array_to_bt_rec(ks, 0)

    def __repr__(self) -> str:
        """
        Returns a string representation of this binary tree (useful for debugging).

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

        q: Deque[tuple[(BTNode[T] | None, int, int, str)]] = deque(
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
        Whether this binary tree is non-empty.

        Return
        -------
        `bool`
            `True` if non-empty, `False` otherwise.
        """
        return self._root is not None

    @property
    def is_empty(self) -> bool:
        """
        Whether this binary tree is empty.
        """
        return self._root is None

    def __eq__(self, other) -> bool:
        if not isinstance(other, BTree):
            return False

        q1: Deque[BTNode[T] | None] = deque([self._root])
        q2: Deque[BTNode[T] | None] = deque([other._root])
        n1: BTNode[T] | None = None
        n2: BTNode[T] | None = None
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

    @staticmethod
    def _array_to_bt_rec(ks: list[T | None], i: int) -> BTNode[T] | None:
        if i >= len(ks) or ks[i] is None:
            return None

        return BTNode(
            ks[i],  # type: ignore
            BTree._array_to_bt_rec(ks, 2 * i + 1),
            BTree._array_to_bt_rec(ks, 2 * i + 2),
        )

    @property
    def size(self) -> int:
        """
        The size of this tree, i.e. its number of nodes.
        """
        return BTree._size_rec(self._root)

    @staticmethod
    def _size_rec(node: BTNode[T] | None) -> int:
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
        return 1 + BTree._size_rec(node._left) + BTree._size_rec(node._right)

    @property
    def height(self) -> int:
        """
        The height of this binary tree, i.e. the length of the longest path from the root to a leaf.
        """
        return BTree._height_rec(self._root)

    @staticmethod
    def _height_rec(node: BTNode[T] | None) -> int:
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
        return 1 + max(BTree._height_rec(node._left), BTree._height_rec(node._right))

    @property
    def is_min_heap(self) -> bool:
        """
        Whether this binary tree verifies the min heap property, i.e. that each node of
        the tree as a key lower than those of its children.
        """
        return self._is_min_heap_rec(self._root)

    def _is_min_heap_rec(self, node: BTNode[T] | None) -> bool:
        if node == None:
            return True

        cond = True
        if node.left != None:
            cond = cond and node._k <= node.left._k  # type: ignore
        if node.right != None:
            cond = cond and node._k <= node.right._k  # type: ignore

        return (
            cond
            and self._is_min_heap_rec(node.left)
            and self._is_min_heap_rec(node.right)
        )

    @property
    def is_max_heap(self) -> bool:
        """
        Whether this binary tree verifies the max heap property, i.e. that each node of
        the tree as a key greater than those of its children.
        """
        return self._is_max_heap_rec(self._root)

    def _is_max_heap_rec(self, node: BTNode[T] | None) -> bool:
        if node == None:
            return True

        cond = True
        if node.left != None:
            cond = cond and node._k >= node.left._k  # type: ignore
        if node.right != None:
            cond = cond and node._k >= node.right._k  # type: ignore

        return (
            cond
            and self._is_max_heap_rec(node.left)
            and self._is_max_heap_rec(node.right)
        )

    @property
    def is_bst(self) -> bool:
        """
        Whether this tree verifies the binary search tree property,
        i.e. that for each node, the left child's key is inferior
        to that node's key, and right child's key is superior.
        """
        return self._is_bst_rec(self._root, None, None)

    def _is_bst_rec(self, node: BTNode[T] | None, inf: T | None, sup: T | None) -> bool:
        if node == None:
            return True

        # on construit la condition sur "node"
        cond = True
        if inf != None:
            cond = cond and node._k <= inf  # type: ignore
        if sup != None:
            cond = cond and node._k > sup  # type: ignore

        return (
            self._is_bst_rec(node.left, node._k, sup)
            and cond
            and self._is_bst_rec(node.right, inf, node._k)
        )

    @property
    def is_complete(self) -> bool:
        """
        Whether this binary tree is complete.
        """
        # Another way do to it, but more costly:
        #     1) traverse the tree in breadth-first search, storing values in an array, as well as Nones if they are (O(n))
        #     2) trim the Nones at the end (worst case is 2^height-1 Nones to trim, say O(n))
        #     3) check if there is a None in the array; if so, the binary tree isn't complete (O(n))
        # Total: O(3n) in time; O(2n) in space (queue + array)

        # The better way:
        #     1) compute the height of the tree (O(log n) time, if complete tree, O(n) in the worst case; O(1) space, but recursion)
        #     2) traverse the tree in breadth-first search:
        #         - if None encountered at any level other than the last, return false
        #         - if None encountered at the last level, set a boolean flag (say "shouldBeNone")
        #         - if any node of the last level should be None and isn't, return false
        #     3) return true
        # Total: O(2n) in time; O(n) in space (queue)
        if self._root is None:
            return True

        h = self.height
        should_be_none = False
        is_last_lvl = False
        q: Deque[tuple[BTNode[T] | None, int]] = deque([(self._root, 0)])
        while q:
            node, lvl = q.popleft()
            is_last_lvl = lvl >= h

            if is_last_lvl and should_be_none and node is not None:
                return False

            if node is None:
                if not is_last_lvl:
                    return False
                else:
                    should_be_none = True
                    continue

            if not is_last_lvl:
                q.append((node.left, lvl + 1))
                q.append((node.right, lvl + 1))

        return True

    def lca(self, v: T, w: T) -> Option[T]:
        """
        Returns the *lowest common ancestor* of nodes with values *v* and *w* resp.

        The lowest common ancestor of two nodes *v* and *w* in a tree or directed
        acyclic graph (DAG) T is the lowest (i.e. deepest) node that has both v and w
        as descendants, where we define each node to be a descendant of itself
        (so if v has a direct connection from w, w is the lowest common ancestor).

        Parameters
        ----------
        a
        b

        Returns
        -------
        `Option[T]`
            May be `Option.NONE()` if tree is empty or more generally, if either
            *v* or *w* (or both) is not found in the tree.
        """
        lca_node = self._lca_rec(self._root, v, w)
        return Option.Some(lca_node._k) if lca_node is not None else Option.NONE()

    def _lca_rec(self, node: BTNode[T] | None, v: T, w: T) -> BTNode[T] | None:
        # Idea: I am a node. If I am v or w, I declare being the lca.
        # During the unraveling of recursion, if I have my two children
        # telling me they are the lca, then I am the lca.
        if node == None or node._k == v or node._k == w:
            return node
        lca_l = self._lca_rec(node._left, v, w)
        lca_r = self._lca_rec(node._right, v, w)
        if lca_l != None and lca_r != None:
            return node
        elif lca_l != None:
            return lca_l
        elif lca_r != None:
            return lca_r
        else:
            return None

    def contains(self, k: T) -> bool:
        """
        Returns whether this tree has a node with key *k*.

        Parameters
        ----------
        k

        Returns
        -------
        `bool`
        """
        q: Deque[BTNode[T] | None] = deque([self._root])
        while q:
            node = q.popleft()
            if node:
                if node._k == k:
                    return True

                q.append(node.left)
                q.append(node.right)

        return False

    def depth_first_traversal(
        self, f: Callable[[T], Any], order: DFTOrder = DFTOrder.PRE_ORDER
    ):
        """
        Traverses this tree in a depth-first manner.

        Parameters
        ----------
        f
            A function to apply on the key of each node traversed.
        order
            The order of the depth-first traversal.

            Defaults to `DFTOrder.PRE_ORDER`.

        Examples
        --------
        .. code-block:: python

            bt = BTree([1, 2, 3, 4, None, 5, None, 6, 7])
            s = StringIO()
            bt.depth_first_traversal(lambda k: s.write(f"{k} "))
            assert s.getvalue() == "1 2 4 6 7 3 5 "
        """
        match order:
            case DFTOrder.PRE_ORDER:
                BTree._depth_first_pre_order_traversal_rec(self._root, f)
            case DFTOrder.IN_ORDER:
                BTree._depth_first_in_order_traversal_rec(self._root, f)
            case DFTOrder.POST_ORDER:
                BTree._depth_first_post_order_traversal_rec(self._root, f)
            case DFTOrder.REVERSE_PRE_ORDER:
                BTree._depth_first_rev_pre_order_traversal_rec(self._root, f)
            case DFTOrder.REVERSE_IN_ORDER:
                BTree._depth_first_rev_in_order_traversal_rec(self._root, f)
            case DFTOrder.REVERSE_POST_ORDER:
                BTree._depth_first_rev_post_order_traversal_rec(self._root, f)

    @staticmethod
    def _depth_first_pre_order_traversal_rec(
        node: BTNode[T] | None, f: Callable[[T], Any]
    ):
        """
        Traverses the tree with *node* as root in a depth-first, pre-order manner.

        Parameters
        ----------
        node
            The root of the tree to walk.
        f
            A function to apply on the key of each node traversed.
        """
        if node is None:
            return

        f(node._k)
        if node._left is not None:
            BTree._depth_first_pre_order_traversal_rec(node._left, f)
        if node._right is not None:
            BTree._depth_first_pre_order_traversal_rec(node._right, f)

    @staticmethod
    def _depth_first_in_order_traversal_rec(
        node: BTNode[T] | None, f: Callable[[T], Any]
    ):
        """
        Traverses the tree with *node* as root in a depth-first, in-order manner.

        Parameters
        ----------
        node
            The root of the tree to walk.
        f
            A function to apply on the key of each node traversed.
        """
        if node is None:
            return

        if node._left is not None:
            BTree._depth_first_in_order_traversal_rec(node._left, f)
        f(node._k)
        if node._right is not None:
            BTree._depth_first_in_order_traversal_rec(node._right, f)

    @staticmethod
    def _depth_first_post_order_traversal_rec(
        node: BTNode[T] | None, f: Callable[[T], Any]
    ):
        """
        Traverses the tree with *node* as root in a depth-first, post-order manner.

        Parameters
        ----------
        node
            The root of the tree to walk.
        f
            A function to apply on the key of each node traversed.
        """
        if node is None:
            return

        if node._left is not None:
            BTree._depth_first_post_order_traversal_rec(node._left, f)
        if node._right is not None:
            BTree._depth_first_post_order_traversal_rec(node._right, f)
        f(node._k)

    @staticmethod
    def _depth_first_rev_pre_order_traversal_rec(
        node: BTNode[T] | None, f: Callable[[T], Any]
    ):
        """
        Traverses the tree with *node* as root in a depth-first, reverse pre-order manner.

        Parameters
        ----------
        node
            The root of the tree to walk.
        f
            A function to apply on the key of each node traversed.
        """
        if node is None:
            return

        f(node._k)
        if node._right is not None:
            BTree._depth_first_rev_pre_order_traversal_rec(node._right, f)
        if node._left is not None:
            BTree._depth_first_rev_pre_order_traversal_rec(node._left, f)

    @staticmethod
    def _depth_first_rev_in_order_traversal_rec(
        node: BTNode[T] | None, f: Callable[[T], Any]
    ):
        """
        Traverses the tree with *node* as root in a depth-first, reverse in-order manner.

        Parameters
        ----------
        node
            The root of the tree to walk.
        f
            A function to apply on the key of each node traversed.
        """
        if node is None:
            return

        if node._right is not None:
            BTree._depth_first_rev_in_order_traversal_rec(node._right, f)
        f(node._k)
        if node._left is not None:
            BTree._depth_first_rev_in_order_traversal_rec(node._left, f)

    @staticmethod
    def _depth_first_rev_post_order_traversal_rec(
        node: BTNode[T] | None, f: Callable[[T], Any]
    ):
        """
        Traverses the tree with *node* as root in a depth-first, reverse post-order manner.

        Parameters
        ----------
        node
            The root of the tree to walk.
        f
            A function to apply on the key of each node traversed.
        """
        if node is None:
            return

        if node._right is not None:
            BTree._depth_first_rev_post_order_traversal_rec(node._right, f)
        if node._left is not None:
            BTree._depth_first_rev_post_order_traversal_rec(node._left, f)
        f(node._k)

    def breadth_first_traversal(self, f: Callable[[T], Any]):
        """
        Traverses this tree in a breadth-first manner.

        Parameters
        ----------
        f
            A function to apply on the key of each node traversed.

        Examples
        --------
        .. code-block:: python

            bt = BTree([1, 2, 3, 4, None, 5, None, 6, 7])
            s = StringIO()
            bt.breadth_first_traversal(lambda k: s.write(f"{k} "))
            assert s.getvalue() == "1 2 3 4 5 6 7 "
        """
        if self._root is None:
            return

        q: Deque[BTNode[T]] = deque([self._root])
        while q:
            node = q.popleft()
            f(node._k)
            if node._left != None:
                q.append(node._left)
            if node._right != None:
                q.append(node._right)
