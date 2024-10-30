from collections import deque
from enum import Enum
from typing import Deque

from option import Option


class Color(Enum):
    BLACK = 0
    RED = 1


class RBTNode[T]:
    """
    A node of `RBTree[T]`.

    Parameters
    ----------
    k
        The value stored in the node.
    c
        The color of the node (`Color.RED` or `Color.BLACK`).
    left
        (Optional) The left child of the node.

        Defaults to `None`.
    right
        (Optional) The right child of the node.

        Defaults to `None`.
    parent
        (Optional) The parent of the node.

        Defaults to `None`.
    """

    def __init__(
        self,
        k: T,
        c: Color,
        left: "RBTNode[T] | None" = None,
        right: "RBTNode[T] | None" = None,
        parent: "RBTNode[T] | None" = None,
    ):
        self._k = k
        self._c = c
        self._left = left
        self._right = right
        self._parent = parent

    @property
    def k(self) -> T:
        return self._k

    @property
    def c(self) -> Color:
        return self._c

    @property
    def left(self) -> "RBTNode[T] | None":
        return self._left

    @property
    def right(self) -> "RBTNode[T] | None":
        return self._right

    @property
    def parent(self) -> "RBTNode[T] | None":
        return self._parent


class RBTree[T]:
    r"""
    A red-black binary search tree.

    Parameters
    ----------
    ks
        (Optional) A list of keys to insert in the tree.

        Defaults to `[]`.

    Examples
    --------
    .. code-block:: python

        rbt = RBTree([10, 5, 15, 2, 12, 7, 17])
        print(rbt)
        #      10
        #   /¯¯¯ ¯¯¯\
        #   5      15
        # /¯ ¯\   /¯ ¯\
        # 2   7  12  17
    """

    def __init__(self, ks: list[T] = []):
        self._root: RBTNode[T] | None = None
        for k in ks:
            self.insert(k)

    def __repr__(self) -> str:
        """
        Returns a string representation of this red-black binary search tree
        (useful for debugging).

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

        q: Deque[tuple[(RBTNode[T] | None, int, int, str)]] = deque(
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
                valstr = str(t[0].key)
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
                color = "\033[91m" if t[0].c == Color.RED else "\033[37m"
                pstr += (
                    " " * (t[2] - pre - len(valstr)) + f"{color}{valstr}\033[0m"
                )  # correct the position according to the number size
                pre = t[2]
            s += linestr + "\n" + pstr + "\n"
        return s

    def __len__(self) -> int:
        return self.size

    def __bool__(self) -> bool:
        """
        Whether this tree is non-empty.

        Return
        -------
        `bool`
            `True` if non-empty, `False` otherwise.
        """
        return self._root is not None

    @property
    def is_empty(self) -> bool:
        """
        Whether this tree is empty.
        """
        return self._root is None

    def __eq__(self, other) -> bool:
        if not isinstance(other, RBTree):
            return False

        q1: Deque[RBTNode[T] | None] = deque([self._root])
        q2: Deque[RBTNode[T] | None] = deque([other._root])
        n1: RBTNode[T] | None = None
        n2: RBTNode[T] | None = None
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
        Returns the size of this tree, i.e. its number of nodes.

        Returns
        -------
        `int`
        """
        return RBTree._size_rec(self._root)

    @staticmethod
    def _size_rec(node: RBTNode[T] | None) -> int:
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
        return 1 + RBTree._size_rec(node._left) + RBTree._size_rec(node._right)

    @property
    def height(self) -> int:
        """
        Returns the height of this tree, i.e. the length of the longest path from the root to a leaf.

        Returns
        -------
        `int`
        """
        return RBTree._height_rec(self._root)

    @staticmethod
    def _height_rec(node: RBTNode[T] | None) -> int:
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
        return 1 + max(RBTree._height_rec(node._left), RBTree._height_rec(node._right))

    def insert(self, k: T) -> bool:
        """
        Inserts value *k* into this tree.

        Parameters
        ----------
        k

        Returns
        -------
        `bool`
            `True` if a new node was inserted, `False` if a node
            with key *k* already exists.
        """
        return self._insert_it(k)

    def _insert_it(self, k: T) -> bool:
        """
        Inserts value *k* into this tree.

        Implementation details
        ----------------------
        This function inserts a new value iteratively.

        Parameters
        ----------
        k

        Returns
        -------
        `bool`
            `True` if a new node was inserted, `False` if a node
            with key *k* already exists.
        """
        # Find the parent/previous node to the one we want to insert.
        cur_node = self._root
        p = None
        while cur_node is not None:
            p = cur_node
            if k < cur_node._k:  # type: ignore
                cur_node = cur_node._left
            elif k > cur_node._k:  # type: ignore
                cur_node = cur_node._right
            else:
                break

        # Insert the new node if needed.
        n = RBTNode(k, Color.RED, None, None, p)
        if p is None:
            self._root = n
            return True
        if k < p._k:  # type: ignore
            p._left = n
        elif k > p._k:  # type: ignore
            p._right = n
        else:  # k == p.key
            return False

        # Rotate and recolor to maintain red-black tree invariants.
        while p is not None:
            # Parent is black, so nothing to do.
            if p._c == Color.BLACK:
                break

            # Parent is root and red, so just repaint it in black.
            gp = p._parent
            if gp is None:
                p._c = Color.BLACK
                break

            # Parent is red and uncle is black (or None).
            u = gp._left if p == gp._right else gp._right
            if u is None or u._c == Color.BLACK:
                # Rotate so as to make `n` an outer child of `gp`.
                if p == gp._left and n == p._right:
                    self._left_rotate(p)
                    n = p
                    p = gp._left
                elif p == gp._right and n == p._left:
                    self._right_rotate(p)
                    n = p
                    p = gp._right
                # Now that `n` is an outer child, we only need one
                # last rotation for the parent to take the place
                # of the grandparent, then recolor.
                if p == gp._left:
                    self._right_rotate(gp)
                else:
                    self._left_rotate(gp)
                p._c = Color.BLACK  # type: ignore
                gp._c = Color.RED
                break

            # Parent is red and uncle is red.
            # Repaint parent and uncle in black and grandparent in red,
            # but that may introduce violations from the grandparent up,
            # so continue the loop
            p._c = Color.BLACK
            u._c = Color.BLACK
            gp._c = Color.RED
            n = gp
            p = n._parent

        return True

    def get(self, k: T) -> Option[RBTNode[T]]:
        """
        Returns the node with key *k* if found.

        Parameters
        ----------
        k

        Returns
        -------
        `Option[RBTNode[T]]`
        """
        return self._get_it(k)

    def _get_it(self, k: T) -> Option[RBTNode[T]]:
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
        `Option[RBTNode[T]]`
        """
        n = self._root
        while n is not None:
            if n._k == k:
                return Option.Some(n)
            elif k < n._k:  # type: ignore
                n = n._left
            else:
                n = n._right

        return Option.NONE()

    def _get_rec(self, k: T) -> Option[RBTNode[T]]:
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
        `Option[RBTNode[T]]`
        """
        node = self._get_rec_helper(self._root, k)
        return Option.Some(node) if node is not None else Option.NONE()

    def _get_rec_helper(self, node: RBTNode[T] | None, key: T) -> RBTNode[T] | None:
        if node == None:
            return None
        elif node._k == key:
            return node
        elif key < node._k:  # type: ignore
            return self._get_rec_helper(node._left, key)
        else:
            return self._get_rec_helper(node._right, key)

    def delete(self, k: T) -> bool:
        """
        Deletes the node with key *k*, if present in this tree.

        Parameters
        ----------
        k

        Returns
        -------
        `bool`
            `True` if a node with key *k* was found in the tree and deleted,
            `False` if no such node was found.
        """
        return self._delete_it(k)

    def _delete_it(self, k: T) -> bool:
        """
        Deletes the node with key *k*, if present in this tree.

        Note
        ----
        This implementation is inspired by https://en.wikipedia.org/wiki/Red%E2%80%93black_tree#Removal.

        Parameters
        ----------
        k

        Returns
        -------
        `bool`
            `True` if a node with key *k* was found in the tree and deleted,
            `False` if no such node was found.
        """
        # If empty tree, return early.
        if self._root is None:
            return False

        # Find the node to delete.
        # ------------------------
        p = None
        n = self._root
        while n is not None and n._k != k:
            if k < n._k:  # type: ignore
                p = n
                n = n._left
            elif k > n._k:  # type: ignore
                p = n
                n = n._right

        if n is None:  # Didn't found a node with key *k*.
            return False

        # Delete the node.
        # ----------------
        if n._left is None and n._right is None:  # node is a leaf
            # When the deleted node has no children (both NIL) and is the root, replace it with NIL.
            if p is None:
                self._root = None
            # When the deleted node has no children (both NIL), and is red, simply remove the leaf node.
            elif n._c == Color.RED:
                if p._left == n:
                    p._left = None
                else:
                    p._right = None
            # When the deleted node has no children (both NIL), and is black, deleting it will create an imbalance
            # and requires a fixup.
            else:
                is_left = p._left == n
                if p._left == n:
                    p._left = None
                else:
                    p._right = None

                while p is not None:
                    if is_left:
                        s = p._right
                        assert s is not None
                        cn = s._left
                        dn = s._right
                    else:
                        s = p._left
                        assert s is not None
                        cn = s._right
                        dn = s._left

                    # Case 1
                    # ******
                    # If sibling is red, then parent and nephews are black.
                    # Entering this branch, we know that:
                    #   n is black
                    #   p is not None and black
                    #   s is red
                    #   cn is black
                    #   dn is black
                    if s._c == Color.RED:
                        if is_left:
                            self._left_rotate(p)
                        else:
                            self._right_rotate(p)
                        p._c = Color.RED
                        s._c = Color.BLACK

                        s = cn
                        assert s is not None
                        if is_left:
                            cn = s._left
                            dn = s._right
                        else:
                            cn = s._right
                            dn = s._left

                        if dn is not None and dn._c == Color.RED:
                            # Now dn is red and s is black, which corresponds to case 2,
                            # which we copy past here.
                            if is_left:
                                self._left_rotate(p)
                            else:
                                self._right_rotate(p)
                            s._c = p._c
                            p._c = Color.BLACK
                            dn._c = Color.BLACK
                            break
                        elif cn is not None and cn._c == Color.RED:
                            # Now cn is red and s is black, which corresponds to case 3,
                            # which we copy past here.
                            if is_left:
                                self._right_rotate(s)
                            else:
                                self._left_rotate(s)
                            s._c = Color.RED
                            cn._c = Color.BLACK
                            dn = s
                            s = cn

                            if is_left:
                                self._left_rotate(p)
                            else:
                                self._right_rotate(p)
                            s._c = p._c
                            p._c = Color.BLACK
                            dn._c = Color.BLACK
                            break
                        else:
                            # Otherwise cn and dn are black, which corresponds to case 4.
                            s._c = Color.RED
                            p._c = Color.BLACK
                            break

                    # Case 2
                    # ******
                    # Entering this branch, we know that:
                    #   n is black
                    #   p is not None
                    #   s is black
                    #   dn is red
                    elif dn is not None and dn._c == Color.RED:
                        if is_left:
                            self._left_rotate(p)
                        else:
                            self._right_rotate(p)
                        s._c = p._c
                        p._c = Color.BLACK
                        dn._c = Color.BLACK
                        break

                    # Case 3
                    # ******
                    # Entering this branch, we know that:
                    #   n is black
                    #   p is not None
                    #   s is black
                    #   cn is red
                    #   dn is black
                    elif cn is not None and cn._c == Color.RED:
                        if is_left:
                            self._right_rotate(s)
                        else:
                            self._left_rotate(s)
                        s._c = Color.RED
                        cn._c = Color.BLACK
                        dn = s
                        s = cn

                        # Now dn is red and s is black, which corresponds to case 2,
                        # which we copy past here.
                        if is_left:
                            self._left_rotate(p)
                        else:
                            self._right_rotate(p)
                        s._c = p._c
                        p._c = Color.BLACK
                        dn._c = Color.BLACK
                        break

                    # Case 4
                    # ******
                    # Entering this branch, we know that:
                    #   n is black
                    #   p is not None and red
                    #   s is black
                    #   cn is black
                    #   dn is black
                    elif p._c == Color.RED:
                        s._c = Color.RED
                        p._c = Color.BLACK
                        break

                    s._c = Color.RED
                    n = p
                    p = n._parent
                    if p is not None:
                        is_left = p._left == n

        # When the deleted node has 2 children (non-NIL), then we can swap its value with its in-order successor
        # (the leftmost child of the right subtree), and then delete the successor instead.
        # Since the successor is leftmost, it can only have a right child (non-NIL) or no child at all.
        elif n._left is not None and n._right is not None:
            # First find the node with the smallest greater key.
            sg_node = n._right
            sg_parent = n
            while sg_node._left is not None:
                sg_parent = sg_node
                sg_node = sg_node._left
            # Change the key of node to be that of sg_node.
            n._k = sg_node._k
            # Detach sg_node.
            if sg_parent._left == sg_node:
                sg_parent._left = None
            else:
                sg_parent._right = None

        # When the deleted node has only 1 child (non-NIL).
        # In this case, just replace the node with its child, and color it black.
        # The single child (non-NIL) must be red according to conclusion 5,
        # and the deleted node must be black according to requirement 3.
        elif n._left is not None:
            if p is None:
                self._root = n._left
            else:
                if p._left == n:
                    p._left = n._left
                else:
                    p._right = n._left
            n._left._c = Color.BLACK
            n._left._parent = p
        elif n._right is not None:
            if p is None:
                self._root = n._right
            else:
                if p._left == n:
                    p._left = n._right
                else:
                    p._right = n._right
            n._right._c = Color.BLACK
            n._right._parent = p

        return True

    def _left_rotate(self, node: RBTNode[T]):
        """
        Performs a left rotation of the subtree with root *node*.

        Warning
        -------
        `node.right` must *not* be `None`, otherwise this operation doesn't make
        sense and will fail with an `AssertionError`.

        Parameters
        ----------
        node
        """
        assert node._right is not None

        gp = node._parent  # grandparent
        rc = node._right  # right child
        lgc = rc._left  # left grandchild, root of the inner subtree

        node._right = lgc
        if lgc is not None:
            lgc._parent = node

        rc._left = node
        node._parent = rc
        rc._parent = gp

        if gp is not None:
            if node == gp._left:
                gp._left = rc
            else:
                gp._right = rc
        else:
            self._root = rc

    def _right_rotate(self, node: RBTNode[T]):
        """
        Performs a right rotation of the subtree with root *node*.

        Warning
        -------
        `node.left` must *not* be `None`, otherwise this operation doesn't make
        sense and will fail with an `AssertionError`.

        Parameters
        ----------
        node
        """
        assert node._left is not None

        gp = node._parent  # grandparent
        lc = node._left  # left child
        rgc = lc._right  # right grandchild, root of the inner subtree

        node._left = rgc
        if rgc is not None:
            rgc._parent = node

        lc._right = node
        node._parent = lc
        lc._parent = gp

        if gp is not None:
            if node == gp._left:
                gp._left = lc
            else:
                gp._right = lc
        else:
            self._root = lc

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
        return RBTree._contains_rec_helper(self._root, k)

    @staticmethod
    def _contains_rec_helper(root: RBTNode[T] | None, k: T) -> bool:
        if root is None:
            return False
        if k < root._k:  # type: ignore
            return RBTree._contains_rec_helper(root._left, k)
        elif k > root._k:  # type: ignore
            return RBTree._contains_rec_helper(root._right, k)
        else:
            return True
